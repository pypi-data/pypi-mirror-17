"""Implementation of recurrent network, including Gauss-Newton approximation
for use in Hessian-free optimization.

.. codeauthor:: Gautam <gautamrbharadwaj@gmail.com>

Based on
Martens, J., & Sutskever, I. (2011). Learning recurrent neural networks with
hessian-free optimization. Proceedings of the 28th International Conference on
Machine Learning.
"""

from __future__ import print_function

import numpy as np

import gaunn as gn


class RNNet(gn.FFNet):
    """Implementation of recurrent deep network (including gradient/curvature
    computation).

    :param list rec_layers: indices of layers with recurrent connections
            (default is to make all except first and last layers recurrent)
    :param dict W_rec_params: parameters used to initialize recurrent
        weights (passed to :meth:`~.init_weights`)
    :param tuple truncation: a tuple `(n,k)` where backpropagation through
        time will be executed every `n` timesteps and run backwards for `k`
        steps (defaults to full backprop if None)

    See :class:`.FFNet` for the remaining parameters."""

    def __init__(self, shape, rec_layers=None, W_rec_params=None,
                 truncation=None, **kwargs):

        # define recurrence for each layer (needs to be done before super
        # constructor because this is used in compute_offsets)
        if rec_layers is None:
            # assume all recurrent except first/last layer
            rec_layers = np.arange(1, len(shape) - 1)
        self.rec_layers = rec_layers

        # super constructor
        super(RNNet, self).__init__(shape, **kwargs)

        self.truncation = truncation

        # add on recurrent weights
        if kwargs.get("load_weights", None) is None and len(rec_layers) > 0:
            if W_rec_params is None:
                W_rec_params = dict()
            self.W = np.concatenate(
                (self.W, self.init_weights([(self.shape[l], self.shape[l])
                                            for l in range(self.n_layers)
                                            if l in rec_layers],
                                           **W_rec_params)))

    def forward(self, inputs, params=None, deriv=False, init_activations=None,
                init_state=None):
        """Compute layer activations for given input and parameters.

        :param inputs: input vectors (passed to first layer)
        :type inputs: :class:`~numpy:numpy.ndarray`
        :param params: parameter vector (weights) for the network (defaults to
            ``self.W``)
        :type params: :class:`~numpy:numpy.ndarray`
        :param bool deriv: if True then also compute the derivative of the
            activations
        :param list init_activations: initial values for the activations in
            each layer
        :param list init_state: initial values for the internal state of any
            stateful nonlinearities
        """

        # input shape = [minibatch_size, seq_len, input_dim]
        # activations shape = [n_layers, minibatch_size, seq_len, layer_size]

        params = self.W if params is None else params

        if isinstance(inputs, gn.nl.Plant):
            # reset the plant
            # TODO: allow the initial state of plant to be set?
            inputs.reset()

        batch_size = inputs.shape[0]
        sig_len = inputs.shape[1]

        activations = [np.zeros((batch_size, sig_len, l), dtype=self.dtype)
                       for l in self.shape]

        # temporary space to minimize memory allocations
        tmp_space = [np.zeros((batch_size, l), dtype=self.dtype)
                     for l in self.shape]

        if deriv:
            d_activations = [None for _ in self.layers]

        for i, l in enumerate(self.layers):
            # reset any state in the nonlinearities
            l.reset(None if init_state is None else init_state[i])

        W_recs = [self.get_weights(params, (i, i))
                  for i in range(self.n_layers)]
        for s in range(sig_len):
            for i in range(self.n_layers):
                if i == 0:
                    # get the external input
                    if isinstance(inputs, gn.nl.Plant):
                        if s == 0 and init_activations is not None:
                            ff_input = inputs(init_activations[-1])
                        else:
                            # call the plant with the output of the previous
                            # timestep to generate the next input
                            # note: this will pass zeros on the first timestep
                            # if init_activations is not set
                            ff_input = inputs(activations[-1][:, s - 1])
                    else:
                        ff_input = inputs[:, s]
                else:
                    # compute feedforward input
                    ff_input = np.zeros_like(activations[i][:, s])
                    for pre in self.back_conns[i]:
                        W, b = self.get_weights(params, (pre, i))

                        ff_input += np.dot(activations[pre][:, s], W,
                                           out=tmp_space[i])
                        ff_input += b

                # recurrent input
                if i in self.rec_layers:
                    if s > 0:
                        rec_input = np.dot(activations[i][:, s - 1],
                                           W_recs[i][0], out=tmp_space[i])
                    elif init_activations is None:
                        # apply bias input on first timestep
                        rec_input = W_recs[i][1]
                    else:
                        # use the provided activations to initialize the
                        # 'previous' timestep
                        rec_input = np.dot(init_activations[i],
                                           W_recs[i][0], out=tmp_space[i])
                else:
                    rec_input = 0

                # apply activation function
                activations[i][:, s] = self.layers[i].activation(ff_input +
                                                                 rec_input)

                # compute derivative
                if deriv:
                    d_act = self.layers[i].d_activation(ff_input + rec_input,
                                                        activations[i][:, s])
                    if d_activations[i] is None:
                        # note: we can't allocate this array ahead of time,
                        # because we don't know if d_activations will be
                        # returning diagonal vectors or matrices
                        d_activations[i] = np.zeros(
                            np.concatenate(([batch_size], [sig_len],
                                            d_act.shape[1:])),
                            dtype=self.dtype)
                    d_activations[i][:, s] = d_act

        for i, a in enumerate(activations):
            if not np.all(np.isfinite(a)):
                raise OverflowError("Non-finite nonlinearity activation "
                                    "value (layer %d) \n %s" %
                                    (i, a[not np.isfinite(a)]))

        if deriv:
            return activations, d_activations

        return activations

    def calc_grad(self):
        """Compute parameter gradient."""

        grad = np.zeros_like(self.W)
        W_recs = [self.get_weights(self.W, (l, l))
                  for l in range(self.n_layers)]
        batch_size = self.inputs.shape[0]
        sig_len = self.inputs.shape[1]

        # temporary space to minimize memory allocations
        tmp_act = [np.zeros((batch_size, l), dtype=self.dtype)
                   for l in self.shape]
        tmp_grad = np.zeros_like(grad)

        if self.truncation is None:
            trunc_per = trunc_len = sig_len
        else:
            trunc_per, trunc_len = self.truncation

        for n in range(trunc_per - 1, sig_len, trunc_per):
            # every trunc_per timesteps we want to run backprop

            deltas = [np.zeros((batch_size, l), dtype=self.dtype)
                      for l in self.shape]
            state_deltas = [None if not l.stateful else
                            np.zeros((batch_size, self.shape[i]),
                                     dtype=self.dtype)
                            for i, l in enumerate(self.layers)]

            # backpropagate error
            for s in range(n, np.maximum(n - trunc_len, -1), -1):
                # execute trunc_len steps of backprop through time

                error = self.loss.d_loss([a[:, s] for a in self.activations],
                                         self.targets[:, s])
                error = [np.zeros_like(self.activations[i][:, s]) if e is None
                         else e for i, e in enumerate(error)]

                for l in range(self.n_layers - 1, -1, -1):
                    for post in self.conns[l]:
                        error[l] += np.dot(deltas[post],
                                           self.get_weights(self.W,
                                                            (l, post))[0].T,
                                           out=tmp_act[l])

                        # feedforward gradient
                        W_grad, b_grad = self.get_weights(grad, (l, post))
                        W_tmp_grad, b_tmp_grad = self.get_weights(tmp_grad,
                                                                  (l, post))
                        W_grad += np.dot(self.activations[l][:, s].T,
                                         deltas[post], out=W_tmp_grad)
                        b_grad += np.sum(deltas[post], axis=0, out=b_tmp_grad)

                    # add recurrent error
                    if l in self.rec_layers:
                        error[l] += np.dot(deltas[l], W_recs[l][0].T,
                                           out=tmp_act[l])

                    # compute deltas
                    if not self.layers[l].stateful:
                        self.J_dot(self.d_activations[l][:, s], error[l],
                                   transpose_J=True, out=deltas[l])
                    else:
                        d_input = self.d_activations[l][:, s, ..., 0]
                        d_state = self.d_activations[l][:, s, ..., 1]
                        d_output = self.d_activations[l][:, s, ..., 2]

                        state_deltas[l] += self.J_dot(d_output, error[l],
                                                      transpose_J=True,
                                                      out=tmp_act[l])
                        self.J_dot(d_input, state_deltas[l], transpose_J=True,
                                   out=deltas[l])
                        self.J_dot(d_state, state_deltas[l], transpose_J=True,
                                   out=state_deltas[l])

                    # gradient for recurrent weights
                    if l in self.rec_layers:
                        W_grad, b_grad = self.get_weights(grad, (l, l))
                        W_tmp_grad, b_tmp_grad = self.get_weights(tmp_grad,
                                                                  (l, l))
                        if s > 0:
                            W_grad += np.dot(self.activations[l][:, s - 1].T,
                                             deltas[l], out=W_tmp_grad)
                        else:
                            # put remaining gradient into initial bias
                            b_grad += np.sum(deltas[l], axis=0,
                                             out=b_tmp_grad)

        grad /= batch_size

        return grad

    def check_grad(self, calc_grad):
        """Check gradient via finite differences (for debugging)."""

        eps = 1e-6
        grad = np.zeros_like(calc_grad)

        sig_len = self.inputs.shape[1]
        if self.truncation is None:
            trunc_per = trunc_len = sig_len
        else:
            trunc_per, trunc_len = self.truncation

        inc_W = np.zeros_like(self.W)

        for n in range(trunc_per, sig_len + 1, trunc_per):
            start = np.maximum(n - trunc_len, 0)

            # the truncated backprop gradient is equivalent to running the
            # network normally for the initial timesteps and then just changing
            # the parameters for the truncation period.  so that's what we're
            # simulating here.
            if start > 0:
                prev = self.forward(self.inputs[:, :start], self.W)
                init_a = [p[:, -1] for p in prev]
                init_s = [l.state.copy() if l.stateful else None
                          for l in self.layers]
            else:
                init_a = None
                init_s = None

            for i in range(len(self.W)):
                inc_W[i] = eps

                out_inc = self.forward(self.inputs[:, start:n], self.W + inc_W,
                                       init_activations=init_a,
                                       init_state=init_s)
                out_dec = self.forward(self.inputs[:, start:n], self.W - inc_W,
                                       init_activations=init_a,
                                       init_state=init_s)

                error_inc = self.loss.batch_loss(out_inc,
                                                 self.targets[:, start:n])

                error_dec = self.loss.batch_loss(out_dec,
                                                 self.targets[:, start:n])

                grad[i] += (error_inc - error_dec) / (2 * eps)

                inc_W[i] = 0

        try:
            assert np.allclose(calc_grad, grad, rtol=1e-3)
        except AssertionError:
            print("calc_grad")
            print(calc_grad)
            print("finite grad")
            print(grad)
            print("calc_grad - finite grad")
            print(calc_grad - grad)
            print("calc_grad / finite grad")
            print(calc_grad / grad)
            input("Paused (press enter to continue)")

    def calc_G(self, v, damping=0, out=None):
        """Compute Gauss-Newton matrix-vector product."""

        if out is None:
            Gv = np.zeros(self.W.size, dtype=self.dtype)
        else:
            Gv = out
            Gv.fill(0)

        batch_size = self.inputs.shape[0]
        sig_len = self.inputs.shape[1]

        # temporary space to minimize memory allocations
        tmp_act = [np.zeros((batch_size, l), dtype=self.dtype)
                   for l in self.shape]
        tmp_grad = np.zeros_like(Gv)

        # R forward pass
        R_states = [None if not l.stateful else
                    np.zeros((batch_size, self.shape[i]), dtype=self.dtype)
                    for i, l in enumerate(self.layers)]
        R_activations = self.tmp_space
        for a in R_activations:
            a.fill(0)

        v_recs = [self.get_weights(v, (l, l))
                  for l in range(self.n_layers)]
        W_recs = [self.get_weights(self.W, (l, l))
                  for l in range(self.n_layers)]
        Gv_recs = [self.get_weights(Gv, (l, l))
                   for l in range(self.n_layers)]
        v_ff = dict([(conn, self.get_weights(v, conn))
                     for conn in self.offsets])
        W_ff = dict([(conn, self.get_weights(self.W, conn))
                     for conn in self.offsets])
        Gv_ff = dict([(conn, self.get_weights(Gv, conn))
                      for conn in self.offsets])

        for s in range(sig_len):
            for l in range(self.n_layers):
                R_act = R_activations[l][:, s]

                # input from feedforward connections
                for pre in self.back_conns[l]:
                    vw, vb = v_ff[(pre, l)]
                    Ww, _ = W_ff[(pre, l)]

                    R_act += np.dot(self.activations[pre][:, s], vw,
                                    out=tmp_act[l])
                    R_act += vb
                    R_act += np.dot(R_activations[pre][:, s], Ww,
                                    out=tmp_act[l])

                # recurrent input
                if l in self.rec_layers:
                    if s == 0:
                        # bias input on first step
                        R_act += v_recs[l][1]
                    else:
                        R_act += np.dot(self.activations[l][:, s - 1],
                                        v_recs[l][0], out=tmp_act[l])
                        R_act += np.dot(R_activations[l][:, s - 1],
                                        W_recs[l][0], out=tmp_act[l])

                if not self.layers[l].stateful:
                    self.J_dot(self.d_activations[l][:, s], R_act, out=R_act)
                else:
                    d_input = self.d_activations[l][:, s, ..., 0]
                    d_state = self.d_activations[l][:, s, ..., 1]
                    d_output = self.d_activations[l][:, s, ..., 2]

                    R_states[l] = self.J_dot(d_state, R_states[l])

                    R_states[l] += self.J_dot(d_input, R_act, out=tmp_act[l])
                    self.J_dot(d_output, R_states[l], out=R_act)

        # R backward pass
        if self.truncation is None:
            trunc_per = trunc_len = sig_len
        else:
            trunc_per, trunc_len = self.truncation

        R_error = [np.zeros((batch_size, l), dtype=self.dtype)
                   for l in self.shape]
        R_deltas = [np.zeros((batch_size, l), dtype=self.dtype)
                    for l in self.shape]

        for n in range(trunc_per - 1, sig_len, trunc_per):
            for i in range(self.n_layers):
                R_deltas[i].fill(0)
                if R_states[i] is not None:
                    R_states[i].fill(0)

            for s in range(n, np.maximum(n - trunc_len, -1), -1):
                for l in range(self.n_layers - 1, -1, -1):
                    if self.d2_loss[l] is not None:
                        np.multiply(self.d2_loss[l][:, s],
                                    R_activations[l][:, s],
                                    out=R_error[l])
                    else:
                        R_error[l].fill(0)

                    # error from feedforward connections
                    for post in self.conns[l]:
                        R_error[l] += np.dot(R_deltas[post],
                                             W_ff[(l, post)][0].T,
                                             out=tmp_act[l])

                        # feedforward gradient
                        W_g, b_g = Gv_ff[(l, post)]
                        W_tmp_grad, b_tmp_grad = self.get_weights(tmp_grad,
                                                                  (l, post))
                        W_g += np.dot(self.activations[l][:, s].T,
                                      R_deltas[post], out=W_tmp_grad)
                        b_g += np.sum(R_deltas[post], axis=0, out=b_tmp_grad)

                    # add recurrent error
                    if l in self.rec_layers:
                        R_error[l] += np.dot(R_deltas[l], W_recs[l][0].T,
                                             out=tmp_act[l])

                    # compute deltas
                    if not self.layers[l].stateful:
                        self.J_dot(self.d_activations[l][:, s], R_error[l],
                                   transpose_J=True, out=R_deltas[l])
                    else:
                        d_input = self.d_activations[l][:, s, ..., 0]
                        d_state = self.d_activations[l][:, s, ..., 1]
                        d_output = self.d_activations[l][:, s, ..., 2]

                        R_states[l] += self.J_dot(d_output, R_error[l],
                                                  transpose_J=True,
                                                  out=tmp_act[l])
                        self.J_dot(d_input, R_states[l], transpose_J=True,
                                   out=R_deltas[l])
                        self.J_dot(d_state, R_states[l], transpose_J=True,
                                   out=R_states[l])

                    # recurrent gradient
                    if l in self.rec_layers:
                        W_g, b_g = Gv_recs[l]
                        W_tmp_grad, b_tmp_grad = self.get_weights(tmp_grad,
                                                                  (l, l))
                        if s > 0:
                            W_g += np.dot(self.activations[l][:, s - 1].T,
                                          R_deltas[l], out=W_tmp_grad)
                        else:
                            b_g += np.sum(R_deltas[l], axis=0, out=b_tmp_grad)

        Gv /= batch_size

        Gv += damping * v  # Tikhonov damping

        return Gv

    def load_GPU_data(self):
        """Load data for the current epoch onto GPU."""

        from pycuda import gpuarray

        def split_axes(array, n=1):
            # split a multidimensional array into a corresponding list of lists
            # along the first n axes (this is used so that array.__getitem__
            # isn't called repeatedly, as it is somewhat expensive for
            # gpuarrays)
            if n == 1:
                return [a for a in array]

            return [split_axes(a, n - 1) for a in array]

        # clear out old data (this would happen eventually on its own, but by
        # doing it first we make sure there is room on the GPU before
        # creating new arrays)
        if hasattr(self, "GPU_W"):
            del self.GPU_W
            del self.GPU_activations
            del self.GPU_d_activations
            del self.GPU_d2_loss
            del self.GPU_tmp_space
            del self.GPU_states
            del self.GPU_errors
            del self.GPU_deltas

        self.GPU_W = gpuarray.to_gpu(self.W)

        # rearrange GPU data so that signal is the first axis (so
        # that each time step is a single block of memory in GPU_calc_G)
        self.GPU_activations = [
            split_axes(gpuarray.to_gpu(np.ascontiguousarray(
                np.swapaxes(a, 0, 1))), 1)
            for a in self.activations]

        self.GPU_d_activations = [
            split_axes(gpuarray.to_gpu(np.ascontiguousarray(
                np.rollaxis(np.swapaxes(a, 0, 1), -1, 1))), 2)
            if self.layers[i].stateful else
            split_axes(gpuarray.to_gpu(np.ascontiguousarray(
                np.swapaxes(a, 0, 1))), 1)
            for i, a in enumerate(self.d_activations)]

        self.GPU_d2_loss = [
            split_axes(gpuarray.to_gpu(np.ascontiguousarray(
                np.swapaxes(a, 0, 1))), 1)
            if a is not None else None for a in self.d2_loss]

        self.GPU_tmp_space = [split_axes(gpuarray.empty((a.shape[1],
                                                         a.shape[0],
                                                         a.shape[2]),
                                                        self.dtype), 1)
                              for a in self.activations]

        # pre-allocate calc_G arrays
        batch_size = self.inputs.shape[0]
        self.GPU_states = [[gpuarray.empty((batch_size, self.shape[i]),
                                           dtype=self.dtype) for _ in range(2)]
                           if l.stateful else None
                           for i, l in enumerate(self.layers)]
        self.GPU_errors = [gpuarray.empty((batch_size, l),
                                          dtype=self.dtype)
                           for l in self.shape]
        self.GPU_deltas = [gpuarray.empty((batch_size, l),
                                          dtype=self.dtype)
                           for l in self.shape]

    def GPU_calc_G(self, v, damping=0, out=None):
        """Compute Gauss-Newton matrix-vector product on GPU."""

        from pycuda import gpuarray

        if out is None or not isinstance(out, gpuarray.GPUArray):
            Gv = gpuarray.zeros(self.W.shape, dtype=self.dtype)
        else:
            Gv = out
            Gv.fill(0)

        if not isinstance(v, gpuarray.GPUArray):
            GPU_v = gpuarray.to_gpu(v)
        else:
            GPU_v = v

        batch_size = self.inputs.shape[0]
        sig_len = self.inputs.shape[1]

        # R forward pass
        R_states = self.GPU_states
        R_activations = self.GPU_tmp_space
        for i in range(self.n_layers):
            R_activations[i][0].base.fill(0)
            if R_states[i] is not None:
                R_states[i][0].fill(0)

        v_recs = [self.get_weights(GPU_v, (l, l))
                  for l in range(self.n_layers)]
        W_recs = [self.get_weights(self.GPU_W, (l, l))
                  for l in range(self.n_layers)]
        Gv_recs = [self.get_weights(Gv, (l, l))
                   for l in range(self.n_layers)]
        v_ff = dict([(conn, self.get_weights(GPU_v, conn))
                     for conn in self.offsets])
        W_ff = dict([(conn, self.get_weights(self.GPU_W, conn))
                     for conn in self.offsets])
        Gv_ff = dict([(conn, self.get_weights(Gv, conn))
                      for conn in self.offsets])

        for s in range(sig_len):
            for l in range(self.n_layers):
                R_act = R_activations[l][s]

                # input from feedforward connections
                for pre in self.back_conns[l]:
                    vw, vb = v_ff[(pre, l)]
                    gn.gpu.dot(self.GPU_activations[pre][s], vw,
                               out=R_act, increment=True)
                    gn.gpu.iadd(R_act, vb)
                    gn.gpu.dot(R_activations[pre][s], W_ff[(pre, l)][0],
                               out=R_act, increment=True)

                # recurrent input
                if l in self.rec_layers:
                    if s == 0:
                        # bias input on first step
                        gn.gpu.iadd(R_act, v_recs[l][1])
                    else:
                        gn.gpu.dot(self.GPU_activations[l][s - 1],
                                   v_recs[l][0], out=R_act, increment=True)
                        gn.gpu.dot(R_activations[l][s - 1], W_recs[l][0],
                                   out=R_act, increment=True)

                if not self.layers[l].stateful:
                    if not isinstance(self.layers[l], gn.nl.Linear):
                        # note: this requires a memory allocation if
                        # d_activations is non-diagonal
                        gn.gpu.J_dot(self.GPU_d_activations[l][s], R_act,
                                     out=R_act)
                else:
                    d_input = self.GPU_d_activations[l][s][0]
                    d_state = self.GPU_d_activations[l][s][1]
                    d_output = self.GPU_d_activations[l][s][2]

                    # note: we're doing this weird thing with two R_states
                    # in order to avoid doing a copy every time
                    i = s % 2
                    gn.gpu.J_dot(d_state, R_states[l][i],
                                 out=R_states[l][1 - i])
                    gn.gpu.J_dot(d_input, R_act, out=R_states[l][1 - i],
                                 increment=True)
                    gn.gpu.J_dot(d_output, R_states[l][1 - i], out=R_act)

        # R backward pass
        if self.truncation is None:
            trunc_per = trunc_len = sig_len
        else:
            trunc_per, trunc_len = self.truncation

        R_error = self.GPU_errors
        R_deltas = self.GPU_deltas

        for n in range(trunc_per - 1, sig_len, trunc_per):
            for i in range(self.n_layers):
                R_deltas[i].fill(0)
                if R_states[i] is not None:
                    R_states[i][n % 2].fill(0)

            for s in range(n, np.maximum(n - trunc_len, -1), -1):
                for l in range(self.n_layers - 1, -1, -1):
                    if self.GPU_d2_loss[l] is not None:
                        gn.gpu.multiply(self.GPU_d2_loss[l][s],
                                        R_activations[l][s], out=R_error[l])
                    else:
                        R_error[l].fill(0)

                    # error from feedforward connections
                    for post in self.conns[l]:
                        W, _ = W_ff[(l, post)]
                        gn.gpu.dot(R_deltas[post], W, out=R_error[l],
                                   transpose_b=True, increment=True)

                        # feedforward gradient
                        W_g, b_g = Gv_ff[(l, post)]
                        gn.gpu.dot(self.GPU_activations[l][s], R_deltas[post],
                                   out=W_g, transpose_a=True, increment=True)
                        gn.gpu.sum_cols(R_deltas[post], out=b_g,
                                        increment=True)

                    # add recurrent error
                    if l in self.rec_layers:
                        gn.gpu.dot(R_deltas[l], W_recs[l][0], out=R_error[l],
                                   transpose_b=True, increment=True)

                    # compute deltas
                    if not self.layers[l].stateful:
                        gn.gpu.J_dot(self.GPU_d_activations[l][s], R_error[l],
                                     out=R_deltas[l], transpose_J=True)
                    else:
                        d_input = self.GPU_d_activations[l][s][0]
                        d_state = self.GPU_d_activations[l][s][1]
                        d_output = self.GPU_d_activations[l][s][2]

                        i = s % 2
                        gn.gpu.J_dot(d_output, R_error[l], out=R_states[l][i],
                                     increment=True, transpose_J=True)
                        gn.gpu.J_dot(d_input, R_states[l][i], out=R_deltas[l],
                                     transpose_J=True)
                        gn.gpu.J_dot(d_state, R_states[l][i],
                                     out=R_states[l][1 - i], transpose_J=True)

                    # recurrent gradient
                    if l in self.rec_layers:
                        if s > 0:
                            gn.gpu.dot(self.GPU_activations[l][s - 1],
                                       R_deltas[l], out=Gv_recs[l][0],
                                       transpose_a=True, increment=True)
                        else:
                            gn.gpu.sum_cols(R_deltas[l], out=Gv_recs[l][1],
                                            increment=True)

        # Tikhonov damping and batch mean
        Gv._axpbyz(1.0 / batch_size, GPU_v, damping, Gv)

        if isinstance(v, gpuarray.GPUArray):
            return Gv
        else:
            return Gv.get(out, pagelocked=True)

    def check_J(self, start=0, stop=None):
        """Compute the Jacobian of the network via finite differences."""

        eps = 1e-6
        N = self.W.size

        # as in check_grad, the truncation is equivalent to running the network
        # normally for the initial timesteps and then changing the parameters,
        # so that's what we do here to compute the Jacobian

        if start > 0:
            prev = self.forward(self.inputs[:, :start], self.W)
            init_a = [p[:, -1] for p in prev]
            init_s = [l.state.copy() if l.stateful else None
                      for l in self.layers]
        else:
            init_a = None
            init_s = None

        if stop is None:
            stop = self.inputs.shape[1]

        # compute the Jacobian
        J = [None for _ in self.layers]
        inc_i = np.zeros_like(self.W)
        for i in range(N):
            inc_i[i] = eps

            inc = self.forward(self.inputs[:, start:stop], self.W + inc_i,
                               init_activations=init_a, init_state=init_s)
            dec = self.forward(self.inputs[:, start:stop], self.W - inc_i,
                               init_activations=init_a, init_state=init_s)

            for l in range(self.n_layers):
                if start > 0:
                    inc[l] = np.concatenate((prev[l], inc[l]), axis=1)
                    dec[l] = np.concatenate((prev[l], dec[l]), axis=1)

                J_i = (inc[l] - dec[l]) / (2 * eps)
                if J[l] is None:
                    J[l] = J_i[..., None]
                else:
                    J[l] = np.concatenate((J[l], J_i[..., None]), axis=-1)

            inc_i[i] = 0

        return J

    def check_G(self, calc_G, v, damping=0):
        """Check Gv calculation via finite differences (for debugging)."""

        sig_len = self.inputs.shape[1]
        if self.truncation is None:
            trunc_per = trunc_len = sig_len
        else:
            trunc_per, trunc_len = self.truncation

        G = np.zeros((len(self.W), len(self.W)), dtype=self.dtype)

        for n in range(trunc_per, sig_len + 1, trunc_per):
            start = np.maximum(n - trunc_len, 0)

            # compute Jacobian
            # note that we do a full forward pass and a partial backwards
            # pass, so we only truncate the backwards J matrix
            J = self.check_J(0, n)
            trunc_J = self.check_J(start, n) if start > 0 else J

            # second derivative of loss function
            L = self.loss.d2_loss([a[:, :n] for a in self.activations],
                                  self.targets[:, :n])
            # TODO: check loss via finite differences

            G += np.sum([np.einsum("abji,abj,abjk->ik", trunc_J[l], L[l], J[l])
                         for l in range(self.n_layers) if L[l] is not None],
                        axis=0)

        # divide by batch size
        G /= self.inputs.shape[0]

        Gv = np.dot(G, v)
        Gv += damping * v

        try:
            assert np.allclose(calc_G, Gv, rtol=1e-3)
        except AssertionError:
            print("calc_G")
            print(calc_G)
            print("finite G")
            print(Gv)
            print("calc_G - finite G")
            print(calc_G - Gv)
            print("calc_G / finite G")
            print(calc_G / Gv)
            input("Paused (press enter to continue)")

    def compute_offsets(self):
        """Precompute offsets for layers in the overall parameter vector."""

        ff_offset = super(RNNet, self).compute_offsets()

        # offset for recurrent weights is end of ff weights
        offset = ff_offset
        for l in range(self.n_layers):
            if l in self.rec_layers:
                self.offsets[(l, l)] = (
                    offset,
                    offset + self.shape[l] * self.shape[l],
                    offset + (self.shape[l] + 1) * self.shape[l])
                offset += (self.shape[l] + 1) * self.shape[l]

        return offset - ff_offset

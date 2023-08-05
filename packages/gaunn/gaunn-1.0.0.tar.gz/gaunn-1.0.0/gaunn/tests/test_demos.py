import os

import pytest

import gaunn as gn
from gaunn.tests import use_GPU
from gaunn import demos


def test_standard():
    # just run through all the demos to make sure they run without crashing

    demos.xor()
    demos.crossentropy()
    demos.connections()
    demos.integrator(plots=False)
    demos.plant(plots=False)
    demos.profile("integrator", max_epochs=2)


@pytest.mark.skipif(not os.path.isfile("mnist.pkl"), reason="No MNIST dataset")
@pytest.mark.parametrize("use_GPU", use_GPU)
def test_mnist(use_GPU):
    demos.mnist(model_args={"use_GPU": use_GPU},
                run_args={"minibatch_size": 7500, "max_epochs": 1})

    demos.profile("mnist", max_epochs=1, use_GPU=use_GPU)


@pytest.mark.skipif(not gn.gpu_enabled, reason="GPU packages not installed")
def test_adding():
    demos.adding(T=10, plots=False)


if __name__ == "__main__":
    pytest.main("-x -v --tb=native test_demos.py")

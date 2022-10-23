import pytest

from psfpy.model import psf, varied_psf, PSF, VariedPSF
from psfpy.exceptions import ParameterValidationError


def test_base_equation_valid():
    func = lambda x, y: x + y
    eqn = psf(func)
    assert isinstance(eqn, PSF)
    assert eqn._parameters == set()
    assert eqn(1, 2) == 3


def test_base_equation_many_parameters():
    func = lambda x, y, sigma, mu: x + y + sigma + mu
    eqn = psf(func)
    assert isinstance(eqn, PSF)
    assert eqn._parameters == {'sigma', 'mu'}
    assert eqn(1, 2, 3, 4) == 10


def test_base_equation_missing_xy():
    func = lambda: 1
    with pytest.raises(ParameterValidationError):
        eqn = psf(func)


def test_base_equation_misordered_xy():
    func = lambda y, x: x + y
    with pytest.raises(ParameterValidationError):
        eqn = psf(func)


def test_base_equation_missing_y():
    func = lambda x, sigma: x + sigma
    with pytest.raises(ParameterValidationError):
        eqn = psf(func)


def test_base_parameterization_valid():
    ref = psf(lambda x, y, sigma: x + y)
    func = lambda x, y: {"sigma": 0.1}
    parameterization = varied_psf(ref)(func)
    assert isinstance(parameterization, VariedPSF)
    assert parameterization.parameterization_parameters == {'sigma'}
    assert parameterization(0, 0) == {"sigma": 0.1}


def test_base_parameterization_too_few_parameters_failure():
    ref = psf(lambda x, y: x + y)
    func = lambda: {'sigma': 0.1}
    with pytest.raises(ParameterValidationError):
        parameterization = varied_psf(ref)(func)


def test_base_parameterization_too_many_parameters_failure():
    ref = psf(lambda x, y: x + y)
    func = lambda x, y, c: {'sigma': 0.1}
    with pytest.raises(ParameterValidationError):
        parameterization = varied_psf(ref)(func)


def test_base_parameterization_missing_x_failure():
    ref = psf(lambda x, y: x + y)
    func = lambda c, y: {'sigma': 0.1}
    with pytest.raises(ParameterValidationError):
        parameterization = varied_psf(ref)(func)


def test_base_parameterization_missing_y_failure():
    ref = psf(lambda x, y: x + y)
    func = lambda x, c: {'sigma': 0.1}
    with pytest.raises(ParameterValidationError):
        parameterization = varied_psf(ref)(func)

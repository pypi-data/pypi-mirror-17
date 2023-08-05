import theano
import theano.tensor as T
import numpy as np

from neupy.utils import asfloat
from neupy.core.properties import ProperFractionProperty, NumberProperty
from .base import MinibatchGradientDescent


__all__ = ('Adadelta',)


class Adadelta(MinibatchGradientDescent):
    """
    Adadelta algorithm.

    Parameters
    ----------
    decay : float
        Decay rate. Value need to be between ``0`` and ``1``.
        Defaults to ``0.95``.
    epsilon : float
        Value need to be greater than ``0``. Defaults to ``1e-5``.
    {MinibatchGradientDescent.Parameters}

    Attributes
    ----------
    {MinibatchGradientDescent.Attributes}

    Methods
    -------
    {MinibatchGradientDescent.Methods}
    """
    decay = ProperFractionProperty(default=0.95)
    epsilon = NumberProperty(default=1e-5, minval=0)

    def init_layers(self):
        super(Adadelta, self).init_layers()
        for layer in self.layers:
            for parameter in layer.parameters:
                parameter_shape = T.shape(parameter).eval()
                parameter.prev_mean_squred_grad = theano.shared(
                    name="prev_mean_squred_grad_" + parameter.name,
                    value=asfloat(np.zeros(parameter_shape)),
                )
                parameter.prev_mean_squred_dx = theano.shared(
                    name="prev_mean_squred_dx_" + parameter.name,
                    value=asfloat(np.zeros(parameter_shape)),
                )

    def init_param_updates(self, layer, parameter):
        step = self.variables.step
        epsilon = self.epsilon

        gradient = T.grad(self.variables.error_func, wrt=parameter)

        prev_mean_squred_grad = parameter.prev_mean_squred_grad
        prev_mean_squred_dx = parameter.prev_mean_squred_dx

        mean_squred_grad = (
            self.decay * prev_mean_squred_grad +
            (1 - self.decay) * gradient ** 2
        )
        parameter_delta = gradient * (
            T.sqrt(prev_mean_squred_dx + epsilon) /
            T.sqrt(mean_squred_grad + epsilon)
        )
        mean_squred_dx = (
            self.decay * prev_mean_squred_dx +
            (1 - self.decay) * parameter_delta ** 2
        )

        return [
            (prev_mean_squred_grad, mean_squred_grad),
            (prev_mean_squred_dx, mean_squred_dx),
            (parameter, parameter - step * parameter_delta),
        ]

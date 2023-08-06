"""Basis functions for projecting binned spikes.

"""
from abc import ABC, abstractmethod
import numpy as np


class Basis(ABC):
    @abstractmethod
    def __init__(self, num_basis_functions: int):
        pass

    @abstractmethod
    def get_basis(self, num_timesteps: int) -> np.ndarray:
        """Returns a ndarray with shape
        (num_timesteps, num_basis_functions)

        NB: The assumption is that this matrix will be applied to hankel
        matrices, with lag decreasing across columns.

        basis vectors must have short lags at the top,
        matching the way the Hankel matrix is constructed
        """


class RaisedCosineBasis(Basis):
    """Make a nonlinearly stretched basis consisting of raised cosines.
    """

    _MIN_OFFSET = 1e-20

    def __init__(self, num_basis_functions, linearity_factor=10):
        """
        linearity_factor: offset for nonlinear stretching of x axis
                          (larger values means closer to linear spacing)
        """
        self.num_basis_functions = num_basis_functions
        self.linearity_factor = linearity_factor

    @staticmethod
    def raised_cos(center, domain, peak_spacing) -> np.ndarray:
        """Evaluates a raised cosine (which looks similar to a Gaussian
        curve) over a discrete domain given by `domain`, centered at
        `center` and with spread related to `peak_spacing`.
        """
        cos_input = np.clip((domain - center) * np.pi / peak_spacing / 2, -np.pi, np.pi)
        return (np.cos(cos_input) + 1) / 2

    def get_basis(self, num_timesteps) -> np.ndarray:
        # nonlinearity for stretching x axis
        nonlinearity = lambda x: np.log(x + self.linearity_factor + self._MIN_OFFSET)

        first_peak = nonlinearity(0)
        last_peak = nonlinearity(num_timesteps * (1 - 1.5 / self.num_basis_functions))
        peak_centers = np.linspace(first_peak, last_peak, self.num_basis_functions)
        log_domain = nonlinearity(np.arange(num_timesteps))
        peak_spacing = (last_peak - first_peak) / (self.num_basis_functions - 1)
        basis = np.column_stack(
            [self.raised_cos(c, log_domain, peak_spacing) for c in peak_centers]
        )
        basis /= np.linalg.norm(basis, axis=0)
        return basis

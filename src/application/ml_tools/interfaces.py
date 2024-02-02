import abc

import numpy as np


class AbstractImageAnalysisMLModel(abc.ABC):
    @abc.abstractmethod
    def analyze_frame(self, frame: np.ndarray):
        raise NotImplementedError

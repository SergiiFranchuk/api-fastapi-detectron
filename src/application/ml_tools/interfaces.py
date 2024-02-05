import abc

import numpy as np

from application.ml_tools.constants import ImageAnalysisOperationType


class AbstractImageAnalysisMLModel(abc.ABC):
    @abc.abstractmethod
    def analyze_frame(self, frame: np.ndarray):
        raise NotImplementedError


class AbstractMLToolFactory(abc.ABC):
    @abc.abstractmethod
    def build_model(self, analysis_type: ImageAnalysisOperationType, **kwargs):
        raise NotImplementedError

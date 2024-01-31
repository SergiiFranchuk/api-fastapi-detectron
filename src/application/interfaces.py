import abc
import numpy as np


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, **filters):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, reference, data):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference):
        raise NotImplementedError


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args, **kwargs):
        raise NotImplementedError


class AbstractImageAnalysisMLModel(abc.ABC):
    @abc.abstractmethod
    def analyze_frame(self, frame: np.ndarray):
        raise NotImplementedError

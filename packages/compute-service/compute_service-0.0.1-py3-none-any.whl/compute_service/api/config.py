from pydantic import BaseModel

from compute_service.queue.base import BaseQueue

# We use singleton for dependency injection
class APIConfig():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(APIConfig, cls).__new__(cls)
            cls.instance._input_model = None
            cls.instance._input_validator = None
            cls.instance._sessionmaker = None
            cls.instance._queue = None

        return cls.instance
    
    @property
    def input_model(self):
        return self._input_model

    @input_model.setter
    def input_model(self, input_model):
        if not isinstance(input_model, type):
            raise Exception("input_params is not a class")
        if not issubclass(input_model, BaseModel):
            raise Exception("input_params is not a subclass of pydantic.BaseModel")

        self._input_model = input_model

    @property
    def input_validator(self):
        return self._input_validator

    @input_validator.setter
    def input_validator(self, input_validator):
        if input_validator is None:
            self._input_validator = None
        elif not callable(input_validator):
            raise Exception("input_validator is not a function")
        
        self._input_validator = input_validator

    @property
    def sessionmaker(self):
        return self._sessionmaker

    @sessionmaker.setter
    def sessionmaker(self, sessionmaker):
        if not callable(sessionmaker):
            raise Exception("sessionmaker is not callable")
        self._sessionmaker = sessionmaker
    
    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, queue):
        if not issubclass(type(queue), BaseQueue):
            raise Exception("queue is not a subclass of BaseQueue")
        self._queue = queue

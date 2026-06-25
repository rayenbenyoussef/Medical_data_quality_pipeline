from  abc import ABC, abstractmethod

class BaseDBConnection(ABC):

    def __init__(self):
        self.cursor = None
        self.connection = None

    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def execute(self, query: str,params=None):
        pass
    @abstractmethod
    def fetchall(self)->list[dict]:
        pass

    @abstractmethod
    def fetchone(self)->dict:
        pass
    @abstractmethod
    def commit(self):
        pass
    @abstractmethod
    def rollback(self):
        pass
    @abstractmethod
    def close(self):
        pass

    @property
    @abstractmethod
    def placeholder(self) -> str:
        pass

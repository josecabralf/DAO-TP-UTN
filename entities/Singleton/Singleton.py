from abc import ABC

class Singleton(ABC):
  def __new__(cls):
      if not hasattr(cls, 'instance'): cls._instance = super(Singleton, cls).__new__(cls)
      return cls._instance
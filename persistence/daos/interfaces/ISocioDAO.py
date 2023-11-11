from abc import ABC, abstractmethod
from persistence.dtos.SocioDTO import SocioDTO


class ISocioDAO(ABC):
  @abstractmethod
  def create(self, socio: SocioDTO): ...
  
  @abstractmethod
  def fetchById(self, id: int) -> SocioDTO: ... 
  
  @abstractmethod
  def fetchAll(self) -> list: ...
  
  @abstractmethod
  def update(self, socio: SocioDTO): ...
  
  @abstractmethod
  def delete(self, id: int): ...
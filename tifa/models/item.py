from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tifa.models.base import Model


class Item(Model):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")

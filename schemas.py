from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Book Schemas
class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: int


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
    

# ========================================================
# Author Schemas
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class AuthorResponse(AuthorBase):
    id: int
    books: List[BookResponse] = []

    model_config = ConfigDict(from_attributes=True)
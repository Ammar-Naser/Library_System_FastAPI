from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library System API",
    description="Full CRUD for Authors and Books",
)

# =====================================================================
# Parent CRUD: Author

@app.post(
    "/authors/",
    response_model=schemas.AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authors"],
)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    new_author = models.Author(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@app.get(
    "/authors/",
    response_model=List[schemas.AuthorResponse],
    tags=["Authors"],
)
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors


@app.get(
    "/authors/{author_id}",
    response_model=schemas.AuthorResponse,
    tags=["Authors"],
)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.put(
    "/authors/{author_id}",
    response_model=schemas.AuthorResponse,
    tags=["Authors"],
)
def update_author(
    author_id: int,
    author_update: schemas.AuthorUpdate,
    db: Session = Depends(get_db),
):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    if author_update.name is not None:
        author.name = author_update.name
    if author_update.bio is not None:
        author.bio = author_update.bio

    db.commit()
    db.refresh(author)
    return author


@app.delete(
    "/authors/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Authors"],
)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()
    return None


# =====================================================================
# Child CRUD: Book

@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(
            status_code=400, detail="Book with this ISBN already exists"
        )

    new_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get(
    "/books/",
    response_model=List[schemas.BookResponse],
    tags=["Books"],
)
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


@app.get(
    "/books/{book_id}",
    response_model=schemas.BookResponse,
    tags=["Books"],
)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return None
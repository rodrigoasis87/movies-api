from typing import List
from fastapi import Path, Query, APIRouter
from fastapi.responses import JSONResponse

from src.models.movie_model import Movie, MovieCreate, MovieUpdate


movies: List[Movie] = []

movie_router = APIRouter()



@movie_router.get('/', tags=['Movies'], status_code=200, response_description="Debe devolver carga exitosa")
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@movie_router.get('/{id}', tags=['Movies'])
def get_movie_by_id(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404, response_description="ey")


@movie_router.get('/by_category', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=25)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=200)


@movie_router.post('/', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)
    #return RedirectResponse('/movies', status_code=303)


@movie_router.put('/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title == movie.title
            item.overview == movie.overview
            item.year == movie.year
            item.rating == movie.rating
            item.category == movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@movie_router.delete('/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


# @app.get('/get_file')
# def get_file():
#     return FileResponse('file.pdf')
import os

from fastapi import FastAPI, Response, status, Depends, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated


from src.routers.movie_router import movie_router
from src.utils.http_error_handler_starlette import HTTPErrorHandler


app = FastAPI()

# app.add_middleware(HTTPErrorHandler)

@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    print("Middleware is running")
    try:
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content=content, status_code=status_code)


static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('/static', StaticFiles(directory=static_path), 'static')
templates = Jinja2Templates(directory=templates_path)


@app.get('/', tags=['Home'])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome'})


# def common_params(start_date: str, end_date: str):
#     return { "start_date": start_date, "end_date": end_date}

# common_dep = Annotated[dict, Depends(common_params)]

class CommonDep:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date


@app.get('/users', tags=['Users'])
def get_users(commons: CommonDep = Depends()):
    return f"Users created between {commons['start_date']} and {commons['end_date']}"

@app.get('/customers', tags=['Customers'])
def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons['start_date']} and {commons['end_date']}"


app.include_router(prefix='/movies', router=movie_router)
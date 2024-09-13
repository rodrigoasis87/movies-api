import datetime

from pydantic import BaseModel, Field, field_validator



class Movie(BaseModel):
    id: int
    title: str  
    overview: str 
    year: int 
    rating: float 
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str 
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year, ge=1900)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=20)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': 'My movie',
                'overview': 'Trata acerca de...',
                'year': 2022,
                'rating': 5,
                'category': 'Comedia'
            }
        }
    }

    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError("Title file must have minimum 5 characters")
        if len(value) > 25:
            raise ValueError("Title file must have maximum 25 characters")
        return value
    
    #sirve mucho para mails


class MovieUpdate(BaseModel):
    title: str  
    overview: str 
    year: int 
    rating: float 
    category: str  



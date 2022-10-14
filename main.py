# Python
from typing import Optional  # para crear tipado estático
from enum import Enum
# Pydantic
from pydantic import BaseModel, Field, EmailStr  # Base Model para poder crear modelos, Field para validarlos
# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models
class HairColor(str, Enum):
    white: str = "white"
    black: str = 'black'
    brown: str = 'brown'
    red: str = 'red'
    blonde: str = 'blonde'
    tinted: str = 'tinted'


class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Jose"
    )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Sosa"
    )
    age: int = Field(
        ..., 
        gt=0,
        le=115,  # menor que 115 años
        example=31
    )
    # hair_color será opcional, en corchetes el tipo de dato que se espera, y si no existe, por defecto que sea none
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=True)
    email: EmailStr = Field(
        ...,
        title="Person Email",
        example="j.sosa@gmail.com"
    )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Jose",
    #             "last_name": "Sosa",
    #             "age": 31,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }


@app.get("/")  # path operation decorator with get method
def home():
    return {'Hello': 'World'}


# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):  # el ... indica que es obligatorio
    return person


# Validaciones: Query parameters
@app.get("/person/detail")
def show_person(
        # name es opcional, default, si no existe el name que sea None
        name: Optional[str] = Query(
            default=None, 
            min_length=1, 
            max_length=50, 
            title="Person name",
            description="This is the person name",
            example="John"
        ),
        age: int = Query(
            ..., 
            title="Person age",
            description="This is the person age",
            example=23
        )  # Los ... indican que es obligatorio, no se recomienda hacer esto, 
        # si necesitas un parametro obligatorio se recomienda hacerlo en un path parameter
):
    return {name: age}


# Validaciones: Path parameters
@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0, example=11)):
    return {person_id: "It exists"}


# Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., 
        title="Person ID", 
        description="This is the person ID",
        gt=0,
        example=11
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()  # Convertir a diccionario
    results.update(location.dict())  # agregar el otro diccionario
    return results

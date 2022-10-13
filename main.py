# Python
from typing import Optional  # para crear tipado estático
# Pydantic
from pydantic import BaseModel  # para poder crear modelos
# FastAPI
from fastapi import FastAPI, Body

app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    # hair_color será opcional, en corchetes el tipo de dato que se espera, y si no existe, por defecto que sea none
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")  # path operation decorator with get method
def home():
    return {'Hello': 'World'}


# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):  # el ... indica que es obligatorio
    return person

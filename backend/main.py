"""
This script is the main backend file for a To-Do application using FastAPI. It provides endpoints to create, read, update, and delete To-Do items stored in a MongoDB database.
The application also includes CORS middleware to allow requests from a specific frontend origin.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# import all the database functions to interact with MongoDB, calling these functions under each path operation function
from database import db_fetch_one_todo, db_fetch_all_todos, db_create_todo, db_update_todo, db_delete_todo
from model import ToDo, ToDoResponse

app = FastAPI()

origins = ["https://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/")
def index() -> dict:
    return {"message": "Hello"}

"""
Important things to note:
when retrieving data from mongoDB, it returns as dict (underlying is actually BSON). 
It needs to be converted into a pre-defined Pydantic model to be returned.
"""

@app.get("/api/todos", response_model=list[ToDo])
async def get_all_todos() -> list[ToDo]:
    """
    fetch all To_Dos from the database. Notice that we include the response_model in the path operation decorator,
    so fastapi will automatically validate and convert the response against the model.
    :return: list of To_Do objects
    """
    response = await db_fetch_all_todos()
    # # note here below is the manual way of converting using the **kwargs unpacking operator, since we have defined the response_model in the decorator, no need to do this manually.
    # if response:
    #     ans = []
    #     for each in response:
    #         ans.append(ToDo(**each))
    #     return ans

    raise HTTPException(status_code=404, detail="No todos found")

@app.get("/api/get_todo/{title}", response_model=ToDo)
async def get_todo_by_title(title: str) -> ToDo | None:
    """
    Fetch a single To_Do item by its title from the database.
    :param title: to_do title to search for
    :return: a To_Do object or None
    """
    response = await db_fetch_one_todo(title)
    if response:
        return ToDo(**response)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/api/todo", response_model=ToDoResponse)
async def create_todo(to_do: ToDo) -> dict:
    """
    This endpoint creates a new To_Do item in the database.
    :param to_do: an instance of model containing the title and description.
    :return: dictionary with a message and the created To_Do item.
    """
    response = await db_create_todo(to_do)
    if response:
        # because here we return a raw dict contains to_do model object, fastapi will automatically convert it to the ToDoResponse model.
        return {"message": "Todo created", "to_do": response}
    raise HTTPException(status_code=400, detail="Error creating to_do")

@app.put("/api/update_todo/{title}", response_model=ToDoResponse)
async def update_todo(title: str, desc: str) -> dict:
    """
    This endpoint updates an existing To_Do item in the mongodb by its title.
    :param title: title to find the To_Do item.
    :param desc: new task description.
    :return: dictionary with a message and the updated To_Do item.
    """
    response = await db_update_todo(title, desc)
    if response is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo updated successfully", "to_do": response}


@app.delete("/api/remove_todo/{title}")
async def delete_todo(title: str) -> dict:
    """
    This endpoint deletes a To_Do item from mongodb by its title.
    :param title: title to find the To_Do item.
    :return: dictionary
    """
    response = await db_delete_todo(title)
    if response is True:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found or already deleted")

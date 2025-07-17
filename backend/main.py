from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import fetch_one_todo, fetch_all_todos, create_todo, update_todo, delete_todo
from model import ToDo

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

@app.get("/api/todos", response_model=ToDo)
async def get_todos() -> list[ToDo]:
    response = await fetch_all_todos()
    return response

@app.get("/api/get_todo/{title}", response_model=ToDo)
async def get_todo_by_title(title: str) -> ToDo | None:
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/api/todo")
async def create_todo(todo: ToDo) -> dict:
    response = await create_todo(todo)
    if response:
        return {"message": "Todo created", "todo": response}
    raise HTTPException(status_code=400, detail="Error creating todo")

@app.put("/api/update_todo/{title}")
async def update_todo(title: str, desc: str) -> dict:
    response = await update_todo(title, desc)
    if response is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo updated", "updated todo is": response}


@app.delete("/api/remove_todo/{title}")
async def delete_todo(title: str) -> dict:
    # response = await delete_todo(title)
    # return response
    response = await delete_todo(title)
    if response:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

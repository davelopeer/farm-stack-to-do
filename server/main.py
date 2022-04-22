from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo
from database import (
  fetch_all_todos,
  fetch_one_todo,
  create_todo,
  update_todo,
  remove_todo
)


# App object
app = FastAPI()

origins = ['http://localhost:3000']

# Communication with frontend
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

@app.get("/")
def reat_root():
  return {"Ping": "Pong"}

@app.get("/api/todo")
async def get_todo():
  response = await fetch_all_todos()
  return response

@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_title(title):
  response = await fetch_one_todo(title)
  if response:
    return response
  raise HTTPException(status_code=404, detail=f"Todo {title} not found")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
  response = await create_todo(todo.dict())
  if response:
    return response
  raise HTTPException(status_code=400, detail=f"Bad request")

@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title: str, desc: str):
  response = await update_todo(title, desc)
  if response:
    return response
  raise HTTPException(status_code=404, detail=f"Todo {title} not found")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
  response = await remove_todo(title)
  if response:
    return "Successfully deleted!"
  raise HTTPException(status_code=404, detail=f"Todo {title} not found")

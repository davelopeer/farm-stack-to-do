from model import Todo
import asyncio

# MOngoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.TodoList
collection = database.todo

async def fetch_one_todo(title):
  document = await collection.find_one({'title': title})
  return document

async def fetch_all_todos():
  from time import time
  start = time()
  todos = []
  cursor = collection.find({})
  async for document in cursor:
    todos.append(Todo(**document))
  end = time()
  print('fetch_all_todos: %f' % (end - start))
  return {}

async def create_todo(todo):
  async def do_insert():
    result = await collection.insert_many(
        [{'title': 'nome', 'description': [{'title': f'{i}.{n}'} for n in range(40)]} for i in range(5000)])
    print('inserted %d docs' % (len(result.inserted_ids),))

  await do_insert()

  return {}

async def update_todo(title, desc):
  await collection.update_one({'title': title}, {'$set': {
    'description': desc
  }})

  document = await collection.find_one({'title': title})

  return document

async def remove_todo(title):
  # await collection.delete_one({'title': title})
  await collection.delete_many({})

  return {}
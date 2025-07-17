"""
This scripts contains all the logics for interacting with the MongoDB database. Performs CRUD operations on the "todos" collection.
"""

from model import ToDo
# motor is an asynchronous MongoDB driver for Python, built on top of pymongo. It plays nicely with FastAPI, which is also async.
import motor.motor_asyncio


'''
These 3 lines below are used to connect to the MongoDB database.
'''
# connect to the database, Creates a non-blocking connection to your local MongoDB.
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')

# Access the database named "TodoList" in MongoDB. If it doesn’t exist, MongoDB will create it.
database = client.TodoList

# Access the "todos" collection within that DB.
collection = database.todos


def todo_serializer(to_do: dict) -> dict:
    """
    This function convert a MongoDB document (which is a dictionary) into a dictionary with required key/value pairs.
    The reason for this is we have defined a Pydantic model that expects specific fields.
    And we want to return the data in a format that matches that model.
    Also, as when inserting data into MongoDB, it will automatically add an "_id" field,
    when we convert the document back to a Pydantic model for return, we need to first convert the retrieved document to a dictionary with the required fields.

    :param to_do: this is the MongoDB document retrieved to be serialized.
    :return: a dictionary with the required key/values.
    """
    return {"id": str(to_do["_id"]), "title": to_do["title"], "description": to_do["description"]}


async def db_fetch_one_todo(title: str) -> dict | None:
    """
    Fetches a single To_Do item from the MongoDB collection based on its title.
    """
    document = await collection.find_one({"title": title})
    return todo_serializer(document) if document else None


async def db_fetch_all_todos() -> list[dict | None]:
    """
    Fetches all ToDos items from the MongoDB collection, it returns a list of dictionaries or None.
    """
    todos = []
    # uses mongodb cursor to fetch all documents in the "todos" collection.
    cursor = collection.find({})
    async for document in cursor:
        todos.append(todo_serializer(document))
    return todos

async def db_create_todo(to_do: ToDo) -> dict:
    """
    when inserting data into MongoDB, it is important to convert the pydantic model object into a plain dictionary.
    so need to use model_dump() method.
    """
    # using the model_dump() method to convert the Pydantic model to a dictionary before inserting into mongoDB.
    # as mongoDB accept dictionaries/json as documents, NOT pydantic model object.
    document = to_do.model_dump()
    print(repr(document))
    # Remove the 'id' field if it exists, as MongoDB will generate its own '_id' field.
    document.pop("id", None)
    await collection.insert_one(document)
    return document

async def db_update_todo(title:str, desc:str) -> dict | None:
    """
    update a To_Do item in the MongoDB collection based on its title.
    :param title: The title of the To_Do item to update.
    :param desc: The new description for the To_Do item.
    :return: a To_Do object or None if not found.
    """
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await db_fetch_one_todo(title)
    return document

async def db_delete_todo(title: str) -> bool:
    """
    Deletes a To_Do item from the MongoDB collection based on its title.
    :param title: The title of the To_Do item to delete.
    :return: a dictionary.
    """
    result = await collection.delete_one({"title": title})
    return result.deleted_count > 0  # Returns True if a document was deleted, otherwise False.



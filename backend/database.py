from model import ToDo
# motor is an asynchronous MongoDB driver for Python, built on top of pymongo. It plays nicely with FastAPI, which is also async.
import motor.motor_asyncio

# connect to the database, Creates a non-blocking connection to your local MongoDB.
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

# Access the database named "TodoList" in MongoDB. If it doesn’t exist, MongoDB will create it.
database = client.TodoList

# Access the "todos" collection within that DB.
collection = database.todos

async def fetch_one_todo(title: str) -> ToDo | None:
    document = await collection.find_one({"title": title})
    document = ToDo(**document) if document else None
    return document

async def fetch_all_todos() -> list[ToDo]:
    """
    Fetches all ToDos items from the MongoDB collection.
    Important things here:
    - when retrieving data from mongoDB, it returns as dict (underlying is actually BSON). need to convert dict into pydantic model
    :return: list of To_Do items
    """
    todos = []
    # uses mongodb cursor to fetch all documents in the "todos" collection.
    cursor = collection.find({})
    async for document in cursor:
        # **kwargs unpacks the document dictionary into keyword arguments for the To_Do model.
        todos.append(ToDo(**document))
    return todos

async def create_todo(to_do: ToDo) -> dict:
    """
    when inserting data into MongoDB, it is important to convert the pydantic model object into a plain dictionary.
    so need to use model_dump() method.
    :param to_do:
    :return: dict
    """
    document = to_do.model_dump()
    result = await collection.insert_one(document)
    return document

async def update_todo(title:str, desc:str) -> ToDo | None:
    """
    update a To_Do item in the MongoDB collection based on its title.
    :param title: The title of the To_Do item to update.
    :param desc: The new description for the To_Do item.
    :return: a To_Do object or None if not found.
    """
    # target = await fetch_one_todo(title)
    # if target is None:
    #     return {"message": "To_do not found"}
    # else:
    #     await collection.update_one({"title": title}, {"$set": {"description": desc}})
    #     return {"message": "To_do updated", "to_do": target}
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await fetch_one_todo(title)
    return document

async def delete_todo(title: str) -> bool:
    """
    Deletes a To_Do item from the MongoDB collection based on its title.
    :param title: The title of the To_Do item to delete.
    :return: a dictionary.
    """
    # target = await fetch_one_todo(title)
    # if target is None:
    #     return {"message": "To_do not found"}
    # else:
    #     await collection.delete_one({"title": title})
    #     return {"message": "To_do deleted successfully", "removed to_do": target}

    result = await collection.delete_one({"title": title})
    return result.deleted_count > 0  # Returns True if a document was deleted, otherwise False.



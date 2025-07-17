## Things to notice:

- The use of `todo_serializer` function to avoid the issues of when returning value from the path operation function, the additional field "_id" automatically created by mongoDB.



## Why return ToDo (Pydantic model) from FastAPI path operation functions, why not just return raw dictionaries to user?

There are three key reasons, and they all serve both your backend’s reliability and your frontend’s clarity:

1: Response Validation & Serialization

when specify `function() -> Pydantic model:` or using `response_model=Pydantic model` in FastAPI route handlers, FastAPI will automatically validate the response data against the Pydantic model.
if the data does not match the model, FastAPI will raise an error and return a 422 Unprocessable Entity response to the client.

- this validates the return value before sending back to the client.

2: Automatic OpenAPI (swagger UI) Documentation

By returning a Pydantic model, fastapi auto-generates interactive API docs with **schema validation**, **sample request/response bodies**.

3: Better code readability and maintainability


Remember fastapi will automatically validate and convert the return value to the specified Pydantic model. As long as the data structures and types match the Pydantic model, FastAPI will handle it correctly.
If not, it will return a 422 Unprocessable Entity error.

These two are equivalent:

```python
@app.get("/api/todos")
async def get_all_todos() -> list[ToDo]:
    response = await db_fetch_all_todos()
    if response:
        ans = []
        for each in response:
            ans.append(ToDo(**each))
        return ans
    
    raise HTTPException(status_code=404, detail="No todos found")
```    
```python
@app.get("/api/todos", response_model=list[ToDo])
async def get_all_todos() -> list[ToDo]:
    response = await db_fetch_all_todos()
    if response:
        return response
    raise HTTPException(status_code=404, detail="No todos found")
    
```


## If mongoDB accepting dictionary, why not just using dictionary as the parameter's datatype in the functions of database.py instead of Pydantic model?

for example: `async def create_todo(todo: dict[str])`, since mongoDB accepts dictionary, why not just use dictionary as the parameter's datatype in the functions of database.py instead of Pydantic model?

(Please note the code above works, but it is not recommended)

1: Data Validation and structure Enforcement

Pydantic models enforce a specific structure and datatypes for the input data. 
This ensures that the data being passed to the database functions is valid, this prevents the invalid data even before reach to schema, so invalid data will not be able to enter database. 
If you use a dictionary, you lose this validation, which can lead to runtime errors or unexpected behavior.

2: Code Clarity and Documentation

e.g: `async def create_todo(todo: ToDo)`, instantly know the fields and types expected in the `todo` parameter.

Pydantic models serve as clear documentation for the expected data structure. 
When you use a Pydantic model, it is immediately clear what fields are required, their types, and any validation rules.

3: Easy Data Conversion and Integration

- using `.model_dump()` method, you can easily convert the Pydantic model to a dictionary or JSON format when needed.
- Or using the **kwargs unpacking with the pydantic model: `{pydantic_model_name}(**document)` to convert the dictionary to a Pydantic model.

### So just remember, using pydantic model to validate the data, before doing db operations, we convert the pydantic model to a dictionary using `.model_dump()` method
### When returning data, use `response_model =` and `-> intended_type:` in path operator decorator and functions to convert the dictionary to a Pydantic model automatically.
### OR using **kwargs unpacking with the pydantic model: `{pydantic_model_name}(**document)` to convert the dictionary to a Pydantic model.
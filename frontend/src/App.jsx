import React, { useState, useEffect } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import ToDoItem from './components/ToDo.jsx'




function App() {
    const [todoList, setTodoList] = useState([{}]);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");

    // use useEffect to fetch all the todos from the backend
    const fetchTodos = async() => {
        try {
            const response = await axios.get("http://localhost:8000/api/todos")
            console.log(response);
            setTodoList(response.data);
        } catch (error) {
            console.error("Error fetching todos:", error);
        }
    }

    // event handler function to add a new to_do
    const addTaskHandler = async() => {
        if (title === "" || description === "") {
            alert("Please fill in both title and description before adding.");
            return;
        }
        try {
            const response = await axios.post("http://localhost:8000/api/todo", {
                "title": title.trim(),
                "description": description.trim()
            })
            console.log(response);
            // Clear the input fields after adding the task
            setTitle("");
            setDescription("")
            // re-fetch the todos to update the list
            fetchTodos();
        } catch (error) {
            console.error("Error adding task:", error);}
    }

    // event handler function to update an existing to_do
    const updateTaskHandler = async() => {
        if (title === "" || description === "") {
            alert("Please fill in both title and description before adding.");
            return;
        }
        try {
            const response = await axios.put("http://localhost:8000/api/update_todo", {
                "title": title.trim(),
                "description": description.trim()
            });
            console.log(response)
            // Clear the input fields after adding the task
            setTitle("");
            setDescription("")
            // re-fetch the todos to update the list
            fetchTodos();
        } catch (error) {
            console.error("Error updating task:", error);
        }
    }

    // useEffect to fetch todos when the component mounts
    useEffect(
        () => {
            fetchTodos();
        }, []
    )

  return (
    <main className="App">
        <>
        <div className="App list-group-item justify-content-center align-items-center mx-auto"
         style={{"width":"800px", "backgroundColor":"white", "marginTop":"20px"}}>
            <h1 className="card text-white bg-primary mb-1">
                Task Manager
            </h1>
            <h6 className="card text-white bg-secondary mb-3">
                Fastapi + React + MongoDB
            </h6>
            <div className="card-body">
                <h5 className="card text-white bg-info mb-3">
                    Add Your Tasks Here
                </h5>
                <span className="card-text">
                    <input className="mb-2 form-control titleIn" placeholder="Task Title..." value = {title}
                    onChange={(e) => {return setTitle(e.target.value)}}/>
                    <textarea className="mb-2 form-control descriptionIn" placeholder="Task Description..." value={description}
                    onChange = {(e) => {return setDescription(e.target.value)}}></textarea>
                    <button className="btn btn-outline-success addTaskBtn mx-2 mb-lg-4" style={{"borderRadius":"50px", "fontWeight":"bold"}}
                    onClick={addTaskHandler}>
                        Add Task
                    </button>
                    <br/>
                    <button className="btn btn-outline-warning mx-2 mb-lg-4" style={{"borderRadius":"50px", "fontWeight":"bold"}}
                    onClick={updateTaskHandler}>
                        Update Task
                    </button>
                </span>
                <h5 className="card text-white bg-secondary mb-3">Your Tasks</h5>
                <div>
                    {/*{here we place the component cards}*/}
                    <ol>
                        {todoList.map((todo, index) => {
                            return (
                                <li key={index}>
                                    <ToDoItem todo={todo} fetchTodos={fetchTodos}/>
                                </li>
                            )
                        })}
                    </ol>
                </div>
            </div>
        </div>
        </>
    </main>
  )
}

export default App

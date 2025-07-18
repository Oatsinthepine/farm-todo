import axios from 'axios';
import React from 'react';

// This component represents a single To_Do item, which this component will be displayed
// in the list of To_Dos, using todoList.map() function to assign each individual to_do as this ToDoItem.

export default function ToDoItem(props) {
    // Destructure the to_do and fetchTodos from props
    const {todo, fetchTodos} = props;
    const deleteTaskHandler = async (title) => {
        try {
            const response = await axios.delete(`http://localhost:8000/api/remove_todo/${title}`);
            console.log("Task deleted successfully:", response.data);
            // re-fetch the todos to update the list
            fetchTodos();
        } catch (error) {
            alert("Error deleting task. Please try again.");
            console.error("Error deleting task:", error);
        }
    };

    return (
        <div className="card mb-3">
            <div className="card-body">
                <h5 className="card-title">{todo.title}</h5>
                <p className="card-text">{todo.description}</p>
                <button className="btn btn-danger" onClick={() => deleteTaskHandler(todo.title)}>
                    Delete Task
                </button>
            </div>
        </div>
    );
}
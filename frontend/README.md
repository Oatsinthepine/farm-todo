# Frontend (React-js + Vite)

This is the frontend part of the project, built using React.js and Vite.

## Frontend Logic & Backend Interaction Notes

### State Management:

The main state variables in App.jsx are todoList, title, and description.
todoList holds the list of all to-dos fetched from the backend.
title and description are controlled inputs for adding/updating tasks.

### Fetching Data:

On component mount, fetchTodos() is called (inside useEffect) to load all to-dos from the backend (GET /api/todos).
After adding, updating, or deleting a task, fetchTodos() is called again to refresh the list.

### Adding a Task:

addTaskHandler() sends a POST request to /api/todo with the current title and description.
On success, input fields are cleared and the list is refreshed.

### Updating a Task:

updateTaskHandler() sends a PUT request to /api/update_todo with the user input current title and description within the `<input>` and `<textarea>` field.
On success, input fields are cleared and the list is refreshed.
Note: The update is based on the title field, so titles must be unique.

### Deleting a Task:

Each ToDoItem component has a delete button that calls deleteTaskHandler(title), which sends a DELETE request to /api/remove_todo/{title}.
On success, the list is refreshed.

### Component Structure:

App.jsx manages the main logic and renders the list of tasks.
ToDoItem (in components/ToDo.jsx) represents a single task and handles its own delete action.

###Controlled Inputs:

Both `<input>` and `<textarea>` are controlled by React state (value and onChange), ensuring they reset after actions.


### CORS:

The backend allows requests from http://localhost:5173 (the Vite dev server). **Please note that we have to use `http`, NOT `https`, as the backend is running on port 8000 without SSL.**


### Building and running your application

we can build the frontend image using:
`docker build -t todo_frontend .`.
This creates a Docker image named `todo_frontend` based on the Dockerfile in the current directory.

Then to view the application, we can run the image using:
`docker run -p 80:80 todo_frontend`.
Your application will be available at http://localhost:80.


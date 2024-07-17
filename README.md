# Flask Server with Docker

## Description

This project is a simple Flask web server that provides three endpoints:
- `/ls?<path>`: Returns the output of the `ls -lh` command for the specified directory.
- `/cat?<path>`: Returns the content of the specified file.
- `/json/<command>?<path>`: Returns the output of the specified command (`ls` or `cat`) in JSON format.

## Requirements

- Docker
- Git

## Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/natanmelamed/FlaskServer
    cd FlaskServer
    ```

2. Build the Docker image:

    ```bash
    docker build -t flask-server .
    ```

3. Run the Docker container:

    ```bash
    docker run -d -p 5000:5000 -e PORT=5000 flask-server
    ```

4. Access the server:

    Open your web browser and go to `http://localhost:5000`.

## Endpoints

- `/ls?<path>`: Example: `http://localhost:5000/ls?path=/some/directory`
- `/cat?<path>`: Example: `http://localhost:5000/cat?path=/some/file.txt`
- `/json/<command>?<path>`: Example: `http://localhost:5000/json/ls?path=/some/directory`

## Notes

- Ensure that the specified paths exist within the Docker container's file system.

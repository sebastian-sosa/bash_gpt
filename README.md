# BashGPT

BashGPT is a Python application that uses OpenAI's GPT-4 model to generate and execute bash commands in the local machine to answer user's questions. It provides an interactive command-line interface for users to interact with the GPT-4 model:

```
$ make run
docker run -it -p 4000:80 bash_gpt
User: what is the path of the working directory?
GPT4 Agent:
<bash>pwd</bash>
Press enter to execute `pwd`, any other key to abort:
Command output: /app

GPT4 Agent:
The path of the working directory is `/app`.
The path of the working directory is `/app`.

```

As a safety precaution, the program is run within a Docker container and user's confirmation is asked before executing any command. However, you should note that even if the app is run inside a Docker container, commands could potentially be executed in the host machine (for example if Docker container is run with certain privileges, or volumes from the host machine are mounted into the container).


## Prerequisites

- Docker
- An OpenAI API key


## Setup

1. Clone the repository to your local machine.

2. Create a .env file in the root directory of the project and add your OpenAI API key.

## Running the Application

The application can be run using Docker.

To build the Docker image, run:

```
make build
```


To run the application in a Docker container, use:

```
make run
```

## Testing

Tests are written using pytest. To run the tests in a Docker container, use:  

```
make test
```

## Example usage

See `/conversations` for sample conversations.

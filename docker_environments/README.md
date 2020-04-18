# mssql-cli Dockerfiles
mssql-cli supports a variety of Docker environments.

## Dockerfile Examples
The [prod](https://github.com/dbcli/mssql-cli/tree/master/docker_environments/prod/) folder contains example Dockerfiles for each supported Linux distribution.

## Testing Docker Environments
mssql-cli provides automated scripts for quickly building and running Docker containers for each supported Linux distribution. The automation works by:
1. Running an initial script to build Docker containers for each Dockerfile in a specified folder.
2. Running a secondary script to interactively run each built container with mssql-cli pre-installed. Exiting the container will automatically run the next Docker container.

### Requirements

#### Docker Desktop
Install Docker Desktop from the [Docker website](https://www.docker.com/products/docker-desktop).

#### RedHat Registry Login
A RedHat login must be created and registered with Dcoker to test RHEL builds:
1. Go to https://www.redhat.com/ -> Register an account.
2. In the Docker CLI: call `docker login registry.redhat.io` and log in with your credentials.
https://access.redhat.com/RegistryAuthentication

### Build Testing Environments

#### Set Environment Variables
Set RedHat username and password!

#### Build Docker Images
From the `docker_environments` folder, run:
```sh
./build_containers.sh $(pwd) <folder-name> --no-cache
```

To use cached containers, remove the `--no-cache` argument.

#### Run Docker Images
From the `docker_environments` folder, run:
```sh
./run_containers.sh $(pwd) <folder-name>
```

This will automatically run each built container in an interactive console. Simply call `mssql-cli` to test the installation.

When you're done, exit mssql-cli and type `exit` to move on to the next container.

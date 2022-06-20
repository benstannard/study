# [Compose specification](https://docs.docker.com/compose/compose-file/)

The `Compose` file is a `YAML` file Docker application defining:
+ **services** computing components of an application are defined as `Services`
+ **networks** services communicate with each other `Networks`
+ **volumes** services store and share persistent data into `Volumes`
+ **configs** some services require configuration data that is dependent on the runtime or platform.
+ **secrets** is a specific flavor of configuration data for sensitive data that SHOULD NOT be exposed without security considerations.

A **`Project`** is an individual deployment of an application specification on the platform. A project's name is used to group resources together and isolate them from other applications or other installion of the same Compose specified application with distinct parameters. A projects name ce be set **explicity** by top-level `name` attribute. Compose implementation **MUST** offer a way for user to set a custom project name and override this name, so that the same `compose.yml` file can be deployed twice on the same infrastructure, without changes, by just passing a distinct name.

## Overview

`Compose` is a tool for defining and running multi-continer Docker applications. With `Compose` you use a YAML file to configure your appication's services. Then, with a single command, you create and start all the services from your configuration. See full list of [features](https://docs.docker.com/compose/#features).  

`Compose` works in all environments: production, staging, development, testing, as well as CI workflows.  

Using `Compose` is basically a **three-step** process:
1. Define your app's environment with a `Dockerfile` so it can reproduced anywhere.
2. Define the services that make up your app in `docker-compose.yml` so they can be run together in an isolated environment.
3. Run `docker compose up` command which starts and runs your entire app. You can alternatively run `docker-compose up` binary.

## Illustrative Example

Examples of a `docker-compose.yml` file:  
```
version: "3.9"  # optional since v1.27.0
services:
  web:
    build: .
    ports:
      - "8000:5000"
    volumes:
      - .:/code
      - logvolume01:/var/log
    links:
      - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```
The example application is composed of the following parts:
+ 2 services, backed by Docker images: webapp and database
+ 1 secret (HTTPS certificate), injected into the frontend
+ 1 configuration (HTTP), injected into the frontend
+ 1 persistent volume, attached to the backend
+ 2 networks
```
version: "3.9"
services:
  frontend:
    image: awesome/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate

  backend:
    image: awesome/database
    volumes:
      - db-data:/etc/data
    networks:
      - back-tier

volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"

configs:
  httpd-config:
    external: true

secrets:
  server-certificate:
    external: true

networks:
  # The presence of these objects is sufficient to define them
  front-tier: {}
  back-tier: {}
```

## Services top-level element

A `Compose` file **MUST** declare a `services` root element as a map whose key are string representations of service names, and whose values are service definitions. A service definition contains the configuration that is applied to each container started for that service.  

Each service **MAY** also include a `build` section which defines how to create the Docker image for the service.  

A **Service** is/are:
+ an abstract definition of computing resource within an application which can be scaled/replaced independently or from other components.
+ Services are backed by a set of containers, run by the platform according to replication requirements and placement constraints.
+ Defined by a Docker image and set of runtime arguments.

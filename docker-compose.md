# [Compose specification] (https://docs.docker.com/compose/compose-file/)

The `Compose` file is a `YAML` file Docker application defining:
+ **services** computing components of an application are defined as `Services`
+ **networks** services communicate with each other `Networks`
+ **volumes** services store and share persistent data into `Volumes`
+ **configs** some services require configuration data that is dependent on the runtime or platform.
+ **secrets** is a specific flavor of configuration data for sensitive data that SHOULD NOT be exposed without security considerations.

A **`Project`** is an individual deployment of an application specification on the platform. A project's name is used to group resources together and isolate them from other applications or other installion of the same Compose specified application with distinct parameters. A projects name ce be set **explicity** by top-level `name` attribute. Compose implementation **MUST** offer a way for user to set a custom project name and override this name, so that the same `compose.yml` file can be deployed twice on the same infrastructure, without changes, by just passing a distinct name.

## Illustrative Example

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

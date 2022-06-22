# [Dockerfile](https://docs.docker.com/engine/reference/builder/)

```
# syntax=docker/dockerfile:1
FROM node:12-apline
RUN apk add --no-cache python2 g++ make
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
````
See also [Best Practices Guide](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)  

Docker can build images automatically by reading the instructions in a `Dockerfile`. A `Dockerfile` is just a text document that contains all the commands a user could call on the command line to assemable an image. Using `docker build` users can create automated build that executes several command-line instructions.

## What is a container?

A container is a sandboxed process (`/proc` has info on running processes, pseudo filesystem) on your machine that is isolated from all other processes on the host machine leveraging `kernal namespaces`, `cgroups` and changing the root `chroot`. It is a runnable instance of an image. It's portable, can be run on any **OS**. Containers are isolated from each other and run their own software, binaries, and configurations.  

**Namespaces**  
Limit what you can see, restricts the view of processes on the host machine. Created with syscalls, using clone flags. Unix Timesharing System, Process IDs, Mounts, Network, User IDs, InterProcess Comms.  

## [Docker run reference](https://docs.docker.com/engine/reference/run/)
```
docker run --detach -d --port -p 80:80 docker/getting-started
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]         **must specify an IMAGE**
```

Docker runs processes in isolated containers. A container is a process which runs on a host. The host may be local or remote. When you execute `docker run`, the container process that runs is isolated in that it has its own file system, its own networking, and its own isolated process tree seperate from the host.  

`docker run` command must specify an **IMAGE** to derive the container from. An image developer can define defaults related to:
+ detached or foreground running
+ container identification
+ network settings
+ runtime constraints on CPU and memory

`docker run` has more `[OPTIONS]` than any other command to allow the operator to override nearly all defaults.

### Detached (-d)

To start a container in detached mode, use just -d option. By design, these containers exits when the root process used to run the container exists, unless you also specify the `--rm` option. If you use with `-d` with `--rm`, the container is removed when it exits or when the daemon exits, whichever happens first.

### Foreground

For **interactive processes** like a shell, you **MUST** use `-i` `-t` together in order to allocate a tty for the container process, it is often written as `-it`

In foreground mode (the default when `-d` is not specified), `docker run` cat start the process in the containier and attach the console to the prcess's standing input, ouput, and standard error. It can even pretend to be a TTY and pass along signals. All of those configurable:
+ `-t` Allocate a pseudo-tty
+ `-i` Keep STDIN open even if not attached
+ `-a=[]` Attach to `STDIN`, `STDOUT`, and/or `STDERR` **if you do not specify**, then Docker will attached both stdout, stderr
+ `--sig-proxy=true` Proxy all recieved signals to the process (non-TTY mode only)

### Name (--name)

The operation can identify a container in three ways:
+ UUID Long ID
+ UUID Short ID
+ Name i.e. "evil_ptolemy" if you do not assign a contain name with `--name` option, it autogen by daemon

### Image[:tag]

`docker run ubuntu:14.04`

### PID settings (--pid)

By default, all containers have PID namespaces enables. PID namespaces provide separation of processes. The PID Namespace removes the view of the system processes, and allows the process ids to be reused include pid 1. In certain cases you want your contaners to share the host's process namespace, basically allowing processes within the container to see all of the processes on the system. For example:

```
FROM alpine:latest
RUN apk add --update htop && rm -rf /var/cache/apk/*
CMD ["htop"]
```
```
docker build -t mytop .
docker run --it --rm --pid=host myhtop
```

### Network settings

By default, all containers have networking enable and they can make any outgoing connections. The operator can complete disable networking with `docker run --network none` which would disable all incoming and outgoing networking. In cases like this, you would perform I/O through files `STDIN` and `STDOUT` only.  

Publishing ports and linking to other containers only works with the default (bridge). The **linking feature is a legacy feature**. You should always perfer using Docker network drivers over linking.  

Your container will use the same DNS servers as the host by default, but you can override this with `--dns`.  

### Clean up (--rm)

By default a container's file system persists even after the container exits. This makes debugging a lot easier, since you can inspect the final state, and you retain all of your data by default. But if you are running short-term **foreground** processes, these container file systems can really pile up. If instead, you'd like Docker to **automatically clean up the container and remove the file system when the container exits**, you can add the `--rm` flag.  



## [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
see [best practices guide](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### Usage

Note that each instruction is run independently, so `RUN cd /tmp` will not have any effect on the next instructions.  

`docker build` command builds an image from a `Dockerfile` and a context. The build's context is the set of files at a specified location `PATH` or `URL`. The `PATH` is a directory on your local filesystems. The `URL` is a Git respoitory location.  

The build context is processed recursively. So a `PATH` includes any subdirectories and the `URL` includes the repository and it submodules.  

`docker build .` uses current directory as build context. The build is run by the Docker **daemon**, not the CLI. It's *best* to start with an empty directory as context and keep your Dockerfile in that directory. Add only the files needed for building the Dockerfile.  

`docker build -t benstan/myapp .` You can specify a repository and a tag at which to save the new image if the build succeeds.  

Before the Docker daemon runs the instructions in the `Dockerfile`, it performs a preliminary validation of the `Dockerfile`. If correct, the daemon runs the instructions in the `Dockerfile` one-by-one, committing the results of each instruction to a new image if neccessary, before finally outputting the **ID** of your new image. Whenever possible, Docker uses a build-cache to accelerate the `docker build` process significantly.  

When you're done with your build, look into scanning your image with `docker scan`.  

Docker supports new backend for executing builds. See [BuildKit](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/syntax.md)

### Format

A `Dockerfile` **must begin with a `FROM` instruction.** The `FROM` instruction specifices the *Parent Image* from which you are building.

Here is the format for a `Dockerfile`:
```
# Comment
INSTRUCTION arguments
```

### Parse Directives & escape

Parser directives are optional, and affect the way in which subsequent lines are handled.  **escape** default characer is `\`.

### Environment replacements

Environemnt variables (declared with the `ENV` statement) can also be used in certain instruction as variables to be interpreted by the `Dockerfile`. Environment variables are noted either with `$variable_name` or `${variable_name`}.
```
FROM busybox
ENV FOO=/bar
WORKDIR ${FOO}  # Workdir /bar
```

### FROM

The `FROM` instruction initializes a new build stage and sets the *Base Image* for subsequent instructions. A valid `Dockerfile` must start with a `FROM` instruction. It's easy to start by **pulling an image** from *Public Repositories*.   

`FROM` instructions support variables that are declared by any `ARG` instruction that occur before the first `FROM`.
```
ARG CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD /code/run-app
```

An `ARG` declared before a `FROM` is outside of a build stage, so it can't be used in any instruction after a `FROM`.

### RUN

**RUN** has 2 forms: *shell* and *exec*, *exec* makes it possible to avoid shell string munging.
```
RUN <command>` (*shell* form)
RUN ["executable", "param1", "param2"]` **must** use double quotes, is parsed as a JSON array.
RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'
RUN ["sh", "-c", "echo $HOME"]
```
The `RUN` instruction will execute any commands in a new layer on top of the current image and commit the results. The resulting committed image will be used for the next step in the `Dockerfile`.  

Laying `RUN` instruction and generating commits conforms to the core concepts of Docker where commits are cheap and containers can be created from any point in a image's history, must like source control.  

### CMD

**The main purpose of a CMD is to provide defaults for an executing container** and there can only be **ONE** `CMD` instruction in a `Dockerfile`. These defaults can include an executable, or the can omit the executable, in which case you must specify an `ENTRYPOINT` instruction as well. Unlike the *shell* form, the exec does not invoke a command shell. This means that normal shell processing does not happen. If you want shel processing then either use the *shell* form or execute a shell directy for example: `CMD ["sh", "-c", "echo $HOME"]`.  

**CMD** instruction has three forms: *exec*, *default*, *shell*  
`CMD ["executable", "param1", "param2"]` (*exec* form is preferred form)  

#### RUN vs CMD

Do not confuse `RUN` with `CMD`. `RUN` actually runs a command and commits the result; `CMD` does not execute anything at build time, but specifies the intended command for the image.

### LABEL

The `LABEL` instruction adds metadata to an image. A `LABEL` is a key-value pair.
```
LABEL version="1.0"
LABEL description="This text illustrates"
```

### EXPOSE

The `EXPOSE` instruction informs Docker that the container listens on the specified network port at runtime. TCP is default if not specified. The `EXPOSE` instruction does not actually publish the port. It functions as a type of documentaion between the persone who builds the image and the person who runs the container, about which ports are intended to be published.  

To *actually* publish the pork when running the container, use the `-p` flag on `docker run -p 80:80`  
`EXPOSE <port> [<port>/<protocol>...]`  

`docker network` command supports creating networks for communication amoung containers without the need to publish specific ports, because the containers connected to the network can communication with each other over any port.

### ENV

```
ENV <key>=<value>` ...
ENV MY_DOG="John Doe"
```

The `ENV` instruction sets the environment variable <key> to the value <value>. This value will be interpreted for other environment variables. Variables set using `ENV` will persist when a contain is run from the resulting image. You can view the values using `docker inspect`, and changing them using `docker run --env <key>=<value>`. If an environment variable is only needed during build, and not in the the final image, consider setting a value for a single command instead or using `ARG` which is not persisted in the final image.

### ADD

**FYI** *`COPY` is `ADD` without the tar and remote URL handling.* Best practices suggests using `COPY` where the magic of `ADD` is not required.  

The ADD instruction copies new files, directories or remote file URLs from <src> and adds them to the filesystem of the image at the path <dest>. Multiple <src> resources may be specified but if they are files or directories, their paths are interpreted as relative to the source of the context of the build.  

ADD has two forms:
```
ADD [--chown=<user>:<group>] <src>... <dest>
ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]
ADD test.txt <WORKDIR>/relativeDir/
```

`ADD` obeys the following rules:
+ The <src> path must be inside the context of the build; you cannot ADD ../something /something, because the first step of a docker build is to send the context directory (and subdirectories) to the docker daemon.
+ If <src> is a URL and <dest> does not end with a trailing slash, then a file is downloaded from the URL and copied to <dest>.
+ If <src> is a URL and <dest> does end with a trailing slash, then the filename is inferred from the URL and the file is downloaded to <dest>/<filename>. For instance, ADD http://example.com/foobar / would create the file /foobar. The URL must have a nontrivial path so that an appropriate filename can be discovered in this case (http://example.com will not work).
+ If <src> is a directory, the entire contents of the directory are copied, including filesystem metadata.

### COPY

The `COPY` instruction copies new files or directories from <src> and adds them to the filesystem of the container at the path <dest>.  
```
COPY <src>... <dest>
COPY test.txt relativeDir/
```

### ENTRYPOINT

An `ENTRYPOINT` allows you to configure a container that will run as an executable. For example 

The *exec* form, is preferred form:  
`ENTRYPOINT ["executable", "param1", "param2"]`

### VOLUME

The `VOLUME` instruction creates a mount point with the specified name and marks it as holding extranlly mounted volunes from native host or other containers.  
`VOLUME ["/data"]

### WORKDIR

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, `ADD` instructions that follow it in the `Dockerfile`. The `WORKDIR` instructions can be used **multiple** times in a `Dockerfile`.
```
WORKDIR /path/to/workdir
```

### ARG

The `ARG` instruction defines a variable that users can pass at build-time to the builder with `docker build` command using the `--build-arg <varname>=<value>`.  

## [Volumes](https://docs.docker.com/storage/volumes/)

Volumes are the preferred mechanism for persisting data generated by and used by Docker containers. While bind mounts are dependant on the directory structure and OS of the host machine, **volumes are completely managed by Docker**. Volumes use `rprivate` bind propagation.  Advantages of volumes over bind mounts:
+ Volumes are easier to backup or migrate than bind mounts
+ You can manage volumes using Docker CLI commands or Docker API
+ Works on both Linux and Windows
+ Volumes can be shared more safely amoung multiple containers
+ Volume drivers let you store volumes on remote hosts or cloud providers, to encrypt or add functionality
+ New volumes can have their content pre-populated by a container

```
docker volume create my-vol
docker volume ls
docker volume inspect my-vol
docker volume rm my-vol
```

## Choose the -v or --mount flag

In general, --mount is more explicit and verbose. The **biggest difference** is that the `-v` syntax combines all the options together in one field, while the `--mount` syntax separates them. When using volumes with services, **only** `--mount` is supported.

## Start a container with a volume

If you start a container with a volume that does not yet exist, Docker **creates the volume for you**
















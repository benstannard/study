# [Dockerfile](https://docs.docker.com/engine/reference/builder/)

See also [Best Practices Guide](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)  
Docker can build images automatically by reading the instructions in a `Dockerfile`. A `Dockerfile` is just a text document that contains all the commands a user could call on the command line to assemable an image. Using `docker build` users can create automated build that executes several command-line instructions.

### Usage

`docker build` command builds an image from a `Dockerfile` and a context. The build's context is the set of files at a specified location `PATH` or `URL`. The `PATH` is a directory on your local filesystems. The `URL` is a Git respoitory location.  

The build context is processed recursively. So a `PATH` includes any subdirectories and the `URL` includes the repository and it submodules.  

`docker build .` uses current directory as build context. The build is run by the Docker **daemon**, not the CLI. It's *best* to start with an empty directory as context and keep your Dockerfile in that directory. Add only the files needed for building the Dockerfile.  

To use a file in the build context, the `Dockerfile` referst to the file specified in an instruction, for example a `COPY` instruction.  

`docker build -t benstan/myapp .` You can specify a repository and a tag at which to save the new image if the build succeeds.  

Before the Docker daemon runs the instructions in the `Dockerfile`, it performs a preliminary validation of the `Dockerfile`. If correct, the daemon runs the instructions in the `Dockerfile` one-by-one, committing the results of each instruction to a new image if neccessary, before finally outputting the **ID** of your new image. Whenever possible, Docker uses a build-cache to accelerate the `docker build` process significantly.  

Docker supports new backend for executing builds. See [BuildKit](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/syntax.md)  

### Format

A `Dockerfile` **must begin with a `FROM` instruction.** The `FROM` instruction specifices the *Parent Image* from which you are building.

Here is the format for a `Dockerfile`:  
`# Comment`  
`INSTRUCTION arguments`  

### Parse Directives & escape

Parser directives are optional, and affect the way in which subsequent lines are handled.  **escape** default characer is `\`.  

### Environment replacements

Environemnt variables (declared with the `ENV` statement) can also be used in certain instruction as variables to be interpreted by the `Dockerfile`. Environment variables are noted either with `$variable_name` or `${variable_name`}  
`FROM busybox`  
`ENV FOO=/bar`  
`WORKDIR ${FOO}`  # Workdir /bar  

### FROM

The `FROM` instruction initializes a new build stge and sets the *Base Image* for subsequent instructions. `Dockerfile` must start by **pulling an image** and it's easy from *Public Repositories*.
`ARG VERSION=latest`  
`FROM busybox:${VERSION}`  

### RUN

**RUN** has 2 forms: *shell* and *exec*
`RUN <command>` (*shell* form)  
`RUN ["executable", "param1", "param2"]` **must** use double quotes, is parsed as a JSON array.  
`RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'  
`RUN ["sh", "-c", "echo $HOME"]  
The `RUN` instruction will execute any commands in a new layer on top of the current image and commit the results.  

### CMD

**The main purpose of a CMD is to provide defaults for an executing container** and there can only be **ONE** `CMD` instruction in a `Dockerfile`. These defaults can include an executable, or the can omit the executable, in which case you must specify an `ENTRYPOINT` instruction as well. Unlike the *shell* form, the exec does not invoke a command shell. This means that normal shell processing does not happen. If you want shel processing then either use the *shell* form or execute a shell directy for example: `CMD ["sh", "-c", "echo $HOME"]`.  

**CMD** instruction has three forms: *exec*, *default*, *shell*  
`CMD ["executable", "param1", "param2"]` (*exec* form is preferred form)  

### RUN vs CMD

Do not confuse `RUN` with `CMD`. `RUN` actually runs a command and commits the result; `CMD` does not execute anything at build time, but specifies the intended command for the image.  

### LABEL

The `LABEL` instruction adds metadata to an image. A `LABEL` is a key-value pair.  
`LABEL version="1.0"`  
`LABEL description="This text illustrates"  

### Expose

The `EXPOSE` instruction informs Docker that the container listens on the specified network port at runtime. TCP is default if not specified. The `EXPOSE` instruction does not actually publish the port. It functions as a type of documentaion between the persone who builds the image and the person who runs the container, about which ports are intended to be published.  

To *actually* publish the pork when running the container, use the `-p` flag on `docker run -p 80:80`  
`EXPOSE <port> [<port>/<protocol>...]`  

`docker network` command supports creating networks for communication amoung containers without the need to publish specific ports, because the containers connected to the network can communication with each other over any port.  

### ENV

`ENV <key>=<value>` ...  
`ENV MY_DOG="John Doe"`

The `ENV` instruction sets the environment variable <key> to the value <value>. This value will be interpreted for other environment variables. Variables set using `ENV` will persist when a contain is run from the resulting image. You can view the values using `docker inspect`, and changing them using `docker run --env <key>=<value>`. If an environment variable is only needed during build, and not in the the final image, consider setting a value for a single command instead or using `ARG` which is not persisted in the final image.
`RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y ...` -or-  
`ARG DEBIAN_FRONTEND=noninteractive`  
`RUN apt-get update && apt-get install -y ...`  

### ADD

The ADD instruction copies new files, directories or remote file URLs from <src> and adds them to the filesystem of the image at the path <dest>. Multiple <src> resources may be specified but if they are files or directories, their paths are interpreted as relative to the source of the context of the build.

ADD has two forms:  
`ADD [--chown=<user>:<group>] <src>... <dest>`  
`ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]`  
`ADD test.txt <WORKDIR>/relativeDir/`  

`ADD` obeys the following rules:  
- The <src> path must be inside the context of the build; you cannot ADD ../something /something, because the first step of a docker build is to send the context directory (and subdirectories) to the docker daemon.  

- If <src> is a URL and <dest> does not end with a trailing slash, then a file is downloaded from the URL and copied to <dest>.  

- If <src> is a URL and <dest> does end with a trailing slash, then the filename is inferred from the URL and the file is downloaded to <dest>/<filename>. For instance, ADD http://example.com/foobar / would create the file /foobar. The URL must have a nontrivial path so that an appropriate filename can be discovered in this case (http://example.com will not work).  

- If <src> is a directory, the entire contents of the directory are copied, including filesystem metadata.  

### COPY

The `COPY` instruction copies new files or directories from <src> and adds them to the filesystem of the container at the path <dest>.  

### ENTRYPOINT

An `ENTRYPOINT` allows you to configure a container that will run as an executable. For example 

The *exec* form, is preferred form:  
`ENTRYPOINT ["executable", "param1", "param2"]`

### VOLUME

The `VOLUME` instruction creates a mount point with the specified name and marks it as holding extranlly mounted volunes from native host or other containers.  
`VOLUME ["/data"]

### WORKDIR

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, `ADD` instructions that follow it in the `Dockerfile`. The `WORKDIR` instructions can be used **multiple** times in a `Dockerfile`  
`WORKDIR /path/to/workdir`

### ARG

The `ARG` instruction defines a variable that users can pass at build-time to the builder with `docker build` command using the `--build-arg <varname>=<value>`.  

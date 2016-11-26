## Installation

Firstly, on the cluster machine, build the containers:

```console
$ ./build_containers.sh
```

Then install the application:

```console
$ pip install --user .
```

Run via the ``flask`` command:

```console
$ FLASK_APPLICATION=bigjobbies flask run
```

## Quick start

### On the compute server

Firstly, set up a local [virtualenv](https://virtualenv.pypa.io/en/stable/) to
install Python packages in:

```console
python -m virtualenv -p $(which python3) bigjobbies_venv
source bigjobbies_venv/bin/activate
```

Then install the application and [gunicorn](http://gunicorn.org/) web
application runner:

```console
pip install --upgrade gunicorn git+https://github.com/rjw57/bigjobbies#egg=bigjobbies
```

Then start the application server. (If ``gunicorn`` complains about port 8000
already being in use add the ``-b localhost:<portnumber>`` option with a
different port number.)

```console
gunicorn bigjobbies:app
```

### On your local machine

Start a SSH tunnel to the compute server. In this example, the port number the
application is running on is 8000 and the compute server is called ``yoshi``.

```console
ssh -fN -L5000:localhost:8000 yoshi
```

You can now navigate to [localhost:5000](http://localhost:5000/) in your browser
and get started.

### Other ways of port forwarding

#### ngrok

[ngrok](https://ngrok.com/) can be used to forward the application to machines
without SSH installed. For example, on the compute server, download ``ngrok``
and use the following command:

```console
./ngrok http --bind-tls true 8000
```

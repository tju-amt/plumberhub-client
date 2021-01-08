# plumberhub-client
A Client SDK of PlumberHub impliemented by python.
``plumberhub-client`` can be used with Python >= 3.7.

# Installation

Install ``plumberhub-client`` with:
```
pip install plumberhub-client
```
or,
```
pipenv install plumberhub-client
```

# Basic example

Here's a example. It will print each sample.
```python
from src.plumberhub.Client import PlumberHubClient

def handleSample(sample):
    print(sample)

client = PlumberHubClient(
    # plumberhub server hostname
    hostname = '127.0.0.1',

    # plumberhub server port
    port = 8080,

    # A clientId applied from plumberhub
    client_id = 'f7e9e4cabe7ed2f95ee506199cd41e0a0d352e91466ef7f2c87793a92e76d198',

    # Do something on sample incoming
    onsample = handleSample,
)
```

# Working with BDF/EDF file

[An example](https://github.com/tju-amt/plumberhub-client-example.git)

# License

``plumberhub-client`` is a free Open Source software released under the MIT license.
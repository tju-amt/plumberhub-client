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
from plumberhub import PlumberHubClient

def handleSample(sample):
    print(sample)

def sayHello():
    print('hello')

    device = client.get_device()
    gain = client.get_gain()
    sampling_rate = client.get_sampling_rate()
    
    print(device)
    print(gain)
    print(sampling_rate)
        
    client.start()

def sayBye():
    print('bye')

client = PlumberHubClient(
    # plumberhub server hostname
    hostname = '127.0.0.1',

    # plumberhub server port
    port = 8080,

    # A clientId applied from plumberhub
    client_id = 'f7e9e4cabe7ed2f95ee506199cd41e0a0d352e91466ef7f2c87793a92e76d198',

    # Do something on sample incoming
    onsample = handleSample,

    onready = sayHello,

    onclose = sayBye
)

time.sleep(2)
client.stop()
client.close()

```

# Working with BDF/EDF file

[An example](https://github.com/tju-amt/plumberhub-client-example.git)

# License

``plumberhub-client`` is a free Open Source software released under the MIT license.
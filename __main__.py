from src.plumberhub.Client import PlumberHubClient
import time

bbb=0

def p(sample):
    print(sample.at)

client = PlumberHubClient(
    hostname = '127.0.0.1',
    port = 8080,
    client_id = 'f7e9e4cabe7ed2f95ee506199cd41e0a0d352e91466ef7f2c87793a92e76d198',
    onsample = p,
    onerror = p,
    onclose = p
)

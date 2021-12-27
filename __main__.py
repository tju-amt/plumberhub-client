from src.plumberhub.Client import PlumberHubClient
import time

global cnt
cnt = 0

def p(sample):
    print(sample)

def p1(sample):
    global cnt
    cnt+=1
    if(cnt %100 == 0):
        print(cnt)

def onclose():
    print(88)

def onready():
    print('hello')

    device = client.get_device()
    gain = client.get_gain()
    sampling_rate = client.get_sampling_rate()
    
    print(device)
    print(gain)
    print(sampling_rate)
        
    time.sleep(10)
    client.start()

    master = client.is_master()
    print(master)
    



client = PlumberHubClient(
    hostname = '127.0.0.1',
    port = 8080,
    client_id = '0c3eb6949ed2368bf338e3ab08653621ff6f65564a306ddd8bf2966f1fecfa25',
    onsample = p1,
    onevent = p,
    onerror = p,
    onclose = onclose,
    onready = onready
)


time.sleep(2)
# client.set_gain(24)
newgain = client.get_gain()

print('\nnew gain:' + str(newgain) + '\n')

client.stop()
client.close()
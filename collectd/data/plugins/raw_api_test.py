from websocket import create_connection
import json

ip = '10.30.0.223'
port = '9000'
choice = 'n'

# while(choice != 'y'):
#     ip = input("enter the ip address:")
#     port = input("enter the port: ")
#     choice = input("{}:{} is correct? \n press y or n to retry ...".format(ip, port))

print("ws://{}:{}".format(ip, port))
ws = create_connection("ws://{}:{}".format(ip, port))
result =  ws.recv()
j_res = json.loads(result)
print(j_res)
message = "init" 
if (j_res['message'] == 'ready'):   
    while(message != 'exit'):
        message = input("message: ")
        try:
            ws.send("{\"message\":\"%s\"}" % (message))
            result =  ws.recv()
            j_res = json.loads(result)
            print(j_res)
        except Exception as e:
            print("exception:\n")
            print(e)
            print("no response...")
else:
    print ("device no connected")            

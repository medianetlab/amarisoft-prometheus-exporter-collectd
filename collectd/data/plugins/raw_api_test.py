from websocket import create_connection
import json

ip = '10.30.0.223'
port = '9001'
choice = 'n'

# while(choice != 'y'):
#     ip = input("enter the ip address:")
#     port = input("enter the port: ")
#     choice = input("{}:{} is correct? \n press y or n to retry ...".format(ip, port))
while(choice != '1' and choice != '1'):
    choice = input("press (1) for MME, (2) for ENB\n")
    if (choice == '1'):
        port = '9000'
        break
    elif (choice == '2'):
        port = '9001'
        break
    print("wrong choice... try again!\n")    
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
            if message == "ue_get":
                ws.send("{\"message\":\"ue_get\" ,\"stats\"=true}")
            else:    
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

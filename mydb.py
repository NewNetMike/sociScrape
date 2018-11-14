import pyrebase
from secrets import *

db = pyrebase.initialize_app(config).database()

def db_save(location, data):
    nodes = location.split("/")
    n = db.child(nodes[0])
    for i in range(1, len(nodes)-1):
        n = n.child(nodes[i])
    #print("node-1 : " + nodes[-1] + ", strVAL : " + str(data))
    n.update({nodes[-1]:str(data)})



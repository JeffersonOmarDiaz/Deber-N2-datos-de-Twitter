#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "7S1GtIcHDgb7sHKPI9UbToNee"
csecret = "DiWXkdOs8McEUBXqzduyxLKGDI1dlxkV7plx3PhaSGkCEMsbGc"
atoken = "1342889774-uTgjppSYGraFFnMCN0hSGDXudVokTjGPv1Rtbdc"
asecret = "9ZtEetYdwhHb7qPY2ynylMKoMrs0bxRDlHuvkhMvqjb3Z"

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('geografico')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['geografico']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-74.1058040766,40.6300348044,-73.9082243672,40.7793526798])
#twitterStream.filter(track = ["ecuador", "temblor", "alcaldequito", "tragedia","terremoto"])

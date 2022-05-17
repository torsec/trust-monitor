from http import client
from pymongo import MongoClient

client = MongoClient('172.17.0.2', 27017, username='mongo', password='prova')
db = client['admin']
whitelists = db['whitelist']

def store_whitelist(whitelist):

    _id = whitelists.insert_one(whitelist).inserted_id
    
    return _id
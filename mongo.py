from pymongo import MongoClient
from config import MONGODB_URI

cluster = MongoClient(MONGODB_URI)
db = cluster['cwp']

welcome_db = db['welcomes']



from pymongo import MongoClient

class Audit :
  def __init__(
    self,
    db_url,
    db_name,
    db_collection,
  ):
    self.db_url = db_url
    self.db_name = db_name
    self.db_collection = db_collection

  def count(self, criteria):
    client = MongoClient(self.db_url)
    db = client[self.db_name]
    collection = db[self.db_collection]
    return collection.count_documents(criteria)
  
  def find(self, criteria):
    client = MongoClient(self.db_url)
    db = client[self.db_name]
    collection = db[self.db_collection]
    return list(collection.find(criteria).sort('createdAt', 1).limit(1))
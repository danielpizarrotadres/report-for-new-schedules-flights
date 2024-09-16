class Log :
  def __init__(
    self,
    db_url,
    db_name,
    db_collection,
  ):
    self.db_url = db_url
    self.db_name = db_name
    self.db_collection = db_collection

    def get_logs(self, criteria):
        print('get_logs')
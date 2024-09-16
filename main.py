# TODO
# 1- Get all flights since 2024-09-14 until current date
# 2- Iterate over each flight and get all audits for each flight
# 3- Iterate over each audit and get all affectations for each audit. If affectation is not found, get all logs for the audit

import os
from datetime import datetime
from audits import Audit
from dotenv import load_dotenv

if __name__ == '__main__':
  print('Start')

  query = {
    "createdAt": {"$gte": datetime(2024, 9, 14, 0, 0, 0),
    "$lte": datetime(2024, 9, 17, 0, 0, 0) }
  }

  dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
  load_dotenv(dotenv_path)

  db_url = os.getenv('DB_PDC_EXTRACTOR_URL')
  db_name = os.getenv('DB_PDC_EXTRACTOR_NAME')
  db_collection = os.getenv('DB_PDC_EXTRACTOR_COLLECTION')

  audit = Audit(db_url, db_name, db_collection)

  # print(audit.count(query))
  # print(audit.find(query))



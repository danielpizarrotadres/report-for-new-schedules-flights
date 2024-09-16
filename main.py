# TODO
# 1- Get all flights since 2024-09-14 until current date
# 2- Iterate over each flight and get all audits for each flight
# 3- Iterate over each audit and get all affectations for each audit. If affectation is not found, get all logs for the audit

from . import affectations, audits, main
from datetime import datetime

if __name__ == '__main__':
  print('Start')

  query = {
    "createdAt": {"$gte": datetime(2024, 9, 2, 0, 0, 0),
    "$lte": datetime(2024, 9, 4, 0, 0, 0) }
  }
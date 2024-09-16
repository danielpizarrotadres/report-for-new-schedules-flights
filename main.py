import os
from datetime import datetime
from audits import Audit
from pdc import Pdc
from dotenv import load_dotenv
import pandas as pd

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
db_url = os.getenv('DB_PDC_EXTRACTOR_URL')
db_name = os.getenv('DB_PDC_EXTRACTOR_NAME')
db_collection = os.getenv('DB_PDC_EXTRACTOR_COLLECTION')

def find_audits(audits, criteria):
  audits_found = []
  for index, item in enumerate(audits):
    tstamp = item.get('flightUniqueId')[:19]
    action = item.get('actionType')
    idFlight = item.get('flightId')
    if (
      tstamp == criteria.get('TSTAMP') and
      action == criteria.get('ACTION') and
      idFlight == criteria.get('ID')
    ):
      audits_found.append(item)
  return audits_found

if __name__ == '__main__':
    print('Start')

    # Find all audits from 2024-09-14 until 2024-09-17
    audit = Audit(db_url, db_name, db_collection)
    since = datetime(2024, 9, 14, 0, 0, 0)
    until = datetime(2024, 9, 17, 0, 0, 0)
    print(f"Criteria: {since} -> {until}")
    audits = audit.find({
        "createdAt": {
            "$gte": since,
            "$lte": until
        }
    })
    print(f"Total audits: {len(audits)}")

    # Find all audits from PDC database
    pdc = Pdc()
    audits_from_pdc = pdc.find()

    # List to collect all data
    all_data = []

    # Iterate over each audit from PDC database and find it in the audits
    for index, item in enumerate(audits_from_pdc):
        print(f'Processing audit {index + 1} of {len(audits_from_pdc)}')

        audits_belonging_pdc = find_audits(audits, item)
        print(f"Total audits_belonging_pdc found: {len(audits_belonging_pdc)}")

        if len(audits_belonging_pdc) == 0:
            print(f"Audit not found in the database")
            continue

        for j, element in enumerate(audits_belonging_pdc):
            print(f'Processing audit_belonging_pdc {j + 1} of {len(audits_belonging_pdc)}')

            all_data.append({
                'PDC EMPLOYEE': item.get('EMPLOYEE'),
                'PDC TSTAMP': item.get('TSTAMP'),
                'PDC ID': item.get('ID'),
                'PDC IDDATE': item.get('IDDATE'),
                'AUDIT ORIGIN': element.get('origin'),
                'AUDIT DESTINATION': element.get('destination'),
                'AUDIT FLIGHT ID': element.get('flightId'),
                'AUDIT DEPARTURE DATE': element.get('departureDate'),
                'AUDIT ID': element.get('_id'), 
            })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(all_data)

    # Get the current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'report_{current_time}.xlsx'

    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)
    print(f'Excel file {file_name} created successfully')
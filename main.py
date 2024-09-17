import os
from datetime import datetime
from audits import Audit
from pdc import Pdc
from affectations import Affectation
from dotenv import load_dotenv
import pandas as pd

green = "\033[92m"
reset = "\033[0m"
red = "\033[91m"
yellow = "\033[93m"

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
db_url_pdc_extractor = os.getenv('DB_PDC_EXTRACTOR_URL')
db_name_pdc_extractor = os.getenv('DB_PDC_EXTRACTOR_NAME')
db_collection_pdc_extractor = os.getenv('DB_PDC_EXTRACTOR_COLLECTION')

db_url_affected_flights_request = os.getenv('DB_AFFECTED_FLIGHTS_REQUEST_URL')
db_name_affected_flights_request = os.getenv('DB_AFFECTED_FLIGHTS_REQUEST_NAME')
db_collection_affected_flights_request = os.getenv('DB_AFFECTED_FLIGHTS_REQUEST_COLLECTION')

def find_audits(audits, criteria):
  audits_found = []
  for index, item in enumerate(audits):
    tstamp = item.get('flightUniqueId')[:19]
    action = item.get('actionType')
    id_flight = item.get('flightId')
    if (
      tstamp == criteria.get('TSTAMP') and
      action == criteria.get('ACTION') and
      id_flight == criteria.get('ID')
    ):
      audits_found.append(item)
  return audits_found

def find_affected_flights(affectations, criteria):
  flights_found = []
  for index, item in enumerate(affectations):
    id_flight = item.get('flightNumber')
    departure_date = item.get('departureDate')
    origin = item.get('origin')
    # has_manifest = item.get('hasManifest')
    # pnrs = item.get('affectedPnrs')

    old_flight_origin = item.get('oldFlight', {}).get('origin')
    old_flight_destination = item.get('oldFlight', {}).get('destination')
    old_flight_number = item.get('oldFlight', {}).get('flightNumber')
    old_flight_carrier = item.get('oldFlight', {}).get('carrier')
    old_flight_departure_date = item.get('oldFlight', {}).get('departureDate')

    new_flight_origin = item.get('newFlight', {}).get('origin')
    new_flight_destination = item.get('newFlight', {}).get('destination')
    new_flight_number = item.get('newFlight', {}).get('flightNumber')
    new_flight_carrier = item.get('newFlight', {}).get('carrier')
    new_flight_departure_date = item.get('newFlight', {}).get('departureDate')

    mapped_id = int(criteria.get('flightId').split()[1].lstrip('0'))

    if (
      id_flight == mapped_id and
      departure_date == criteria.get('departureDate') and
      origin == criteria.get('origin') and
      old_flight_origin == criteria.get('data', {}).get('oldFlight', {}).get('DEPSTN') and
      old_flight_destination == criteria.get('data', {}).get('oldFlight', {}).get('ARRSTN') and
      old_flight_departure_date == criteria.get('data', {}).get('oldFlight', {}).get('STD')[:10] and
      new_flight_origin == criteria.get('data', {}).get('newFlight', {}).get('DEPSTN') and
      new_flight_destination == criteria.get('data', {}).get('newFlight', {}).get('ARRSTN') and
      new_flight_departure_date == criteria.get('data', {}).get('newFlight', {}).get('STD')[:10]
    ):
      flights_found.append(item)

  return flights_found


if __name__ == '__main__':
  print('Starting process')

  # Find all audits from 2024-09-14 until 2024-09-17
  audit = Audit(db_url_pdc_extractor, db_name_pdc_extractor, db_collection_pdc_extractor)
  since = datetime(2024, 9, 12, 0, 0, 0)
  until = datetime(2024, 9, 17, 0, 0, 0)
  print(f"Searching audits through mongo: {since} -> {until}")
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

  # Find all affected flights from affected-flights-request
  affectation = Affectation(db_url_affected_flights_request, db_name_affected_flights_request, db_collection_affected_flights_request)
  print(f"Searching affectations through mongo: {since} -> {until}")
  affectations = affectation.find({
    "createdAt": {
      "$gte": since,
      "$lte": until
      }
  })
  print(f"Total affectations: {len(affectations)}")

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
      print(f'Processing audit_belonging_pdc {j + 1} / {element.get('_id')} of {len(audits_belonging_pdc)}')

      affectations_belonging_audit = find_affected_flights(affectations, element)
      print(f"Total affectations_belonging_audit found: {len(affectations_belonging_audit)}")

      for k, flight in enumerate(affectations_belonging_audit):
        print(f'{green}Processing affectation_belonging_audit {k + 1} of {len(affectations_belonging_audit)}{reset}')

        all_data.append({
          '[PDC] EMPLOYEE': item.get('EMPLOYEE'),
          '[PDC] TSTAMP': item.get('TSTAMP'),
          '[PDC] ID': item.get('ID'),
          '[PDC] IDDATE': item.get('IDDATE'),
          '[PDC] ACTION': item.get('ACTION'),
          '[AUDIT] ORIGIN': element.get('origin'),
          '[AUDIT] DESTINATION': element.get('destination'),
          '[AUDIT] FLIGHT ID': element.get('flightId'),
          '[AUDIT] DEPARTURE DATE': element.get('departureDate'),
          '[AUDIT] ID': element.get('_id'),
          '[AFFECTATION] ID': flight.get('_id'),
        })

  df = pd.DataFrame(all_data)
  current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
  file_name = f'report_{current_time}.xlsx'
  df.to_excel(file_name, index=False)
  print(f'Excel file {green}{file_name}{reset} created {green}successfully{reset}')
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from connect_to_google_sheets import main as gs_connect

def main():
	"""Google Sheets API read example. Prints values from a sample spreadsheet."""

	# The ID and range of a sample spreadsheet.
	SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms' # Go to https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0 to view sample spreadhseet.
	SAMPLE_RANGE_NAME = 'Class Data!A2:E'

	try:
		service = gs_connect()

		if (service is not False):
			# Call the Sheets API
			sheet = service.spreadsheets()
			result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
			values = result.get('values', [])

			if not values:
				# If the entire range (in this example both A and E columns) is empty.
				print('No data found.')
				return

			print('Name, Major:')
			for row in values:
				# Print columns A and E, which correspond to indices 0 and 4. If one is empty it prins ",".
				print('%s, %s' % (row[0], row[4]))
	except HttpError as err:
		print(err)

if __name__ == '__main__':
	main()

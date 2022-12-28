import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

from connect_to_google_sheets import main as gs_connect

def main():
	load_dotenv()

	SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
	RANGE_NAME = 'Data!A2:N'

	try:
		service = gs_connect()

		if (service is not False):
			# Call the Sheets API
			values = [
				[
					'Example like', 'Example address', 'Example size', 'Example floor', 'Example year', 
					'Example start', 'Example rent', 'Example service costs', '', 'Example utilities cost', 
					'Example total costs', 'Example total pp', 'Example gross pm one', 
				],
				[
					'Example like2', 'Example address2', 'Example size2', 'Example floor2', 'Example year2', 
					'Example start2', 'Example rent2', 'Example service costs2', '', 'Example utilities cost2', 
					'Example total costs2', 'Example total pp2', 'Example gross pm one2', 
				],
			]
			body = {
				'values': values
			}
			result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,valueInputOption="USER_ENTERED", body=body).execute()
			print(f"{result.get('updatedCells')} cells updated.")
			return result
	except HttpError as err:
		print(err)

if __name__ == '__main__':
	main()

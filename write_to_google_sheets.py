import os.path

from googleapiclient.errors import HttpError
from dotenv import load_dotenv

from connect_to_google_sheets import main as gs_connect

def main(values):
	load_dotenv()

	SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
	RANGE_NAME = 'Data!B2:N'

	try:
		service = gs_connect()

		if (service is not False):
			# Call the Sheets API
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

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Available scopes: https://developers.google.com/identity/protocols/oauth2/scopes#sheets.
# Delete token.json if modifying scopes.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
	load_dotenv()

	SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
	RANGE_NAME = 'Data!A2:N'

	"""Google Sheets API example. Prints values from a sample spreadsheet."""
	credentials = None
	
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first time.
	# If the file exists then get the credentials from it.
	if os.path.exists('token.json'):
		credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
	
	# If there are no (valid) credentials available, let the user log in.
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			credentials = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(credentials.to_json())

	try:
		service = build('sheets', 'v4', credentials=credentials)

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

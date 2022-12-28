import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def main():
	"""Connect to Google Sheets API. 
	Returns resource to interact with the API on success. Otherwise returns None."""
	print("Connecting to Google Sheets API...") # TODO: Remove debug

	# Available scopes: https://developers.google.com/identity/protocols/oauth2/scopes#sheets.
	# Delete token.json if modifying scopes.
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

	credentials = None
	
	# Token.json stores the user's access and refresh tokens. 
	# It is created automatically when the authorization flow completes for the first time.
	if os.path.exists('token.json'):
		credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
	
	# If there are no (valid) credentials available, ask the user to log in.
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			credentials = flow.run_local_server(port=0)
		# Save the credentials
		with open('token.json', 'w') as token:
			token.write(credentials.to_json())

	try:
		service = build('sheets', 'v4', credentials=credentials)
		print("Succesfully connect to Google Sheets API.") # TODO: Remove debug
		return service
	except:
		print("An error occured when trying to connect to Google Sheets API.") # TODO: Remove debug
		return None

if __name__ == '__main__':
	main()

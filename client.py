import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class Auth:
	creds = None
	service = None
	def __init__(self):
		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				self.creds = pickle.load(token)

	def login(self):

		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', SCOPES)
				self.creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.pickle', 'wb') as token:
				pickle.dump(self.creds, token)

		self.service = build('sheets', 'v4', credentials=self.creds)
		self.sheet = self.service.spreadsheets()


class Gsheet(Auth):
	idsheet = None
	sheet = None
	def __init__(self, idsheet, *arg, **kwarg):
		super().__init__(*arg, **kwarg)
		self.idsheet = idsheet


	def get_data(self, ranges):
		result = self.sheet.values().get(spreadsheetId=self.idsheet,
									range=ranges).execute()
		values = result.get('values', [])

		if not values:
			print('No data found.')
			return False

		return values

	def update(self, ranges, values):
		values = list(map(lambda x: [x], values))

		batch_update_values_request_body = {
			# How the input data should be interpreted.
			'value_input_option': 'USER_ENTERED',  # TODO: Update placeholder value.

			# The new values to apply to the spreadsheet.
			'data': [
				{
				  "range": ranges,
				  "majorDimension": 'ROWS',
				  "values": values
				}
			],  # TODO: Update placeholder value.

			# TODO: Add desired entries to the request body.
		}

		request = self.sheet.values().batchUpdate(spreadsheetId=self.idsheet, body=batch_update_values_request_body)
		response = request.execute()

		# TODO: Change code below to process the `response` dict:
		return response.get('totalUpdatedRows', 0)
			


if __name__ == '__main__':
	sheet = Gsheet('1KJli5gK8HLNY4tggexu28n9gPcTiRAJ27Cgqb0MCT94')
	sheet.login()
	# for row in sheet.get_data('Class Data!A2:A'):
	# 	print(row)

	sheet.update('B4', [
			1,2,3,4,5

		])
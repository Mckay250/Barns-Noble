import base64
import email
from typing import List
from Google import Create_Service

CLIENT_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

def search_message(search_string: str) -> List:
    try:
        search_result = service.users().messages().list(userId="me", q=search_string).execute()

        if 'result_estimate' in search_result.keys():
            print(f"There were 0 results for {search_string}")
            return None
        else :
            final_list = []
            message_ids = search_result['messages']
            
            for item in message_ids:
                final_list.append(item['id'])
            return final_list

    except Exception as e:
        print("An error occured", e)
        return None

def get_message(msg_id : str) -> str:
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        msg_str = email.message_from_bytes(msg_raw)

        content_type = msg_str.get_content_maintype()

        if content_type == 'multipart':
            # part1 is plain text, part2 is html text
            part1, part2 = msg_str.get_payload()
            return part2.get_payload()
        else:
            return msg_str.get_payload()

    except Exception as e:
        print("An error occured", e)
        return None
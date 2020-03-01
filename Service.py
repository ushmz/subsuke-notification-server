from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from SQLRepository import SQLRepository as sql

class Service:
    
    def sendPushNotfication(self, token, message, extra=None):
        try:
            response = PushClient().publish(
                PushMessage(to=token, body=message, data=extra)
            )
        except PushServerError as serverError:
            print(f'errors: {serverError.errors}')
            print(f'response_data: {serverError.response_data}')
            raise
        except (ConnectionError, HTTPError) as exc:
            raise self.retry(exc=exc)

        try:
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            # from notificationds.models import PushToken
            # PushToken.object.filter(token=token).update(active=False)
            pass
        except PushResponseError as resp:
            print(f'push_response: {resp.push_response._asdict()}')
            raise self.retry(exc=resp)


    def registerToken(self, data, files):
        if data['user']['username']:
            sql.registerToken(data['token'], data['user']['username'])
        else:            
            sql.registerToken(data['token'])


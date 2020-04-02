import requests
import json
from argparse import RawTextHelpFormatter, ArgumentParser
import sys


class SlackConnector:
    USER_LOOKUP_ENDPOINT = 'https://slack.com/api/users.lookupByEmail'
    POST_MESSAGE_ENDPOINT = 'https://slack.com/api/chat.postMessage'

    def __init__(self, auth_token):
        self.auth_token = auth_token

    def get_user_info(self, email: str) -> dict:
        """
        Retrieves user data based on the email
        @param email: User's email, from within the same workspace as auth_token is used
        @return: dict with user-related data
        """

        try:
            user_response = requests.get(self.USER_LOOKUP_ENDPOINT, {'token':  self.auth_token, 'email': email})
            user_response_json = user_response.json()

            if user_response_json['ok']:
                user = user_response_json['user']

                return {
                    'id': user['id'],
                    'name': user['real_name'].split(' ')[0]
                }
            else:
                raise Exception(user_response_json['error'])
        except Exception as e:
            print(f'ERROR {e}')

    def send_message_to_user(self, message: str, user_id: str, message_personalization: dict = None):
        """
        Send message to a Slack user as another Slack user (represented by auth token)
        @param message: String with what is to be sent as a message. Might be personalized using message_personalization
        @param user_id: Recipient's ID
        @param message_personalization: Dict where keys represent strings to be replaced with values of those keys.
                For example {'user_name': 'NAME'} will replace "{user_name}" (with {} included) with NAME
        @return:
        """

        if message_personalization:
            for key, value in message_personalization.items():
                message = message.replace(f'{{{key}}}', value)

        headers = {'Authorization': f'Bearer {self.auth_token}', 'Content-type': 'application/json'}
        payload = {'channel': user_id,
                   'text': message,
                   'as_user': True}

        try:
            requests.post(self.POST_MESSAGE_ENDPOINT, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(f'ERROR {e}')


class FileHelper:
    """
    Utility class for accessing files on the disk.
    """

    @staticmethod
    def emails(path_user_emails) -> set:
        with open(path_user_emails) as f:
            return {line.rstrip() for line in f}

    @staticmethod
    def message(path_message) -> str:
        with open(path_message) as f:
            return f.read()


class CustomArgumentParser(ArgumentParser):
    """
    Argument parser and help generator.
    """
    def __init__(self):
        super().__init__(description=
                         "Send a message to multiple Slack users from a specified user's account.\n\n"
                         "The list of recipients needs to be provided in a file, one email per one line.\n"
                         "Please consult option --path_emails for more details.\n\n"
                         "The message to be sent also needs to be put in a file.\n"
                         "It can contain \"templates\" that will be personalized (replaced) on the fly:\n"
                         "  - {user_name}  : user's first name\n"
                         "  - {user_email} : user's email\n"
                         "  - {user_id}    : user's Slack workspace ID\n"
                         "Please consult option --path_message for more details.\n\n",
                         formatter_class=RawTextHelpFormatter)

        required_params = self.add_argument_group('REQUIRED ARGUMENTS')

        required_params.add_argument('-t', '--token',
                                     required=True,
                                     help='Auth token which can be obtained at: '
                                          'https://api.slack.com/apps/APP_ID/oauth'
                                          'after adding user as a Collaborator to the Slack app.')

        optional_params = self.add_argument_group('OPTIONAL ARGUMENTS')

        optional_params.add_argument('-e', '--path_emails',
                                     default='message_slack_users.emails',
                                     help='Path to a file with the list of recipients (user emails). '
                                          'Default: message_slack_users.emails')
        optional_params.add_argument('-m', '--path_message',
                                     default='message_slack_users.message',
                                     help='Path to a file with the message to post. '
                                          'Default: message_slack_users.message')
        optional_params.add_argument('-d', '--dry-run',
                                     default=False,
                                     type=bool,
                                     help='When set to "True" or "1" (without quotes) it will mock sending message '
                                          'to the users but will still retrieve their data via Slack\'s API')

    def error(self, message):
        """
        Overrides default behaviour of displaying only error when one is encountered - this will also display full help
        @param message: string which describes error that has occured
        @return:
        """
        sys.stderr.write('ERROR: %s\n\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    # Load arguments (required or optional with default values)
    config = CustomArgumentParser().parse_args()

    # Instantiate a connector to Slack's API which will use user's unique auth token
    slack_connector = SlackConnector(auth_token=config.token)

    # Load emails (recipients) and message from files on the disk
    emails = FileHelper.emails(config.path_emails)
    message = FileHelper.message(config.path_message)

    # Process emails one by one
    for index, email in enumerate(emails):
        print(f'#{index+1} PROCESSING {email}... ', end='')
        user = slack_connector.get_user_info(email)

        if user:
            if config.dry_run:
                print(f"DRY_RUN {user['name']} @ {user['id']}")
            else:
                print(f"MESSAGING {user['name']} @ {user['id']}")

                message_personalization = {
                    'user_name': user['name'],
                    'user_id': user['id'],
                    'user_email': email,
                }

                slack_connector.send_message_to_user(
                    message=message,
                    user_id=user['id'],
                    message_personalization=message_personalization)

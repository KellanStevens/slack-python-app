import string
import slack
from slack.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
from os import environ as osenv


class text:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class SlackBot:
    _client = None

    def __init__(self, api_token: string) -> None:
        self._client = slack.WebClient(token=api_token)

        try:
            self._client.auth_test()

        except SlackApiError as e:
            print()
            assert e.response["ok"] is False
            assert e.response["error"] # str like 'invalid_auth', 'invalid_arguments', 'invalid_users'
            print(f"Got an error: {e.response['error']}")
            exit()
        
        print("Connection success")

    def workspace_name(self):
        print("Connected to: " + text.BOLD + self._client.team_info().get("team").get("name") + text.END)

if __name__ == "__main__":
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    slack_bot = SlackBot(osenv["SLACK_TOKEN"])
    slack_bot.workspace_name()
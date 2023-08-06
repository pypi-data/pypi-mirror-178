from random import choices
from rich.console import Console
from string import ascii_letters, digits
import requests

if __name__ == '__main__':
    from exceptions import *
else:
    from .exceptions import *

def generate_csrf_token() -> str:
    return "".join(choices(ascii_letters + digits, k=32))


def valid_username(username) -> bool:
    valid_chars = ascii_letters + digits + "_."
    if len(username) == 0:
        return False
    if '..' in username:
        return False
    if username.startswith('.') or username.endswith('.'):
        return False
    if len(username) < 0:
        return False
    for char in username:
        if char not in valid_chars:
            return False
    return True


def username_type(username) -> str:
    if username.startswith('@'):
        return 'username'
    if '@' in username:
        return 'user_email'
    return 'username'


USER_AGENT = 'Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440)'
BASE_URL   = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'


class InstaReset:

    def __init__(self):
        pass

    def send_request(self, username):

        if not valid_username(username):
            raise InvalidUsernameException("Invalid username: {}".format(username))
        
        csrf_token = generate_csrf_token()
        username_type_ = username_type(username)
        data = {username_type_: username, '_csrf': csrf_token}
        headers = {'user-agent': USER_AGENT,}

        response = requests.post(BASE_URL, data=data, headers=headers)
        
        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            raise RateLimitedException("Rate limited")
        elif response.status_code == 404:
            raise UsernameNotFoundException("Username not found: {}".format(username))
        


if __name__ == "__main__":

    console = Console()
    console.clear()
    def input_exit(reason):
        return console.input("[bold red][!] " + reason + ", Press ENTER to exit...")

    console.print("""
[purple]
    ____           __           ____                 __ 
   /  _/___  _____/ /_____ _   / __ \___  ________  / /_
   / // __ \/ ___/ __/ __ `/  / /_/ / _ \/ ___/ _ \/ __/
 _/ // / / (__  ) /_/ /_/ /  / _, _/  __(__  )  __/ /_  
/___/_/ /_/____/\__/\__,_/  /_/ |_|\___/____/\___/\__/  

[*] GitHub > https://www.github.com/Kh4lidMD/InstaReset
[*] PyPi   > https://pypi.org/project/instareset/
[*] PIP    > pip install instareset

[/purple]""")

    username = console.input("[bold green][>] Enter target's username: [/bold green]")
    if not valid_username(username):
        input_exit("Invalid username")
        exit(1)
    console.print("[bold green][>] Target's method: " + username_type(username) + "[/bold green]\n")

    csrf_token = generate_csrf_token()
    headers = {'_csrf': csrf_token, 'User-Agent': USER_AGENT}
    data = {username_type(username): username}

    response = requests.post(BASE_URL, headers=headers, data=data)

    if response.status_code == 404:
        input_exit("Server responded with 404, usually means that the username was not found")
        exit(1)
    elif response.status_code == 429:
        input_exit("Server responded with 429, means that you're being rate limited")
        exit(1)
    
    try:
        status_code = response.status_code
        response = response.json()
    except Exception as e:
        input_exit("Invalid response (could not convert to JSON)")
        exit(1)

    if response['status'] == 'ok':
        console.print("[bold green][>] Password reset link sent successfully![/bold green]\n")
        if username_type(username) == 'username':
            console.print("[bold green][>] " + response['toast_message'] + "[/bold green]\n")
        input_exit("Press ENTER to exit...")
    else:
        input_exit("Something went wrong")
        exit(1)

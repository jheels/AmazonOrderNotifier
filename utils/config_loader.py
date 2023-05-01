import sys
import json
import requests
import logging
from typing import Dict

from .headers import login

# YYYY-MM-DD HH:MM:SS.mmm
logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)


logger = logging.getLogger()
RED_CROSS = "\u274C"
CHECKMARK = "\u2705"

def start() -> bool:
    """
    Initializes the configuration checker and loads the configuration from the 'config.json' file.
    Validates the configuration and confirms the webhook and Amazon Refresh Token.
    
    Returns:
        True if the configuration is valid, False otherwise.
    
    Raises:
        FileNotFoundError: If the 'config.json' file is not found.
        JSONDecodeError: If the 'config.json' file is invalid.
        SystemExit: If the program needs to exit gracefully.
        Exception: If an unexpected error occurs.
    """
    
    logging.info("Initialising configuration checker...")
    logging.info("Loading configuration...")

    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            
        logging.info("Checking configuration...")
        if validate_config(config) and confirm_webhook(config["discord_webhook"]) and confirm_amz_token(config["lwa-refresh_token"]):
            logging.info("Configuration is valid")
            return True
    except FileNotFoundError:
        logging.warning("Configuration file not found " + RED_CROSS)
    except (json.decoder.JSONDecodeError, TypeError):
        logging.warning("Configuration file is invalid " + RED_CROSS)
    except SystemExit:
        pass  # Exit gracefully
    except Exception:
        logging.warning("An unexpected error occurred")
    regenerate_config()

def validate_config(config: Dict[str, str]) -> bool:
    """
    This function validates the syntax of the 'config.json' file and checks if the required keys and their values
    are present. If the file syntax is invalid or the required keys are missing or have no values, it prompts the
    user to exit the program. If the values of the required keys are valid, it returns True.

    Args:
        config: A dictionary object containing the configuration data.
    
    Returns: A boolean value indicating if the configuration is valid or not.
    """
    
    required_keys = {"discord_webhook", "lwa-refresh_token"}

    if not required_keys.issubset(set(config.keys())):
        logging.info("Missing keys in config.json")
    elif not config["discord_webhook"] or not config["lwa-refresh_token"]:
        logging.info("Missing values in config.json")
    else:
        logging.info("Config.json syntax is valid")

        if confirm_webhook(config["discord_webhook"]) and confirm_amz_token(config["lwa-refresh_token"]):
            logging.info("Values in config.json are valid")
            return True

    input("Press Enter to exit...")
    sys.exit(1)


def regenerate_config() -> None:
    """Asks the user if they want to regenerate the 'config.json' file. If yes, regenerates the file
    with empty values for 'discord_webhook' and 'lwa-refresh_token' keys, overwriting the existing file.

    If no, prompts the user to press Enter to exit the program.

    Raises:
        None
    """
    choice = input("Regenerate config.json? (y/n) : ")
    while choice not in ["y", "n"]:
        choice = input("Regenerate config.json? (y/n) : ")
    else:
        if choice == "y":
            with open('config.json', 'w') as config_file:
                config = {"discord_webhook": "", "lwa-refresh_token": ""}
                json.dump(config, config_file, indent=4)
                logging.info("Regenerated config.json\nExiting...")
        else:
            input("Press Enter to exit...")
            sys.exit(1)

def confirm_webhook(webhook_url) -> bool:
    """Checks if the given `webhook_url` is valid by sending a GET request to it.
    
    Args:
        webhook_url (str): The Discord webhook URL to check.
    
    Returns:
        bool: True if the webhook URL is valid and returns a successful response, 
              False otherwise.
    """
    try:
        response = requests.get(webhook_url)
        response.raise_for_status()
        logging.info("1. Webhook URL is valid " + CHECKMARK) 
        return True
    except requests.exceptions.RequestException:
        logging.warning("1. Webhook URL is invalid " + RED_CROSS)
        return False

def confirm_amz_token(refresh_token) -> bool:
    """
    Validates the given Amazon Refresh Token by sending a request to the Amazon OAuth 2.0 token endpoint.

    Args:
        refresh_token: A string representing the Amazon Refresh Token to be validated.

    Returns:
        A boolean indicating whether the given refresh token is valid. Returns True if the token is valid,
        and False otherwise.

    Raises:
        HTTPError: If the request to the token endpoint fails, for example, due to an invalid request or invalid
        client credentials.
    """

    try:
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": "", # Replace with your client_id and client_secret
            "client_secret": "" 
        }
        
        response = requests.post("https://api.amazon.com/auth/o2/token", data=payload, headers=login)
        response.raise_for_status()
        
        logging.info("2. Amazon Refresh Token is valid " + CHECKMARK)
    except requests.exceptions.HTTPError :
        logging.warning("2. Amazon Refresh Token is invalid " + RED_CROSS)
        return False

    return True


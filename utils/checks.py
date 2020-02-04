import os
from shutil import copyfile
import json


def check_folder(path):
    if os.path.exists(path):
        return True
    return False


def check_create_folder(path):
    if not check_folder(path):
        print(f"[Action] I'm creating a folder for you... ({path})")
        os.makedirs(path)


def check_file(path):
    if os.path.isfile(path):
        return True
    return False


def check_copy_file(path):
    if not check_file(path):
        print(f"[Action] I'm copying a base file for you... ({path}). \nYou have to manually edit something in it!")
        source_path = path.split("/")[-1]
        copyfile(f"utils/base/{source_path}", path)


def check_create_file(path, content):
    if not check_file(path):
        print(f"[Action] I'm creating a file for you... ({path})")
        with open(path, "w") as f:
            f.write(content)


def check_logging(guild_id):
    if check_folder(f"data/guilds/{guild_id}"):
        return True
    return False


def check_create_logging(guild_id, chan_id):
    if not check_logging(guild_id):
        check_create_folder(f"data/guilds/{guild_id}")
        logging_base = {"channel_id": str(chan_id), "events_disabled": []}
        logging_str = json.dumps(logging_base, indent=4)
        check_create_file(f"data/guilds/{guild_id}/logging.json", logging_str)

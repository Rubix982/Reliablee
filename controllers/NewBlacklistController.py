# Package imports
from dotenv import load_dotenv
import os

load_dotenv()

def MainNewBlacklistController():
    with open(str(os.environ['BLACKLIST_LOCATION']), mode='a') as file:
        new_domain_to_add_to_blacklist = str(
            input("Enter new domain to add in blacklist: "))
        print(f'New domain extracted as: {new_domain_to_add_to_blacklist}')
        file.write(f"{new_domain_to_add_to_blacklist},\n")
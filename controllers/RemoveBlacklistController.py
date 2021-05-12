# Package imports
from dotenv import load_dotenv
import os

load_dotenv()

def RemoveBlacklistController():
    with open(str(os.environ['BLACKLIST_LOCATION']), mode='a') as file:
        new_domain_to_remove_from_blacklist = str(
            input("Enter new domain to remove from blacklist: "))
        print(
            f'To remove domain extracted as: {new_domain_to_remove_from_blacklist}')

        final_domains = []

        for line in file:
            if new_domain_to_add_to_blacklist != line[0:-1]:
                final_domains.append(line[0:-1])

    with open('blacklist.txt', mode='w') as file:
        for domain in final_domains:
            file.writeline(f"{domain},\n")    
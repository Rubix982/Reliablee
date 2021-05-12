# Local imports
from controllers.ServerController import MainServerController
from controllers.NewBlacklistController import MainNewBlacklistController
from controllers.RemoveBlacklistController import RemoveBlacklistController
from controllers.QuitController import MainQuitController

def main():
    
    while 1:
        option_select = int(input('''
        1. Start server
        2. Add new domain to blacklist
        3. Remove domain from blacklist
        4. Exit
        '''))

        if option_select == 1:
            MainServerController()
        elif option_select == 2:
            MainNewBlacklistController()
        elif option_select == 3:
            RemoveBlacklistController()
        elif option_select == 4:
            MainQuitController()
        else:
            print('Unknown selected option. Choose again')

if __name__ == '__main__':
    main()
import os
import logging

from modules.basic_functions import open_console



def setup() -> None:
    logging.info('Starting setup process...')

    open_console()

# Ideas
# Start with asking what the user wants to do
# [0]: Exit program
    # Y/N confirmation prompt
# [1]: Apply mod profile
    # Select the mod(s) you wish to apply
# [2]: Edit mod profiles
    # [0]: go back
    # [1]: Create mod profile
    # [2]: edit profile 1
        # [1]: Change mod priority
            # select mod, select new position (if > max, put at bottom)
        # [2]: Rename mod profile
        # [3]: Delete mod profile
# [3]: Apply FastFlag profile
# [4]: ?Unapply? FastFlag profile
# [5]: Edit FastFlag profile
    # [0]: Go back
    # [1]: Add new profile
    # [2]: Edit Profile 1
        # [1]: Add FastFlag (?+? USE REQUEST TO CHECK IF ITS ACTUALLY A FFLAG)
        # [2]: Remove FastFlag
        # ?[3]: Validate fastflags (check if they exist)?
        # [3]: Change Profile Name
        # [4]: Delete Profile
    # [3]: Edit Profile 2



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()
from os import mkdir
import sys

# Global variables for changing output of script.
debug_mode = False
year = 2024

# Dictionary containing all of the months' data.
months = {1: ("January", lambda: 31), 2: ("February", lambda: check_leapyear()),
          3: ("March", lambda: 31), 4: ("April", lambda: 30),
          5: ("May", lambda: 31), 6: ("June", lambda: 30),
          7: ("July", lambda: 31), 8: ("August", lambda: 31),
          9: ("September", lambda: 30), 10: ("October", lambda: 31),
          11: ("November", lambda: 30), 12: ("December", lambda: 31)}


def create_markdown() -> None:
    '''
    Creates the project's markdown and folders in the current directories.

    Creates the root folder, and places a blank year file in it which will
    be used for linking the months. It then loops through every month and
    generates the month files, directories, and calls for the days to be made.
    '''
    year_path = "./"+str(year)+"_Calendar"
    # First, create directory for the calendar.
    create_directory(year_path)
    # Secondly, create the overall year file.
    year_file = open((year_path+"/2024 Recap.md"), "w+")
    year_file.close()
    # Loop through all the months.
    for month in range(1, 13):
        month_path = year_path + "/" + months.get(month)[0]
        # For each month, create a directory in the calender.
        create_directory(month_path)
        create_directory(month_path+"/Days")
        # Create the file the links the month to the year.
        create_month_file(month, month_path)
        # Create the days for that month.
        create_days(month, month_path)


def create_month_file(month: int, month_path: str) -> None:
    '''
    Creates the month's markdown file.

    Opens up the template, edits the end to have a link to the year,
    then proceeds to write the template onto the month's markdown file.

    :param month: The current month.
    :type month: int

    :param month_path: The path to the current month's folder.
    :type month_path: str
    '''
    # Open the template and save the contents.
    month_template_file = open("./templates/month.txt", "r")
    month_template = month_template_file.readlines()
    month_template_file.close()
    # Edit the final line to contain the link.
    month_file = open(
        month_path + "/" + months.get(month)[0] + " Recap.md", "w+"
    )
    # Open month file, edit the contents, then close.
    month_file.write((months.get(month)[0] + " Recap\n"))
    month_file.writelines(month_template)
    month_file.close()


def create_days(month: int, month_path: str) -> None:
    '''
    Creates the days for the current month.

    Loops through the amount of days (as found in the months dictionary)
    and calls a function to create the markdown file for each day.

    :param month: The current month.
    :type month: int

    :param month_path: The path to the current month's folder.
    :param month_path: str
    '''
    # Get month data.
    month_data = months.get(month)
    day_path = month_path + "/Days"
    # Loop through every day for the month.
    for day in range(1, month_data[1]()+1):
        if (debug_mode): print("\nCreating day")
        # Generate the day file for the current day.
        create_day_file(month, day, day_path)


def create_day_file(month: int, day: int, path: str) -> None:
    '''
    Creates the markdown file for the current day.

    Opens up the template, edits the end to have a link to the month,
    then proceeds to write the template onto the day's markdown file.

    :param month: The current month.
    :type month: int

    :param day: The current day.
    :type day: int

    :param path: The path to the current day's folder.
    :type path: str
    '''
    # Open the template and save the contents, then close.
    day_template_file = open("./templates/day.txt", "r")
    day_template = day_template_file.readlines()
    day_template_file.close()
    # Edit last line to have link.
    day_template[len(day_template)-1] = (day_template[len(day_template)-1]
                                         + "[[" + months.get(month)[0]
                                         + " Recap]].")
    # Calculate the file name (YYYY-MM-DD).
    # Unfortunately, this script will only be able to be used for 8000 years (as zfill is set to 4).
    day_name = str(year).zfill(4)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)
    # Open (or create) the file.
    day_file = open((path+"/"+day_name+".md"), "w+")
    # Add title
    day_file.write(day_name+"\n")
    # Add contents of template, then close.
    day_file.writelines(day_template)
    day_file.close()


def check_leapyear() -> int:
    '''
    Calculates if it is a leap year, and returns the amount of days for February.

    :return: The amount of days in this year's February.
    :rtype: int
    '''
    # Check if the year is a leap year.
    if (year % 100 != 0 or year % 400 == 0):
        if (year % 4 == 0):
            # If so, return 29.
            if (debug_mode): print(f"{year} is a leap year!")
            return 29
    if (debug_mode): print(f"{year} is not a leap year!")
    # Else, return 28.
    return 28


def create_directory(path: str) -> None:
    '''
    Creates a directory in the specified path.

    Attempts the create the directroy, but allows for the program to continue
    rather than exit and raise an error. With debug mode on, it still prints
    the error message.

    :param path: The path to create a directory for.
    :type path: str
    '''
    try:
        mkdir(path)
    except FileExistsError:
        if (debug_mode): print(f"{path} -> Directory already exists!")
        pass


def parse_command_line_args() -> None:
    '''
    Function to parse the command line arguments given by the user.

    Detects the amount of command line arguments, and dependent on the 
    amount given, parses them, making sure they are acceptable, and 
    applies the values to the global variables.
    '''
    global year, debug_mode
    if (len(sys.argv) == 1):
        pass
    elif (len(sys.argv) == 3):
        # Check if integer, set global var if so.
        try:
            year = abs(int(sys.argv[1]))
        except ValueError:
            raise Exception("Command Line Arguments Invalid -> Please see README.md")
        # Set global var to True or False dependent on input.
        if (sys.argv[2].upper() == "TRUE"):
            debug_mode = True
        elif (sys.argv[2].upper() == "FALSE"):
            debug_mode = False
        else:
            raise Exception("Command Line Arguments Invalid -> Please see README.md")
    else:
        # The command line arguments aren't correct, so raise an error.
        raise Exception("Command Line Arguments Invalid -> Please see the README.md")


if __name__ == "__main__":
    parse_command_line_args()
    create_markdown()

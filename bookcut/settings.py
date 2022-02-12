import configparser
import os
from bookcut.downloader import pathfinder


def initial_config():
    """function to create settings .ini file, used also for restore settings"""
    try:
        write_config = configparser.ConfigParser()
        module_path = os.path.dirname(os.path.realpath(__file__))
        settings_ini = os.path.join(module_path, "Settings.ini")

        write_config.add_section("LibGen")
        write_config.add_section("Settings")
        mirrors = "https://libgen.lc/,http://libgen.li/,http://185.39.10.101/,http://genesis.lib/"
        write_config.set("LibGen", "mirrors", mirrors)
        write_config.set("Settings", "clean_screen", "True")
        write_config.set("Settings", "destination", "None")

        cfgfile = open(settings_ini, "w")
        write_config.write(cfgfile)
        cfgfile.close()
    except PermissionError as error:
        print("\n", error)
        print("You have to be administrator to change BookCut settings. ")


def mirrors_append(url):
    """function to append the LibGen mirrors list"""

    try:

        # READ EXISTING LIST
        config = configparser.ConfigParser()
        module_path = os.path.dirname(os.path.realpath(__file__))
        settings_ini = os.path.join(module_path, "Settings.ini")

        config.read(settings_ini)
        mirrors = config.get("LibGen", "mirrors")
        mirrors = mirrors + "," + url

        # APPEND LIST
        mirrors = str(mirrors)
        config.set("LibGen", "mirrors", mirrors)

        # WRITE TO INI FILE
        cfgfile = open(settings_ini, "w")
        config.write(cfgfile)
        cfgfile.close()

        # Succefully message
        print("\nSuccesfully added to list!:")
        mirrors = mirrors.split(",")
        for i in mirrors:
            print(i)
    except PermissionError as error:
        print("\n", error)
        print("You have to be administrator to change BookCut settings. ")


def read_settings():
    # read the config file settings and printing them

    # get ini file path
    config = configparser.ConfigParser()
    module_path = os.path.dirname(os.path.realpath(__file__))
    settings_ini = os.path.join(module_path, "Settings.ini")

    # get values
    config.read(settings_ini)
    clean_screen = config.get("Settings", "clean_screen")
    destination = config.get("Settings", "destination")
    settings = [clean_screen, destination]
    return settings


def print_settings():
    """Prints settings"""
    settings = read_settings()

    print("\nBookCut Settings:\n")
    print("1.Clean Screen Option Enabled: ", settings[0])
    print("2.Destination Folder Path: ", settings[1])


def screen_setting(input):
    """clean screen settings adjust"""
    try:
        config = configparser.ConfigParser()
        module_path = os.path.dirname(os.path.realpath(__file__))
        settings_ini = os.path.join(module_path, "Settings.ini")

        config.read(settings_ini)
        config.set("Settings", "clean_screen", input)
        cfgfile = open(settings_ini, "w")
        config.write(cfgfile)
        cfgfile.close()
    except PermissionError as error:
        print("\n", error)
        print("You have to be administrator to change BookCut settings. ")


def set_destination(path):
    try:
        if os.path.isdir(path):
            module_path = os.path.dirname(os.path.realpath(__file__))
            settings_ini = os.path.join(module_path, "Settings.ini")

            config = configparser.ConfigParser()
            config.read(settings_ini)
            config.set("Settings", "destination", path)
            cfgfile = open(settings_ini, "w")
            config.write(cfgfile)
            cfgfile.close()
            print("Destination path changed!\n", path)
        else:
            try:
                os.makedirs(path)
                print("Created folder: ", path)
            except FileNotFoundError as error:
                print("\n", error)
                print("(!) Not a valid path please try again!")

    except PermissionError as error:
        print("\n", error)
        print("(!) You have to be administrator to change BookCut settings!")


def path_checker():
    settings = read_settings()
    if settings[1] != "None":
        return settings[1]
    else:
        path = pathfinder()
        return path


if __name__ == "__main__":
    initial_config()

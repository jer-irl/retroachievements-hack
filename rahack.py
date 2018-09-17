#!/usr/bin/env python3

import readline
import cmd
import urllib.request
import json

consoles = {
    "MEGA_DRIVE": 1,
    "NINTENDO_64": 2,
    "SUPER_NINTENDO": 3,
    "GAMEBOY": 4,
    "GAMEBOY_ADVANCE": 5,
    "GAMEBOY_COLOR": 6,
    "NINTENDO": 7,
    "PC_ENGINE": 8,
    "SEGA_CD": 9,
    "SEGA_32X": 10,
    "MASTER_SYSTEM": 11,
    "PLAYSTATION": 12,
    "ATARI_LYNX": 13,
    "NEOGEO_POCKET": 14,
    "GAME_GEAR": 15,
    "GAMECUBE": 16,
    "ATARI_JAGUAR": 17,
    "NINTENDO_DS": 18,
    "WII": 19,
    "WII_U": 20,
    "PLAYSTATION_2": 21,
    "XBOX": 22,
    "SKYNET": 23,
    "XBOX_ONE": 24,
    "ATARI_2600": 25,
    "MS_DOS": 26,
    "ARCADE": 27,
    "VIRTUAL_BOY": 28,
    "MSX": 29,
    "COMMODORE_64": 30,
    "ZX81": 31
}


class Prompt(cmd.Cmd):
    prompt = "(rahack) "
    intro = """See 'help' or '?' for available commands or 'help cmd' for details."""

    def __init__(self):
        super().__init__()
        self._token = None
        self._user = None

    def do_login(self, args):
        """Takes 2 space-delimited args: username and password"""
        split_args = args.split()
        if len(split_args) != 2:
            print(self.do_login.__doc__)
            return

        request_args = {}
        request_args["r"] = "login"
        request_args["u"] = split_args[0]
        request_args["p"] = split_args[1]

        response = self._request(request_args)
        if "Success" not in response or not response["Success"]:
            print("Error")
            return

        self._token = response["Token"]
        self._user = request_args["u"]
        print("Successfully logged in")

    def do_list_consoles(self, args):
        """Takes no arguments.  Gives ids for use in program"""
        print("Console name, followed by id")
        for console in consoles:
            print("{}: {}".format(console, consoles[console]))

    def do_list_games(self, args):
        """Takes the console id, or 0 to list all games, and optionally a search string"""
        args = args.split()
        console_id = int(args[0])
        search_str = "" if len(args) == 1 else " ".join(args[1:])
        search_str = search_str.lower()

        request_args = {"r": "gameslist", "c": console_id}
        result = self._request(request_args)

        if "Success" not in result or not result["Success"]:
            print("Error")
            return

        for game_id in result["Response"]:
            if search_str in result["Response"][game_id].lower():
                print("{}: {}".format(result["Response"][game_id], game_id))

    def do_list_achievements(self, args):
        """Takes the game id and lists the possible achievements.  Must be logged in."""
        game_id = int(args)

        request_args = {
            "r": "patch",
            "g": game_id,
            "t": self._token,
            "u": self._user
        }
        result = self._request(request_args)

        if "Success" not in result or not result["Success"]:
            print("Error")
            return

        print("Achievements:")
        for achievement in result["PatchData"]["Achievements"]:
            print("Title: {}, description: {}, ID: {}".format(achievement["Title"], achievement["Description"], achievement["ID"]))

    def do_get_achievement(self, args):
        """Unlock an achievement"""
        args = args.split()
        achievement_id = args[0]
        hardcore_flag = 1 if len(args) == 2 and args[1] == "1" else 0
        
        request_args = {
            "r": "awardachievement",
            "u": self._user,
            "t": self._token,
            "h": hardcore_flag,
            "a": achievement_id
        }
        result = self._request(request_args)

        if "Success" not in result or not result["Success"]:
            print("Error")
            print(result)
            return

        print("Success")
        print(result)

    def do_exit(self, args):
        exit(0)

    def do_quit(self, args):
        exit(0)

    def _request(self, args):
        base_url = "http://retroachievements.org/dorequest.php"
        if len(args) == 0:
            request_url = base_url
        else:
            args_string = "&".join(["{}={}".format(key, args[key]) for key in args])
            request_url = "{}?{}".format(base_url, args_string)

        response = urllib.request.urlopen(request_url)
        return json.loads(response.read())


def main():
    Prompt().cmdloop()


if __name__ == '__main__':
    main()

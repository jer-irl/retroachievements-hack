# retroachievements-hack
A tool to give yourself achievements you didn't earn :(

I wrote this by reverse-engineering the protocol by using packet captures.  An easier, but less fun method would have been to port the rcheevos library to Python or another scriping language.

Python 3 required, but no non-standard library modules are required.

Example usage:
```
$ python3 rahack.py 
See 'help' or '?' for available commands or 'help cmd' for details.
(rahack) help

Documented commands (type help <topic>):
========================================
get_achievement  help  list_achievements  list_consoles  list_games  login

Undocumented commands:
======================
exit  quit

(rahack) login
Username: [USERNAME]
Password: 
Successfully logged in
(rahack) list_consoles
Console name, followed by id
[...]
SUPER_NINTENDO: 3
[...]
(rahack) list_games 3
[...]
Super Mario World: 228
[...]
(rahack) list_achievements 228
Achievements:
[...]
Title: A Groovy Flight, description: Complete SPECIAL-Groovy without landing past the first ? box. No Yoshi, ID: 46000
[...]
(rahack) get_achievement 46000
```

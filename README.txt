# Kliko's modloader
### Roblox modloader made by Kliko

## COMPATIBILITY WARNING
This program is made to be used on windows operating systems

## Simple Explanations
### Launcher.exe
Executes Main.py with the '-Launcher' command. Use this to launch your modded copy of Roblox.

### Setup.exe
Executes Main.py with the '-Setup' command. Use this to get the latest*[1] Roblox version and apply your mod.

### Info.exe
Executes Main.py with the '-Info' command. Use this to get information on:
  - Modloader version
  - Roblox version
  - Current mod
  - FastFlags


# Detailed Explanations
### Launcher.exe
Executes Main.py with the '-Launcher' command, which launches version_directory\current_version\RobloxPlayerBeta.exe

### Setup.exe
Executes Main.py with the '-Setup' command.


## Troubleshooting issues
### Roblox launches without mod
This can be caused by:
  - Not having applied a mod
  - Roblox updates
To fix this, run Setup.exe and follow the instructions.

### asdf


## footnotes
*[1] - The program iterates over the latest five 'WindowsPlayer' versions from https://setup.rbxcdn.com/DeployHistory.txt until it finds one that has been installed in '%localappdata%\Roblox\Versions', then copies this folder to the version_directory declared in Main.py ('%localappdata%\Roblox modloader\Version folder' by default)
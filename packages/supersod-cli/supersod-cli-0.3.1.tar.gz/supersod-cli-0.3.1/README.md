![y](https://3023500.fs1.hubspotusercontent-na1.net/hub/3023500/hubfs/logos/super-sod-logo.png?width=245&name=super-sod-logo.png)
# Super-Sod Command Line Interface
## Contents
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Commands](#commands)
  - [`auth`](#auth)
  - [`load`](#load)
  - [`tasks`](#tasks)
***
## Installation
To install using `pip` use:

`pip install supersod-cli`
***
## Quickstart
*run the following in cmd*

Add geocoding and Onfleet API keys:

`supersod auth ONFLEET_DEV -k <API_KEY>`

`supersod auth GOOGLE_GEOCODING -k <API_KEY>`

Change directory to one with file named `tasks.csv`. In this example it is on your desktop in a folder named Onfleet:

`cd Desktop/Onfleet`

Upload tasks to Onfleet:

`supersod load csv`

List all tasks in the future:

`supersod tasks list`

Clear all test tasks in the future:

`supersod tasks clear`
***
## Commands
### auth
*Add, check, or remove API keys. Saves keys to your OS's keyring.*

VALID KEY NAMES ARE: **ONFLEET_DEV, AZURE_ADMIN, GOOGLE_GEOCODING**
#### Usage
Set an API key: `supersod auth ONFLEET_DEV -k a1234578bcd9xyz`

Check an API key: `supersod auth GOOGLE_GEOCODING --check`
#### Options
- `-k`, `--key`: Value of key to set.
- `--check`: Print the value of the key to the console.
***
### load
*Load a CSV of tasks into Onfleet.*
#### Usage
Load a file named `tasks.csv` in the current directory: `supersod load csv`

Load a file in your home directory named `Rev02_2022.csv`: `supersod load csv -f '~/Rev02_2022.csv'`
#### Options and Arguments
- `-f`, `--filepath`: Filepath of file to read. Default is `./tasks.csv`.
***
### tasks
*List or clear the tasks currently in Onfleet.*

If you go back more than **THREE DAYS** Onfleet cannot get tasks in the future.
#### Usage
List all future tasks: `supersod tasks list`

Clear all future tasks: `supersod tasks clear`

List tasks in the next three days: `supersod tasks list --to 3`

List tasks from the last week: `supersod tasks list --from 7 --to 0`
#### Options and Arguments
- `action`: The type of action to take. Can be `list` or `clear`
- `-f`, `--from`: Number of days to look back.
- `-t`, `--to`: Number of days to look forward. If `--from` > 3 this won't work...
- `--v`: Verbose - Print entire payload when listing tasks


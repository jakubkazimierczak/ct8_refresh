# CT8 Refresher
Keep your CT8 account(s) expiration date fresh by running a simple command! 
The program signs-in to the user panel with provided credentials. This prolongs
the life of account by 90 days (as stated in CT8 rules).

Features:
* [x] Automatic sign-in for multiple accounts
* [x] View expiration dates and remaining days<sup>1</sup> 
* [x] Manage stored users with ease
* [x] Disable some users from automatic sign-in

Note: (Obviously) This script won't work for already expired accounts.

<sup>1</sup> This doesn't account for user sign-in manually after running the script. 


# Installation
# Requirements
Installation in any of ways below requires you to have 
[Python 3](https://www.python.org/downloads/) and 
[pipx](https://pipxproject.github.io/pipx/installation/) installed.

To install pipx on your system use these commands (on Windows replace `python3` with `python`):
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

> See [pipx installation](https://pipxproject.github.io/pipx/installation/) for more details.

## Install with pipx (recommended)
To install this package use `pipx install`:
```
pipx install git+https://github.com/jakubkazimierczak/ct8_refresh
```
The package will be globally available as `ct8_refresh` or (`ct8_refresh.exe` on Windows).  

> **Note**: On first run headless Chrome will be downloaded (~150MB) if it is not found on your system. This is a one time operation 
(and yes, it causes the output to go wild.).
> 

## Run without installing
To run it without installing use `pipx run`:
```
pipx run --spec git+https://github.com/jakubkazimierczak/ct8_refresh ct8_refresh
```
When using package this way you specify parameters after the `ct8_refresh`. e.g.:
```
pipx run --spec git+https://github.com/jakubkazimierczak/ct8_refresh ct8_refresh -h
pipx run --spec git+https://github.com/jakubkazimierczak/ct8_refresh ct8_refresh user --add john_doe
```


# Usage
## Usage help
To get usage help type `ct8_refresh --help`. Program is made of separate commands, 
described in help message as *positional arguments*. Each of them has separate help 
messages, e.g.:
`ct8_refresh run -h`

## First use
### Adding users
First you have to add user that you want to sign-in automatically:
```
ct8_refresh user --add your_username
```
> You will be prompted for a password - don't worry, it won't show up in the console.

If you have multiple users you can add all of them by typing their logins separated by space:
```
ct8_refresh user --add your_username another_username yet_other_username
```
### Running automatic sign-in
After adding all of your users you simply use the command:
```
ct8_refresh run
```
Program will try to sign-in with all of provided and **enabled** accounts.  


# Reporting issues
If you found a bug or encountered an error please open a new issue. It would be 
the best if you include log files (the most recent ones). To get location of the logs use:
```
ct8_refresh --debug-path
```


# Known issues
* When using debug mode log path is printed twice.

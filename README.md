# 2Cool Password Manager

This is a simple demo of a password manager that can be setup and run on your
local machine. It's created to solve the problem of shoulder surfing attacks
and insecure password storage that many students face. This prototype
password manager is created using Python and an encrypted SQLite database.

This project is part of the TECH 12000 course at Purdue University.

## Features

- Create a new account
- Store passwords in an encrypted database (with a master password)
- Generate a random password for a new account
- Retrieve a password for an account
- List all accounts

## Installation

You can use any Python package manager, but I recommend using [`uv`](https://github.com/astral-sh/uv)
to install the dependencies and run the program.

You can follow the install directions at [their documentation page](https://docs.astral.sh/uv/getting-started/installation/)
to install `uv` on your machine.

After installing `uv`, you can clone this repository and install the dependencies.

```sh
git clone https://github.com/rayhanadev/tech120-pwmanager.git
cd tech120-pwmanager
uv venv
source .venv/bin/activate
uv install
```

## Usage

```sh
$ uv run main.py -h
usage: main.py [-h] {add,get,list} ...

2COOL Password Manager

positional arguments:
  {add,get,list}
    add           Add a new password entry
    get           Retrieve a password entry
    list          List all stored services

options:
  -h, --help      show this help message and exit
```

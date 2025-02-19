import argparse
import sys
from getpass import getpass

import lib.db as db
import lib.generator as generator


def add_entry(db_data: dict, service: str, username: str, password: str) -> dict:
    db_data[service] = {"username": username, "password": password}
    print(f"Entry for '{service}' added.")
    return db_data


def get_entry(db_data: dict, service: str):
    entry = db_data.get(service)
    if entry:
        print(f"\nService: {service}")
        print(f"Username: {entry.get('username')}")
        print(f"Password: {entry.get('password')}\n")
    else:
        print(f"No entry found for service: {service}")


def list_services(db_data: dict):
    if db_data:
        print("Stored services:")
        for service in db_data:
            print(f" - {service}")
    else:
        print("No entries in database.")


def main():
    parser = argparse.ArgumentParser(description="2COOL Password Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_add = subparsers.add_parser("add", help="Add a new password entry")
    parser_add.add_argument("--service", required=True, help="Name of the service")
    parser_add.add_argument(
        "--username", required=True, help="Username for the service"
    )
    parser_add.add_argument(
        "--password",
        help="Password for the service (if not provided, one will be generated)",
    )
    parser_add.add_argument(
        "--length", type=int, default=12, help="Length for generated password if needed"
    )

    parser_get = subparsers.add_parser("get", help="Retrieve a password entry")
    parser_get.add_argument("--service", required=True, help="Name of the service")

    subparsers.add_parser("list", help="List all stored services")

    args = parser.parse_args()

    master_password = getpass("Enter master password: ")

    try:
        data = db.load_db(master_password)
    except Exception:
        sys.exit(1)

    if args.command == "add":
        service = args.service
        username = args.username
        if args.password:
            password = args.password
        else:
            password = generator.generate_password(args.length)
            print(f"Generated password: {password}")
        data = add_entry(data, service, username, password)
        db.save_db(data, master_password)
    elif args.command == "get":
        get_entry(data, args.service)
    elif args.command == "list":
        list_services(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

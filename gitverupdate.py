#!/usr/bin/env python3
# program: gitverupdate.py
# purpose: easily update a file's internal version variable with the TAG from the github repo it is in

import subprocess
import argparse
import os
import re

# Constant for the default version variable name
VERSION_VARIABLE_NAME = '__VERSION__'
__VERSION__ = None

def parse_arguments():
    parser = argparse.ArgumentParser(description="Update version variable in source code from Git tag.")
    parser.add_argument("file_path", help="Path to the target source code file.")
    parser.add_argument("--var_name", default=VERSION_VARIABLE_NAME, help="Name of the version variable to update.")
    return parser.parse_args()

def get_git_version():
    try:
        return subprocess.getoutput('git describe --tags --always')
    except:
        print("Error: Unable to retrieve Git tag.")
        exit(1)

def update_version_in_file(file_path, var_name, version):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Check if the version variable is present in the content
        if var_name in content:
            # Find the version variable and replace its value
            pattern = re.compile(f"{re.escape(var_name)}\\s*=\\s*'\\S+'")
            new_content = pattern.sub(f"{var_name} = '{version}'", content)

            # Confirm with the user and update the file
            if new_content != content:
                print(f"Updating {var_name} to '{version}' in {file_path}. Continue? [y/n]: ", end='')
                if input().strip().lower() == 'y':
                    with open(file_path, 'w') as file:
                        file.write(new_content)
                    print(f"Successfully updated {var_name} to '{version}' in {file_path}.")
                else:
                    print("Update canceled.")
            else:
                print(f"Version variable {var_name} found, but value already matches the tag.")

        else:
            print(f"Version variable {var_name} not found in {file_path}. No update needed.")

    except Exception as e:
        print(f"Error: An unexpected error occurred while updating the file. {str(e)}")
        exit(1)


def main():
    # Parse the command-line arguments
    args = parse_arguments()

    # Validate the file path
    if not os.path.exists(args.file_path) or not os.path.isfile(args.file_path):
        print(f"Error: File {args.file_path} not found.")
        exit(1)

    # Retrieve the Git version (tag or commit hash)
    version = get_git_version()

    # Update the version variable in the target file
    update_version_in_file(args.file_path, args.var_name, version)

if __name__ == '__main__':
    main()

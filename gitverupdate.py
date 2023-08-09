#!/usr/bin/env python3
# program: gitverupdate.py
# purpose: easily update a file's internal version variable with the TAG from the github repo it is in

import subprocess
import argparse
import os
import re

# Constant for the default version variable name
VERSION_VARIABLE_NAME = '__VERSION__'
__VERSION__ = "v1.0.1-1-gf60c827"  # Set your desired version number here

def parse_arguments():
    parser = argparse.ArgumentParser(description="Update version variable in source code from Git tag.")
    parser.add_argument("file_path", nargs="?", help="Path to the target source code file.")
    parser.add_argument("--var_name", default=VERSION_VARIABLE_NAME, help="Name of the version variable to update.")
    parser.add_argument("--version", action="store_true", help="Display the application version.")
    parser.add_argument("--show", action="store_true", help="Display the current Git tag for the repository in the CWD.")
    parser.add_argument("--addmajor", action="store_true", help="Increment the major version.")
    parser.add_argument("--addminor", action="store_true", help="Increment the minor version.")
    parser.add_argument("--addpatch", action="store_true", help="Increment the patch version.")
    parser.add_argument("--taglist", action="store_true", help="Display the list of tags in the repository.")
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
        pattern = re.compile(rf"{re.escape(var_name)}\s*=\s*\"(\S+)\"")
        match = pattern.search(content)
        
        if match:
            current_version = match.group(1)
            
            if current_version != version:
                # Replace the current version with the new version
                new_content = pattern.sub(f"{var_name} = \"{version}\"", content)
                
                # Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.write(new_content)
                print(f"Successfully updated {var_name} to '{version}' in {file_path}.")
            else:
                print(f"Version variable {var_name} found, but value already matches the tag.")
        else:
            print(f"Version variable {var_name} not found in {file_path}. No update needed.")

    except Exception as e:
        print(f"Error: An unexpected error occurred while updating the file. {str(e)}")
        exit(1)


def show_git_tag():
    try:
        git_tag = get_git_version()
        print(f"Current Git tag in CWD: {git_tag}")
    except:
        print("Error: Unable to retrieve current Git tag.")
        exit(1)

def add_major_version():
    try:
        git_version = get_git_version()
        parts = git_version.split('-')
        if len(parts) >= 2:
            major, _ = parts[0].split('.')
            new_major = str(int(major) + 1)
            new_version = f"{new_major}.0.0"
            return new_version
        else:
            print("Error: Unable to determine current version for major increment.")
            exit(1)
    except:
        print("Error: Unable to perform major increment.")
        exit(1)

def add_minor_version():
    try:
        git_version = get_git_version()
        parts = git_version.split('-')
        if len(parts) >= 2:
            major, minor, _ = parts[0].split('.')
            new_minor = str(int(minor) + 1)
            new_version = f"{major}.{new_minor}.0"
            return new_version
        else:
            print("Error: Unable to determine current version for minor increment.")
            exit(1)
    except:
        print("Error: Unable to perform minor increment.")
        exit(1)

def add_patch_version():
    try:
        git_version = get_git_version()
        parts = git_version.split('-')
        if len(parts) >= 2:
            major, minor, patch = parts[0].split('.')
            new_patch = str(int(patch) + 1)
            new_version = f"{major}.{minor}.{new_patch}"
            return new_version
        else:
            print("Error: Unable to determine current version for patch increment.")
            exit(1)
    except:
        print("Error: Unable to perform patch increment.")
        exit(1)

def show_tag_list():
    try:
        tag_list = subprocess.getoutput('git tag --list')
        print("List of tags in the repository:")
        print(tag_list)
    except:
        print("Error: Unable to retrieve tag list.")
        exit(1)

def main():
    # Parse the command-line arguments
    args = parse_arguments()

    if args.version:
        print(f"This is gitverupdate.py version {__VERSION__}")
        return

    if args.show:
        show_git_tag()
        return

    if args.taglist:
        show_tag_list()
        return

    if args.addmajor:
        new_version = add_major_version()
        print(f"New version after major increment: {new_version}")
        try:
            subprocess.run(['git', 'tag', new_version])
            print(f"Git tag '{new_version}' created and added.")
        except Exception as e:
            print(f"Error: Unable to create and add Git tag. {str(e)}")
        return

    if args.addminor:
        new_version = add_minor_version()
        print(f"New version after minor increment: {new_version}")
        try:
            subprocess.run(['git', 'tag', new_version])
            print(f"Git tag '{new_version}' created and added.")
        except Exception as e:
            print(f"Error: Unable to create and add Git tag. {str(e)}")
        return

    if args.addpatch:
        new_version = add_patch_version()
        print(f"New version after patch increment: {new_version}")
        try:
            subprocess.run(['git', 'tag', new_version])
            print(f"Git tag '{new_version}' created and added.")
        except Exception as e:
            print(f"Error: Unable to create and add Git tag. {str(e)}")
        return

    if not args.file_path:
        print("Error: The file_path argument is required.")
        return

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


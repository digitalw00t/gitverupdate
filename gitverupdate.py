#!/usr/bin/env python3
import subprocess
import argparse
import os
import re

VERSION_VARIABLE_NAME = '__VERSION__'
__VERSION__ = "v1.2.0-1-g21398f6"


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
    parser.add_argument("--usage", action="store_true", help="Display the usage instructions.") # Added --usage argument
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()

    # Check if no arguments provided or --usage flag used
    if args.usage or not any(vars(args).values()): # Added condition for --usage or no args
        parser.print_help() # Print the usage instructions
        exit(0) # Exit the script

    return args



def debug_print(debug, message):
    if debug:
        print(f"DEBUG: {message}")

def get_git_version(debug=False):
    try:
        git_version = subprocess.getoutput('git describe --tags --always')
        debug_print(debug, f"Retrieved Git version: {git_version}")
        return git_version if git_version.strip() else None
    except:
        print("Error: Unable to retrieve Git tag.")
        exit(1)

def add_major_version(debug=False):
    git_version = get_git_version(debug)
    if not git_version.startswith('v'):
        debug_print(debug, "No existing version found. Starting from v1.0.0.")
        return "v1.0.0"
    
    try:
        major, _, _ = git_version[1:].split('.')
        new_major = str(int(major) + 1)
        new_version = f"v{new_major}.0.0"
        return new_version
    except Exception as e:
        print(f"Error: Unable to determine current version for major increment. {str(e)}")
        return None

def add_minor_version(debug=False):
    git_version = get_git_version(debug)
    if not git_version.startswith('v'):
        debug_print(debug, "No existing version found. Starting from v0.1.0.")
        return "v0.1.0"
    
    try:
        major, minor, _ = git_version[1:].split('.')
        new_minor = str(int(minor) + 1)
        new_version = f"v{major}.{new_minor}.0"
        return new_version
    except Exception as e:
        print(f"Error: Unable to determine current version for minor increment. {str(e)}")
        return None


def add_patch_version(debug=False):
    git_version = get_git_version(debug)
    if not git_version.startswith('v'):
        debug_print(debug, "No existing version found. Starting from v0.0.1.")
        return "v0.0.1"
    
    try:
        major, minor, patch = git_version[1:].split('.')
        new_patch = str(int(patch) + 1)
        new_version = f"v{major}.{minor}.{new_patch}"
        return new_version
    except Exception as e:
        print(f"Error: Unable to determine current version for patch increment. {str(e)}")
        return None

def add_version_tag(version, debug=False, message="Updated version"):
    debug_print(debug, f"Attempting to add Git tag: {version}")
    try:
        # Delete the existing tag if it exists
        subprocess.run(['git', 'tag', '-d', version], stderr=subprocess.DEVNULL)
        debug_print(debug, f"Deleted existing Git tag '{version}' if it existed.")
        # Create and annotate the new tag
        subprocess.run(['git', 'tag', '-a', version, '-m', message])
        print(f"Git tag '{version}' created and added.")
    except Exception as e:
        print(f"Error: Unable to create and add Git tag. {str(e)}")


def show_git_tag(debug=False):
    debug_print(debug, "Attempting to retrieve Git tag.")
    try:
        git_tag = get_git_version()
        print(f"Current Git tag in CWD: {git_tag}")
    except:
        print("Error: Unable to retrieve current Git tag.")
        exit(1)

def update_version_in_file(file_path, var_name, version):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Check if the version variable is present in the content
        pattern = re.compile(rf"{re.escape(var_name)}\s*=\s*(?:\"(\S+)\"|(\S+))")
        match = pattern.search(content)

        if match:
            current_version = match.group(1) or match.group(2)

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



def main():
    args = parse_arguments()

    # Check if no arguments provided or --usage flag used
    if args.usage or not any(vars(args).values()): # Added condition for --usage or no args
        parser.print_help() # Print the usage instructions
        return

    debug = args.debug

    if args.version:
        print(f"This is gitverupdate.py version {__VERSION__}")
        return

    if args.show:
        show_git_tag(debug)
        return

    if args.taglist:
        show_tag_list()
        return

    if args.addmajor:
        new_version = add_major_version(debug)
    elif args.addminor:
        new_version = add_minor_version(debug)
    elif args.addpatch:
        new_version = add_patch_version(debug)

    if args.addmajor or args.addminor or args.addpatch:
        if new_version:
            debug_print(debug, f"New version determined: {new_version}")
            add_version_tag(new_version, debug)
            print(f"New version after {'major' if args.addmajor else 'minor' if args.addminor else 'patch'} increment: {new_version}")
        else:
            print("Error: Unable to determine current version.")
        return

    if not args.file_path:
        print("Error: The file_path argument is required.")
        return

    if not os.path.exists(args.file_path) or not os.path.isfile(args.file_path):
        print(f"Error: File {args.file_path} not found.")
        exit(1)

    version = get_git_version(debug)
    update_version_in_file(args.file_path, args.var_name, version)

if __name__ == '__main__':
    main()


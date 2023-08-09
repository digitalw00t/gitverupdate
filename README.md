```markdown
# Git Version Updater

This utility script, `gitverupdate.py`, is designed to help you easily update a version variable in your source code files with the Git tag from the GitHub repository it is in. It provides options to increment the major, minor, or patch version, update the version variable, display the application version, and show the current Git tag in the repository's working directory (CWD).

## Usage

Run the script with the desired options and arguments:

```bash
./gitverupdate.py [options] [file_path]
```

Or display the usage instructions:

```bash
./gitverupdate.py --usage
```

## Options

- `file_path`: (Optional) Path to the target source code file that contains the version variable you want to update.

- `--var_name`: (Optional) Name of the version variable to update. Default is `__VERSION__`.

- `--version`: (Optional) Display the version of the `gitverupdate.py` script.

- `--show`: (Optional) Display the current Git tag for the repository in the CWD.

- `--addmajor`: (Optional) Reset the minor and patch versions to 0 and increment the major version.

- `--addminor`: (Optional) Reset the patch version and increment the minor version by one.

- `--addpatch`: (Optional) Increment the patch version by one.

- `--taglist`: (Optional) Display the list of current tags in the repository.

- `--usage`: (Optional) Display the usage instructions for the script. This is also shown if no arguments are provided.

## Examples

1. Display the script version:

   ```bash
   ./gitverupdate.py --version
   ```

2. Show the current Git tag in the repository's CWD:

   ```bash
   ./gitverupdate.py --show
   ```

3. Update the version variable in a source code file:

   ```bash
   ./gitverupdate.py my_script.py
   ```

   This will update the specified version variable in the `my_script.py` file with the latest Git tag.

4. Increment the major version:

   ```bash
   ./gitverupdate.py --addmajor
   ```

   This will reset the minor and patch versions to 0 and increment the major version.

5. Increment the minor version:

   ```bash
   ./gitverupdate.py --addminor
   ```

   This will reset the patch version and increment the minor version by one.

6. Increment the patch version:

   ```bash
   ./gitverupdate.py --addpatch
   ```

   This will increment the patch version by one.

7. Display the usage instructions:

   ```bash
   ./gitverupdate.py --usage
   ```

8. Display the list of current tags:

   ```bash
   ./gitverupdate.py --taglist
   ```

## Git Workflow

1. Make changes to your code and ensure it's working as expected.

2. Run the script to update the version variable in your code file.

3. Use the appropriate Git commands to add and commit your changes:

   ```bash
   git add my_script.py
   git commit -m "Update version variable"
   ```

4. If needed, increment the version using one of the `--addmajor`, `--addminor`, or `--addpatch` options.

5. Commit the version increment using the same Git commands as above.

6. Push your changes to the remote repository:

   ```bash
   git push origin main
   ```

Feel free to customize and adapt this script to your specific needs. If you encounter any issues or have suggestions for improvements, please feel free to contribute or provide feedback.
```

You can replace "main" with the appropriate branch name if you're using a different branch for your development.

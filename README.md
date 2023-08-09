# Git Version Updater

This utility script, `gitverupdate.py`, is designed to help you easily update a version variable in your source code files with the Git tag from the GitHub repository it is in. It provides options to update the version variable, display the application version, and show the current Git tag in the repository's working directory (CWD).

## Usage

Run the script with the desired options and arguments:

```bash
./gitverupdate.py [options] [file_path]
```

## Options

- `file_path`: (Optional) Path to the target source code file that contains the version variable you want to update.

- `--var_name`: (Optional) Name of the version variable to update. Default is `__VERSION__`.

- `--version`: (Optional) Display the version of the `gitverupdate.py` script.

- `--show`: (Optional) Display the current Git tag for the repository in the CWD.

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

## Use Cases

1. **Automated Version Updating**: By integrating `gitverupdate.py` into your build process, you can automatically update the version variable in your source code files with the latest Git tag. This ensures that your application's version information is always in sync with your Git tags.

2. **Easy Script Management**: When working with multiple scripts or applications, you can use the `--var_name` option to specify different version variable names for each script. This provides flexibility in managing version information for various components.

3. **Version Display**: Use the `--show` option to quickly check the current Git tag in the repository's CWD. This can be helpful during development to verify the version associated with your codebase.

Feel free to customize and adapt this script to your specific needs. If you encounter any issues or have suggestions for improvements, please feel free to contribute or provide feedback.
```

# MBOX to EML Converter

This script converts MBOX files to EML files and organizes them into an output folder. It then splits the EML files into subfolders based on a maximum size limit and creates ZIP archives of each subfolder.

## Requirements

- Python 3.x
- The mailbox, os, shutil, and tkinter libraries are included in the standard Python distribution.

## Usage

1. Run the script using a Python interpreter:
   `python mbox_to_eml_converter.py'
2. The script will prompt you to select an MBOX file. Navigate to the desired MBOX file and click "Open".
3. The script will convert the MBOX file to EML files and organize them into an output folder.
4. The EML files will be split into subfolders based on a maximum size limit (default is 500 MB).
5. ZIP archives of each subfolder will be created in the output folder.
6. A message will be displayed indicating that the conversion and archiving process is complete.

## Functions

- select_mbox_file(): Opens file dialog to select MBOX file.
- convert_mbox_to_eml(mbox_file_path): Converts MBOX to EML files and organizes them.
- split_into_subfolders(main_folder, max_size=500*1024*1024): Splits EML files into subfolders.
- create_zip_files(main_folder): Creates ZIP archives of subfolders.
- main(): Orchestrates the conversion, organization, splitting, and archiving processes.

## License

MIT License - see LICENSE.md for details.

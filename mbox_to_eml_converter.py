# MBOX to EML converter

# Import necessary libraries
import mailbox
import os
import shutil
from tkinter import filedialog
from tkinter import Tk

def select_mbox_file():
  # Initialize a Tkinter root window
  root = Tk()
  root.withdraw()  # Hide the main window to only show the file dialog
  # Open a file dialog to select an MBOX file, filtering for '.mbox' extensions
  mbox_file_path = filedialog.askopenfilename(filetypes=[("MBOX files", "*.mbox")])
  return mbox_file_path  # Return the selected file path

def convert_mbox_to_eml(mbox_file_path):
  # Open the specified MBOX file
  mbox = mailbox.mbox(mbox_file_path)
  # Create an output folder for EML files, appending '_EML' to the original MBOX file path
  output_folder = mbox_file_path + "_EML"
  os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

  # Iterate through each message in the MBOX file
  for i, message in enumerate(mbox):
    # Write each message to a separate EML file
    with open(os.path.join(output_folder, f"email_{i+1}.eml"), "w") as eml_file:
      eml_file.write(message.as_string())  # Convert the message to a string and save it

  return output_folder  # Return the path of the output folder containing EML files

def split_into_subfolders(main_folder, max_size=500*1024*1024):
  # Assuming EML files are named with a thread ID and a part number, sort them by thread ID
  eml_files = sorted(os.listdir(main_folder), key=lambda filename: filename.split("_")[1])

  current_folder_size = 0
  current_subfolder_path = os.path.join(main_folder, "subfolder_1")
  os.makedirs(current_subfolder_path, exist_ok=True)  # Create the first subfolder
  subfolder_count = 1

  # Iterate through each EML file
  for eml_file in eml_files:
    if not eml_file.endswith('.eml'):
      continue  # Skip non-EML files

    eml_file_path = os.path.join(main_folder, eml_file)
    eml_file_size = os.path.getsize(eml_file_path)

    # If adding the current file would exceed the max_size, create a new subfolder
    if eml_file_size + current_folder_size >= max_size:
      subfolder_count += 1
      current_subfolder_path = os.path.join(main_folder, f"subfolder_{subfolder_count}")
      os.makedirs(current_subfolder_path, exist_ok=True)  # Create the new subfolder
      current_folder_size = 0  # Reset the size counter for the new subfolder

    # Move the EML file to the current subfolder
    shutil.move(eml_file_path, current_subfolder_path)
    current_folder_size += eml_file_size  # Update the current folder size

def create_zip_files(main_folder):
  # Iterate through each subfolder in the main folder
  for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    # Check if the current item is a directory (subfolder)
    if os.path.isdir(subfolder_path):
      # Create a ZIP archive of the subfolder
      shutil.make_archive(subfolder_path, 'zip', subfolder_path)

def main():
  # Prompt the user to select an MBOX file
  mbox_file_path = select_mbox_file()
  if mbox_file_path:
    # Convert the MBOX file to EML files and organize them into an output folder
    output_folder = convert_mbox_to_eml(mbox_file_path)
    # Split the EML files into subfolders based on a maximum size limit
    split_into_subfolders(output_folder)
    # Create ZIP archives of each subfolder
    create_zip_files(output_folder)
    print("Conversion and archiving complete.")  # Notify the user of completion

# Entry point of the script
if __name__ == "__main__":
  main()

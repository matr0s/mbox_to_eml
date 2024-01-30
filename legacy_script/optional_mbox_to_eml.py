# MBOX to EML converter
import mailbox
import os
import shutil
from tkinter import filedialog
from tkinter import Tk

def select_mbox_file():
  root = Tk()
  root.withdraw() # Hide the main window
  mbox_file_path = filedialog.askopenfilename(filetypes=[("MBOX files", "*.mbox")])
  return mbox_file_path

def convert_mbox_to_eml(mbox_file_path):
  mbox = mailbox.mbox(mbox_file_path)
  output_folder = mbox_file_path + "_EML"
  os.makedirs(output_folder, exist_ok=True)

  for i, message in enumerate(mbox):
    with open(os.path.join(output_folder, f"email_{i+1}.eml"), "w") as eml_file:
      eml_file.write(message.as_string())

  return output_folder

def split_into_subfolders(main_folder, max_size=500*1024*1024): # max size in bytes
  current_folder_size = 0
  current_subfolder_path = os.path.join(main_folder, "subfolder_1")
  os.makedirs(current_subfolder_path, exist_ok=True)
  subfolder_count = 1

  for eml_file in os.listdir(main_folder):
    if not eml_file.endswith('.eml'): # Skip non-EML files
      continue

    eml_file_path = os.path.join(main_folder, eml_file)
    eml_file_size = os.path.getsize(eml_file_path)

    if eml_file_size + current_folder_size >= max_size:
      subfolder_count += 1
      current_subfolder_path = os.path.join(main_folder, f"subfolder_{subfolder_count}")
      os.makedirs(current_subfolder_path, exist_ok=True)
      current_folder_size = 0

    shutil.move(eml_file_path, current_subfolder_path)
    current_folder_size += eml_file_size


def create_zip_files(main_folder):
  for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    if os.path.isdir(subfolder_path):
      shutil.make_archive(subfolder_path, 'zip', subfolder_path)

def main():
  mbox_file_path = select_mbox_file()
  if mbox_file_path:
    output_folder = convert_mbox_to_eml(mbox_file_path)
    split_into_subfolders(output_folder)
    create_zip_files(output_folder)
    print("Conversion and archiving complete.")

if __name__ == "__main__":
  main()
from settings import *
import glob, os, datetime
from shutil import copyfile

def find_oldest_file(rootfolder, extension=".avi"):
    return min(
        (os.path.join(dirname, filename)
        for dirname, dirnames, filenames in os.walk(rootfolder)
        for filename in filenames
        if filename.endswith(extension)),
        key=lambda fn: os.stat(fn).st_mtime)

def backup():
    number_of_backups = specifications["number_of_backups"]
    prefix = specifications["prefix"]
    source_dir = specifications["source_dir"]
    source_file = specifications["source_file_name"]
    dest_dir = specifications["dest_dir"]
    extension = specifications["extension"]

    #Check to see if the directories are actually directories
    if not os.path.isdir(source_dir) or not os.path.isdir(dest_dir):
        raise ValueError("Error with directories. Please check.")

    #Check to see if there is a source file in the directory
    pathToFile =  os.path.join( source_dir, source_file )
    if not os.path.isfile( pathToFile ):
        raise ValueError("Source File Not Found")

    #Copy file
    newFileName = prefix + datetime.date.today().strftime("%Y-%m-%d") + "." + extension
    newFilePath = os.path.join(dest_dir,newFileName)
    copyfile(pathToFile, newFilePath)

    #Check the number of backups. If exceeded, remove oldest.
    listOfFiles = glob.glob( dest_dir + "/*." + extension)
    if len(listOfFiles) > number_of_backups:
        file = find_oldest_file(dest_dir, extension)
        os.remove(file)


if __name__ == '__main__':
    backup()

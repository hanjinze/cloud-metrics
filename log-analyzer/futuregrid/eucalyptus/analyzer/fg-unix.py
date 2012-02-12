#! /usr/bin/env python

import os, glob
import re
import shutil
from datetime import datetime
import fnmatch

# NOTE THIS WILL NOT WORK AS SYNTAX NOT OK, JUST USED TO CATCH IDEAS,
# ANYONE CAN IMPROVE


#
# from 
# http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
#
#

def tail(f, window=20):
    """
    Returns the last `window` lines of file `f` as a list.
    """
    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window + 1
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if bytes - BUFSIZ > 0:
            # Seek back one whole BUFSIZ
            f.seek(block * BUFSIZ, 2)
            # read BUFFER
            data.insert(0, f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.insert(0, f.read(bytes))
        linesFound = data[0].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return ''.join(data).splitlines()[-window:]


"""
#
def sort_euca_log (input,output):
    '''sorts the input file and writes it to the output file with given arguments'''
    # TODO:
    os.system ("sort -u -k5n -k2M -k3n -k4 " + input + " > " + output)
    return

def merge_euca_log (input1, input2, output):
    '''merges the two input files and writes it to the output file with given arguments'''
    os.system ("sort -m -k5n -k2M -k3n -k4 " + input + " > " + output)
    return

#def merge_euca_log_files_in_dir (dirpath, output):
#    ''' merges all logfiles in the dir'''

#    logfiles = glob.glob( os.path.join(dirpath, '*.log*') 
     
    # PSEUDO CODE
    #current_log = logfiles.pop ()
    #for file in logfiles
    #   merge_euca_log (current_log, files, tmp)
    #   os.remove (current_log)
    #   os.move (tmp, current_log)
    #os.move (current_log, output)
    #return                     

#def concat_euca_log_files (input1,input2,output):
#    '''checks and concatenates to output files'''
    # check if the last line of input1 <= input2, assumes asscending order 
#    os.system ('cat ' + input1 + " " + input2 + " > " + output)
#    return

#def sort_accending_euca_log (input, output):
#    '''this function will revert the eucalyptus log file'''
    # maes sure that the input file is in acending order
    # date_start = date from first line
    # date_end = date from last line
#    invert_needed = date_start > date_end
#    if inverted_needed
#       os.system("rev " + input + " > " + output)

#
# based on how euca creates logfiles, I guess we can just combine all logfiles with a .?+ at the end
# we must make sure the order is ok to not effect the date ordering
#
"""

def head(file, lines_2find=1):
   file.seek(0)                            #Rewind file
   return [file.next() for x in xrange(lines_2find)]


def getdate_from_euca_log_line(line):
   tmp = re.split ('\]', line.pop())
   return datetime.strptime(tmp[0][1:], '%a %b %d %H:%M:%S %Y')

def generate_filename (date_object, postfix):
  name = str(date_object).replace(" ","-").replace(":","-")
  return name + postfix 

def rename_euca_log_file (path,name):
    old_name = os.path.join(path,name)
    print " renaming "  + old_name
    new_name = generate_euca_log_filename(path,name)
    print new_name
    if not os.path.exists(new_name):
        os.rename (old_name, new_name)
    else:
        print "file existed already: " + new_name, ", deleting: " + old_name   
        os.remove(old_name)
    return

def generate_euca_log_filename (path,name):
    old_name = os.path.join(path,name)
    FILE = open(old_name, "r", 0) 
    line = tail(FILE,1)
    date_object = getdate_from_euca_log_line(line)
    new_name = generate_filename (date_object,'-cc.log')
    new_name = os.path.join(path,new_name)
    return new_name



def ls(path):
  print "----"
  os.system ("ls " + path)
  print "----"

def all_euca_log_files (path):
    '''returns a list of all euca logfiles recursively starting from path'''
    all_files = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, '*cc.log.*'):
                all_files.append(os.path.join(dirname, filename))
    return all_files

def gather_all_euca_log_files (from_path,backup):
    if not os.path.exists (backup):
        os.makedirs (backup)

    print from_path
    for file in all_euca_log_files(from_path):
        path = os.path.dirname(file)
        name = os.path.basename(file)
        new_name = os.path.basename(generate_euca_log_filename (path,name))
        new_location = os.path.join(backup,new_name)
        if not os.path.exists(new_location):
            print new_name
            shutil.copy2 (file, new_location)
        else:
            print new_name + ", WARNING: file exists, copy ignored"
    return

#####################################################################
# MAIN
#####################################################################
def main():
   dir_path = os.getenv("HOME") + "/Downloads/logbackup"

   backup = "/tmp/backup"

   gather_all_euca_log_files (dir_path,backup)

   return

def works():
  FILE = open("/tmp/cc.log.4", "r", 0) 
  print "---- head ----\n"
  print head(FILE,1)
  print "---- tail ----\n"
  line = tail(FILE,1)
  print line
  date_object = getdate_from_euca_log_line(line)
  print date_object
  print generate_filename (date_object,'-cc.log')
  
  shutil.copy2('/tmp/cc.log.4', '/tmp/cc.log.5')
  ls("/tmp")
  rename_euca_log_file("/tmp", "cc.log.5")
  ls("/tmp")
  return
  
if __name__ == "__main__":
    main()
from optparse import OptionParser
import locale
import time
import os


locale.setlocale(locale.LC_ALL, "")

def main():
    try:
        # Receiving options and paths
        options, paths = choose_process()
        filenames = []
        directories = []
        fullpath_of_files = []

        # Recursion to paths if needed
        if options.recursive:
            for path in paths:
                for directory_path, dirs, files in os.walk(path):
                    # Skip hidden paths
                    if not options.hidden:
                        if directory_path[2:].startswith("."):
                            continue
                        # Fulfilling directories and filenames lists
                        directories += [x for x in dirs if not x.startswith(".")]
                        filenames += [x for x in files if not x.startswith(".")]
                        # Fulfilling list with full paths to file
                        for file in files:
                            fullpath_of_files.append(f"{os.path.join(directory_path, file)}")

                    # Filling lists with all the files in directoire 
                    else:
                        directories += [x for x in dirs]
                        filenames += [x for x in files]
                        for file in files:
                            fullpath_of_files.append(f"{os.path.join(directory_path, file)}")
        # Analyzing required paths only
        else:
            for path in paths:
                files = os.listdir(path)
                [filenames.append(item) for item in files if os.path.isfile(item)] if options.hidden\
                else [filenames.append(item) for item in files if not item.startswith(".") and os.path.isfile(item)]

                [directories.append(item) for item in files if os.path.isdir(item)] if options.hidden\
                else [directories.append(item) for item in files if not item.startswith(".") and os.path.isdir(item)]

                if options.hidden:
                    for file in files:
                        fullpath_of_files.append(f"{os.path.join(path, file)}")
                else:
                    for file in files:
                        if file.startswith("."):
                            continue
                        fullpath_of_files.append(f"{os.path.join(path, file)}")

        # Receiving the last time of file's modification
        files_modification_time = get_modification_time(fullpath_of_files)
        # Receiving files sizes
        files_sizes = get_files_sizes(fullpath_of_files)
        # Receiving amount of files and directories
        count = get_count(filenames, directories)
        order_command = options.order

        # Representing data which is mentioned in order_command
        if order_command in ("m", "modified"):
            for modification_time in files_modification_time:
                print(modification_time)
        elif order_command in ("s", "size"):
            for file_size in files_sizes:
                print(file_size)
        elif order_command in ("n", "name"):
            for name in fullpath_of_files:
                print(name[2:])
        else:
            for name, modification_time, file_size in zip(fullpath_of_files, files_modification_time, files_sizes):
                result = ("{0: <}  {1: >10}    {2: >.25}").format(modification_time, file_size, name[2:])
                print(result)
        # Printing amount of files and directories
        print(f"{count[0] if count[0] else 'no'} files, {count[1] if count[1] else 'no'} directories")
    except FileNotFoundError as err:
        print (f"ERROR: {err}")
        
# Parsing options and paths     
def choose_process ():
    default_order = ['modified', 'm', 'size', 's', 'name', 'n']
    parser = OptionParser(usage="Usage: task_unit5.py [options] [path1 [path2 [... pathN]]]\n\
                                \nThe paths are optional; if not given . is used.")
    
    parser.add_option("-H", "--hidden", action="store_true", dest="hidden", 
            help="show hidden files [default: off]")
    parser.add_option("-m", "--modified", action="store_true", dest="modified", 
            help="show last modified date time [default: off]")
    parser.add_option("-o", "--order", dest="order", choices=default_order,
            help=f"order by {default_order}")
    parser.add_option("-r", "--recursive", action="store_true", dest="recursive", 
            help="recurse into subdirectories [default: off]")
    parser.add_option("-s", "--sizes", action="store_true", help="show sizes [default: off]") 
   
    options, args = parser.parse_args()
    if not args:
        args = ["."]
    return options, args

# File's last time of modification
def get_modification_time (files_path):
    files_time = []
    for file in files_path:
            m_time = time.ctime(os.path.getmtime(file))
            files_time.append(" ".join(m_time.split()[3:]))
    return files_time

# Receiving files sizes
def get_files_sizes (files_path):
    files_sizes = []
    for file in files_path:
        files_sizes.append(os.path.getsize(file))
    return files_sizes

# Amount of found files and directories
def get_count(filenames, directories):
    return sum([1 for file in filenames]), sum([1 for directoire in directories])

main()
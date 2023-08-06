#Helper functions for issues related to linux and windows cross platform runtime
from sys import platform
import os
import time

#operating system helper function for paths
def os_path_helper(path_check):
    if(platform == "linux"):
        return path_check.replace("\\", "/")
    return path_check

def SinceLastModified(file_path, divide_seconds = 1):
    if(os.stat(file_path).st_size == 0):
        return -1
    file_to_check = os.stat(file_path).st_mtime
    time_since_modified = (time.time() - file_to_check)/divide_seconds
    return time_since_modified
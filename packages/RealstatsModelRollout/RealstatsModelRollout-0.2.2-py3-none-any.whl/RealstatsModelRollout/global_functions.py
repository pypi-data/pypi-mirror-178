import os
from six import string_types


class globalFunctions:
    def __init__(self):
        self._id = "Optional"

    ### get index location of char in string ###
    def Find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def Path_is_dir(localpath=""):
        local_envpath = ""
        ### Get directory ###
        print("Looking for directory")
        if localpath[-1] == '/':
            local_envpath = localpath
        else:
            local_envpath = localpath + "/"

        isDirectory = os.path.isdir(local_envpath)
        if isDirectory == True:
            return local_envpath
        else:
            raise Exception("Given localpath: " +
                            local_envpath + " is not a directory")

    def Is_value_string(value):
        if isinstance(value, string_types):
            return value
        else:
            return Exception("Type is not string")

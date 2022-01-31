# JOINER.PY V0.1.2

# script made by code-explorer786
# purpose: joins mlog code together

# usage (similar to C):
# %include file / %i file  : inserts contents of file
# %select files / %s files : user input to select a file
# %define NAME VALUE       : define
# %undef NAME              : undefine
# %ifdef NAME              : check if defined
# %ifimported FILENAME     : checks if imported


# how to run:
#    python joiner.py -s src -o dst [--unsafe/-u]

# TODO:
# - add more stuff

import sys

included = []
unsafe = False
src = ""
dst = ""
definitions = {}

def define(k, v):
    global definitions
    definitions[k] = v

def undefine(k):
    global definitions
    del definitions[k]

def apply(s):
    result = []
    for i in s.split(" "):
        if i in definitions: result += [definitions[i]]
        else:                result += [i]
    return " ".join(result)

def get_relative(s):
    # bash moment
    # if you use powershell/cmd, use bash, since this is not v1+
    if "/" not in s:
        return "./"
    result = []
    for i in s.split("/")[:-1]:
        if i == "..":
            result = result[:-1]
            continue
        result += [i]
    return "/".join(result)+"/"

def process_args():
    global src
    global dst
    global relative
    global unsafe
    argc = len(sys.argv)
    i = 1
    while i < argc:
        d = sys.argv[i]
        if d == "-s":
            i += 1
            src = sys.argv[i]
        elif d == "-o":
            i += 1
            dst = sys.argv[i]
        elif d == "-r":
            i += 1
            relative = sys.argv[i]
        elif d in ["--unsafe","-u"]:
            unsafe = True
        i += 1

def include_file(fname):
    global included
    if fname in included and not unsafe: return ""
    included += [fname]
    return process(fname)

def process(fname):
    global included
    relative = get_relative(fname)
    with open(fname,"r") as f:
        data = f.read().split("\n")
    level = 0
    levels_state = {0:True}
    result = ""
    data_index = 0
    while data_index < len(data):
        data_element = data[data_index]
        processed = data_element.split(" ")
        # let's respect the python interpreters
        # that doesn't support case statements. :D
        if processed[0] == "%else":
            levels_state[level] = not levels_state[level]
            data_index += 1
            continue
        elif processed[0] == "%endif":
            level -= 1
            data_index += 1
            continue

        if levels_state[level] == False:
            data_index += 1
            continue

        if processed[0] in ["%include","%i"]:
            processing = relative+data_element[len(processed[0]):].lstrip()
            result += include_file(processing)
        elif processed[0] in ["%select","%s"]:
            processing = data_element[len(processed[0]):].lstrip().rstrip()
            list_files = [relative+filename.lstrip().rstrip() for filename in processing.split(",") if (filename not in included or unsafe)]
            if len(list_files) == 0: continue
            if len(list_files) == 1:
                result += include_file(processing)
                continue
            print("%SELECT REQUEST\nSelect a file using index:")
            for index in range(len(list_files)): print(index,"|",list_files[index])
            filename = list_files[int(input("[  ]\b\b\b"))]
            result += include_file(filename)
        elif processed[0] == "%define":
            define(processed[1],processed[2] if len(processed) > 2 else "")
        elif processed[0] == "%undef":
            undefine(processed[1])
        elif processed[0] in ["%ifdef","%ifimported"]:
            level += 1
            check = False
            if processed[0] == "%ifdef":
                check = processed[1] in definitions
            elif processed[0] == "%ifimported":
                check = relative+processed[1] in included
            levels_state[level] = check 
        else:
            result += data_element
        result += "\n"
        data_index += 1;
    return result[:-1]

def main():
    process_args()
    if(src == "" or dst == ""):
        print("Uh oh! No src or dst file.")
        return 0
    with open(dst, "w") as file:
        file.write(process(src))
    print("Successful!")

if __name__ == "__main__":
    main()
else:
    print("You're not supposed to do that yet.")

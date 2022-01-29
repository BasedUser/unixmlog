# JOINER.PY V0.1.1

# script made by code-explorer786
# purpose: joins mlog code together

# usage (similar to C):
# %include file (inserts contents of file)
# %i file (same as %include file)

# how to run:
#    python joiner.py -s src -o dst [-r relative/] [--unsafe/-u]

# TODO:
# - add more stuff

import sys

included = []
unsafe = False
src = ""
dst = ""
relative = ""

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

def process(fname):
    global included
    with open(fname,"r") as f:
        data = f.read().split("\n")
    result = ""
    for data_element in data:
        processed = data_element.split(" ")
        # let's respect the python interpreters
        # that doesn't support case statements. :D
        if processed[0] == "%include":
            processing = relative+data_element[8:].lstrip()
            if processing in included and not unsafe: continue
            result += process(processing)
            included += [processing]
        elif processed[0] == "%i":
            processing = relative+data_element[3:].lstrip()
            if processing in included and not unsafe: continue
            result += process(processing)
            included += [processing]
        else:
            result += data_element
        result += "\n"
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

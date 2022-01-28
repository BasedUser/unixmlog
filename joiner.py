# JOINER.PY V0.1

# script made by code-explorer786
# purpose: joins mlog code together

# usage (similar to C):
# %include file (inserts contents of file)
# %i file (same as %include file)

# how to run:
#    python joiner.py src dest

# TODO:
# - add more stuff

import sys

included = []
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
            if data_element[8:] in included: continue
            result += process(data_element[8:])
            included += [data_element[8:]]
        elif processed[0] == "%i":
            if data_element[3:] in included: continue
            result += process(data_element[3:])
            included += [data_element[3:]]
        else:
            result += data_element
        result += "\n"
    return result

def main():
    with open(sys.argv[2], "w") as file:
        file.write(process(sys.argv[1]))
    print("Successful!")

if __name__ == "__main__":
    main()
else:
    print("You're not supposed to do that yet.")

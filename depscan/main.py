import glob
import os
import json
import re
import os


def parse_dependancies(path):
    data = {}
    dependanciesList = []

    for file in glob.glob(f"{path}/**/*requirenments.txt", recursive=True):
        with open(file) as r:
            depends_list = []
            for string in r.read().split('\n'):
                parsed = re.split("==", string)
                # Need to add good parser for dependancies version
                depends_list.append({
                    parsed[0]: parsed[1]
                })

            data[file] = depends_list
    return data


if __name__ == '__main__':
    path = os.getcwd()
    obj = parse_dependancies(path)
    print(json.dumps(obj, indent=2))

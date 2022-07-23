import glob
import os
import json
import re
import os
import requests
from mdutils.mdutils import MdUtils


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


def check_package(package_name, version):
    url = 'https://api.osv.dev/v1/query'
    message = {
        "version": version,
        "package": {
            "name": package_name,
            "ecosystem": "PyPI"
        }
    }

    return json.loads(requests.post(url, json=message).text)


def markdown_create(file_name, title, json_parse):
    mdFile = MdUtils(file_name=file_name,
                     title=title)

    vulnarabilities_list = []

    for i in range(len(json_parse["vulns"])):
        vulnarabilities_list.append({
            "name": json_parse["vulns"][i]["affected"][0]["package"]["name"],
            "summary": json_parse.get("vulns")[i]["summary"],
            "CVE": json_parse.get("vulns")[i].get("aliases", "None"),
            "affected_versions": json_parse.get("vulns")[i]["affected"][0]["versions"],
            "fixed_version": json_parse.get("vulns")[i]["affected"][0]["ranges"][0]["events"][1]["fixed"],
            "link": json_parse.get("vulns")[i]["affected"][0]["database_specific"]["source"]
        })

    rows = len(vulnarabilities_list)+1

    list_of_keys = list(vulnarabilities_list[0].keys())
    coloumns = len(list_of_keys)

    formatted_list = []
    formatted_list += list_of_keys

    values_str_list = []

    for item in vulnarabilities_list:
        for value in list(item.values()):
            values_str_list.append(str(value))

    mdFile.new_line()
    mdFile.new_table(columns=coloumns, rows=rows, text=formatted_list + values_str_list,
                     text_align='center')

    mdFile.create_md_file()


if __name__ == '__main__':
    # path = os.getcwd()
    # obj = parse_dependancies(path)
    # print(json.dumps(obj, indent=2))

    # print(check_package("treq", "17.3.1"))
    markdown_create("treq.md", "Vulnarability for treq",
                    check_package("treq", "17.3.1"))

    markdown_create("treq2.md", "Vulnarability for treq",
                    check_package("Pillow", "4.2.1"))

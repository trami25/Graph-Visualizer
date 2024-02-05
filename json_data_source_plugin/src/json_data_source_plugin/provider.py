import json
import re

def provide_json_data(filepath: str) -> dict:
    create_json_data(filepath)
    with open(filepath, 'r') as file:
            json_data = json.load(file)
    return json_data



def create_json_data(filepath: str):
    my_name = "pharaohs.son"
    include_me = False
    input_txt_file = "json_data_source_plugin\\relations.txt"
    output_json_file = filepath

    nodes = set()
    edges = set()
    dict = {}
    name_to_id = {}

    with open(input_txt_file, 'r') as f:
        for line in f:
            accounts = line.split(" ")
            account_1 = re.search('https://www.instagram.com/(.*)/', accounts[0]).group(1)
            account_2 = re.search('https://www.instagram.com/(.*)/', accounts[1]).group(1)

            nodes.add(account_1)
            if include_me:
                edges.add((account_1, account_2))
            else:
                if not (account_1 == my_name or account_2 == my_name):
                    edges.add((account_1, account_2))

    dict["nodes"] = []

    if include_me:
        name_to_id[my_name] = 0
        dict["nodes"].append({"id": 0, "name": my_name})
    else:
        nodes.remove(my_name)
        pass
    id_n = 1
    for account in nodes:
        dict["nodes"].append({"id": id_n, "name": account, "group": 1})
        name_to_id[account] = id_n
        id_n += 1

    dict["edges"] = []
    bi_edges = set()
    id_l = 1
    for accounts in edges:
        id_1 = name_to_id[accounts[0]]
        id_2 = name_to_id[accounts[1]]
        if (accounts[1], accounts[0]) in edges:
            bi_edges.add((id_1, id_2))
            if (id_2, id_1) not in bi_edges:
                dict["edges"].append({"id": id_l, "source": id_1, "target": id_2, "bi_directional": True})
                id_l += 1
        else:
            dict["edges"].append({"id": id_l, "source": id_1, "target": id_2, "bi_directional": False})
            id_l += 1

    with open(output_json_file, 'w') as outfile:
        json.dump(dict, outfile)

    print("json created")


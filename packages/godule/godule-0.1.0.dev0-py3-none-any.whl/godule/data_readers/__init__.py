def read_jsonl(filename : str) -> list:
    import json
    out_list = list()
    with open(filename) as infile:
        for line in infile:
            out_list.append(json.loads(line))
    return out_list


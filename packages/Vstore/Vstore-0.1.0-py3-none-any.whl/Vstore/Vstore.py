""" variable save/load package by Point from Symbs Studios: V-store"""


def var_write_normalized(file_name: str, var: dict, encoding: str = "cp850"):
    out_list = []
    for key, val in zip(var.keys(), var.values()):
        if type(val) is str or type(val) is int:
            out_var = str(val).encode(encoding)
        elif type(val) is bytes:
            out_var = val
        else:
            out_var = val.encode(encoding)
        typ = str(type(val)).split("'")[1]
        out_list.append(key.encode(encoding)
                        + b"&==:" + typ.encode(encoding)
                        + b"|==:" + out_var+b"\r\n")

    with open(file_name, "wb+") as f:
        f.writelines(out_list)


def var_read_normalized(file_name: str, encoding: str = "cp850"):
    # reads raw data and splits it into lines
    with open(file_name, "rb") as f:
        raw_lines = f.read()[:-2].split("\r\n".encode(encoding))

    out_dict = {}
    for line in raw_lines:
        # converts raw data into usable type, key and values
        split_data_1 = line.split("&==:".encode(encoding))
        split_data_2 = split_data_1[1].split("|==:".encode(encoding))
        key = split_data_1[0].decode(encoding)
        typ = split_data_2[0].decode(encoding)
        val = "|==:".encode(encoding).join(split_data_2[1:])

        # converts type data and value into values with assigned type
        if typ == "str":
            val_normalized = str(val.decode(encoding))
        elif typ == "int":
            val_normalized = int(val.decode(encoding))
        elif typ == "bytes":
            val_normalized = val
        else:
            val_normalized = bytes(val.decode(encoding), encoding=encoding)
        out_dict[key] = val_normalized

    return out_dict


# usage examples:
#   saving:
#       var_write_normalized("yes.txt", save_data)
#   loading:
#       save_data = var_read_normalized("yes.txt")

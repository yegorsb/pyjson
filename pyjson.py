import json


def to_py(jsonpy, filename="dynampy.py"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jsonpy, f, ensure_ascii=False, indent=4)
    pyjson = ""
    with open(filename, "r", encoding="utf-8") as f:
        content = ""
        for line in f.readlines():
            content = content + line[4:]
        pyjson = (
            content.replace("{in_curly}", "__open_currly__")
            .replace("{fin_curly}", "__close_currly__")
            .replace("{is}", "__colon__")
            .replace("{with}", "__camma__")
            .replace("{nextline}", "__next_line__")
            .replace("{tab}", "    ")
            .replace("{quote}", "__single_quote__")
            .replace("{qoutes}", "__double_quote__")
            # Cleaning up json to be full python
            .replace("{", "")
            .replace("}", "")
            .replace("(:", "(")
            .replace(":", "")
            .replace('"', "")
            .replace("'", '"')
            .replace(",\n", "\n")
            # Reverse translation
            .replace("__single_quote__", "'")
            .replace("__double_quote__", '"')
            .replace("__colon__", ":")
            .replace("__open_currly__", "{")
            .replace("__close_currly__", "}")
            .replace("__camma__", ",")
            .replace("__next_line__ ", "\\")
        )
        print("----------------------")
        print(pyjson)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pyjson)


def pyjson_chrysalis_transform(raw_string):
    chrysalis = (
        raw_string.replace("{", "{in_curly")
        .replace("}", "{fin_curly}")
        .replace("{in_curly", "{in_curly}")
        .replace(":", "{is}")
        .replace(",", "{with}")
        .replace("\\", "{nextline}")
        .replace("\t", "{tab}")
        .replace("    ", "{tab}")
        .replace("'", "{quote}")
        .replace('"', "{quotes}")
    )
    return chrysalis


def to_pyjson(data_file="dynampy.py"):
    json_code = {}
    molting, growth = [], []
    nest_delimiter = "    "
    chrysalis_form = []
    cocoon = ""

    def clean_line(line=""):
        line = line.lstrip(nest_delimiter).rstrip(nest_delimiter).rstrip("\n")
        line = line.rstrip().lstrip()
        return line

    with open(data_file, "r", encoding="utf-8") as f:
        delimiter_count, moving = 0, 0
        for raw_line in f.readlines():
            to_left, to_right = (
                raw_line.rstrip(nest_delimiter).count(nest_delimiter),
                raw_line.rstrip(nest_delimiter)
                .lstrip(nest_delimiter)
                .count(nest_delimiter),
            )
            movement = to_left - to_right
            chrysalis = pyjson_chrysalis_transform(clean_line(raw_line))
            moving = movement - len(growth)  # Stages
            molting = growth.copy()
            if chrysalis:
                wrap = "}" * abs(moving)  # Stages or transformations
                while abs(moving):  # Transforming or evolving
                    if moving > 0:
                        molting.append(chrysalis)
                        cocoon += f'"{chrysalis}":' + "{"
                        moving -= 1
                    else:
                        molting.pop()
                        moving += 1
                cocoon += wrap
                if wrap:
                    cocoon += ","
                molting.append(chrysalis)
                cocoon += f'"{chrysalis}":' + "{"
                chrysalis_form.append(molting)
                growth = molting.copy()

        moving = 0 - len(growth)
        cocoon += "}" * abs(moving)
        pyjson = json.loads("{" + cocoon + "}")
        return pyjson

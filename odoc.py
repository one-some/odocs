import re

HTML_TEMPLATE_PATH = "html_template.html"

# Vars
in_text_block = False

child_types = {
    "p": "property",
    "m": "method"
}

# Define some helper functions

def err(text, line):
    print(f"Odoc Error on line {line}: {text}")
    exit(1)

# Begin parse
def parse(text):
    lines = text.split("\n")
    scope = None
    odoc = []
    in_text_block = False

    if not lines:
        err("Couldn't read lines. Is the file empty?", 1)

    if len(lines) > 2 and lines[1]:
        err("Second line must be empty!", 2)

    odoc.append({"type": "subject", "content": lines[0]})

    for line_num in range(len(lines)):
        line = lines[line_num]

        # Regex matching
        tag_match = re.match(r"<(.*)>", line)
        if not tag_match or not tag_match.group(1):
            if scope:
                if "content" in scope[-1]:
                    scope["children"][-1]["content"] += line
                else:
                    scope["children"][-1]["content"] = line
            continue

        tag_args = tag_match.group(1).split(":")
        if tag_args[0] == "end":
            print(f"Leaving scope on line {line_num}")
            scope = odoc
            continue
        if len(tag_args) == 2:
            # <type:name>
            if tag_args[0] == "class":
                print("class baby")
                odoc.append({
                    "type": "class",
                    "name": tag_args[1],
                    "children": [],
                    "content": ""
                })
                scope = odoc[-1]["children"]
            else:
                property_match = re.match(r"(p|m)(\[(.*)\])?", tag_args[0])
                if property_match:
                    #target = odoc
                    #if scope:
                    #    print("We think the target is scope.")
                    #    target = scope["children"]
                    #    #err("Child outside of scope!", line_num)
                    scope.append({
                        "type": child_types[property_match.group(1)],
                        "name": tag_args[1],
                        "content": "",
                        "return_type": None
                    })
                    if property_match.group(3):
                        print("yeah, things are changing")
                        target[-1]["return_type"] = property_match.group(3)
                else:
                    err(f"Unknown tag type {tag_args[0]}.", line_num)
            line = line.replace(tag_match.group(0), "")
            # in_text_block = True
    return odoc

def to_html(text):
    # Compose
    odoc = parse(text)
    print(odoc)
    html = ""

    for token in odoc:
        if token["type"] == "subject":
            html += f"<h1 class='subject'>{token['content']}</h1>"
        elif token["type"] == "class":
            html += "<div class='class'>"
            html += f"<span class='type'>class</span> <span>{token['name']}</span>"
            html += token["content"]
            for child in token["children"]:
                html += "<div class='property'>"
                type_html = ""
                if "return_type" in child:
                    type_html = f"<span class='{child['return_type']}'>{child['return_type']}</span> "
                html += f"<span class='type'>{child['type']}</span> <span>{type_html}{child['name']}</span><br>"
                html += child["content"]
                html += "</div>"
            html += "</div>"
        else:
            err(f"Unhtmlifyable token {token}!", "<htmlify>")
    with open(HTML_TEMPLATE_PATH, "r") as file:
        return file.read().replace("[REPLACE-ODOC-CONTENT]", html)

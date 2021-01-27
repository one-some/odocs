import re

HTML_TEMPLATE_PATH = "html_template.html"

# Vars
in_text_block = False

# Define some helper functions

def err(text, line):
    print(f"Odoc Error on line {line}: {text}")
    exit(1)

# Begin parse
def parse(text):
    lines = text.split("\n")
    odoc = []
    in_text_block = False

    if not lines:
        err("Couldn't read lines. Is the file empty?", 1)

    if len(lines) > 2 and lines[1]:
        err("Second line must be empty!", 2)

    for line_num in range(len(lines)):
        line = lines[line_num]
        tag_match = re.match(r"<(.*):(.*)>", line)
        if tag_match and tag_match.group(2):
            tag_type = tag_match.group(1)
            tag_name = tag_match.group(2)
            if tag_type == "class":
                print("class baby")
                odoc.append({
                    "type": "class",
                    "name": tag_name,
                    "content": ""
                })
            else:
                property_match = re.match(r"p(\[(.*)\])?", tag_type)
                if property_match:
                    odoc.append({
                        "type": "property",
                        "name": tag_name,
                        "content": ""
                    })
                    if property_match.group(2):
                        odoc[-1]["lang_type"] = property_match.group(2)
                else:
                    err(f"Unknown tag type {tag_type}.", line_num)
            line = line.replace(tag_match.group(0), "")
            in_text_block = True

        if in_text_block:
            if "content" in odoc[-1]:
                odoc[-1]["content"] += line
            else:
                odoc[-1]["content"] = line
    return odoc

def to_html(text):
    # Compose
    odoc = parse(text)
    html = ""

    for token in odoc:
        if token["type"] == "class":
            html += f"<h1>Class: {token['name']}</h1>"
            html += token["content"]
        elif token["type"] == "property":
            html += f"<h3>Property: {token['lang_type']} {token['name']}</h3>"
            html += token["content"]
        else:
            err(f"Unhtmlifyable token {token}!", "<htmlify>")
    with open(HTML_TEMPLATE_PATH, "r") as file:
        return file.read().replace("[REPLACE-ODOC-CONTENT]", html)

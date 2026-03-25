w = 42.450218
h = 31.545008

from lxml import etree
import glob
import os

file_pattern = "earthkit*-light.svg"
ns = {"svg": "http://www.w3.org/2000/svg"}

# Elements that can have fill/stroke
shape_tags = ["path", "rect", "circle", "ellipse", "line", "polygon", "polyline"]

for file_path in glob.glob(file_pattern):
    print(f"Processing {file_path}...")
    
    tree = etree.parse(file_path)
    root = tree.getroot()
    
    paths_to_remove = root.xpath("//svg:path[@aria-label]", namespaces=ns)
    
    for path in paths_to_remove:
        parent = path.getparent()
        parent.remove(path)

    root.set("width", str(w))
    root.set("height", str(h))
    root.set("viewBox", f"0 0 {w} {h}")

    new_file_path = file_path.replace("-light", "-notext")
    tree.write(new_file_path, pretty_print=True)

    # make all other shapes grey by setting stroke and fill to currentColor
    for tag in shape_tags:
        for elem in root.xpath(f"//svg:{tag}", namespaces=ns):
            # Update stroke if it exists and is not 'none'
            stroke = elem.get("stroke")
            if stroke and stroke.lower() != "none":
                elem.set("stroke", "currentColor")
            
            # Update fill if it exists and is not 'none'
            fill = elem.get("fill")
            if fill and fill.lower() != "none":
                elem.set("fill", "currentColor")

            # Replace stroke/fill in inline style if they exist and are not 'none'
            style = elem.get("style")
            if style:
                style_items = style.split(";")
                new_style_items = []
                for item in style_items:
                    if not item.strip():
                        continue
                    key, _, value = item.partition(":")
                    key = key.strip()
                    value = value.strip()
                    if key in ("stroke", "fill") and value.lower() != "none":
                        value = "currentColor"
                    new_style_items.append(f"{key}:{value}")
                elem.set("style", ";".join(new_style_items))

    new_file_path = file_path.replace("-light", "-grey")
    tree.write(new_file_path, pretty_print=True)
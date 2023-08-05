import os


START_TEMPLATE = """<!DOCTYPE RCC><RCC version="1.0">
    <qresource prefix="/">
"""

END_TEMPLATE = """    </qresource>
</RCC>
"""

ITEM_TEMPLATE = """        <file>{}</file>
"""

data = [
    os.path.join(dir_, filename)
    for dir_, dir_names, file_names in os.walk(os.path.join("resources"))
    for filename in file_names
    if "qmlc" not in filename
]

with open("plugin.qrc", "w") as file:
    file.write(START_TEMPLATE)
    for path in data:
        file.write(ITEM_TEMPLATE.format(path))
    file.write(END_TEMPLATE)


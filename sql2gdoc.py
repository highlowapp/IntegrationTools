import sys
import re
from docx import Document

sql_file = open(sys.argv[1], "r")
sql_code = sql_file.read()
sql_file.close()

#Split into individual lines
lines = sql_code.split("\n")

sql_statements = []

for i in range(len(lines)):
    lines[i] = lines[i].strip()

    if len(lines[i]) == 0:
        continue
    elif lines[i][0:2] == '--':
        continue
    else:
        sql_statements.append(lines[i])

tables = []

for i in range(len(sql_statements)):
    #Get the table information

    table = {
        "name": "",
        "columns": []
    }

    #Name
    table["name"] = sql_statements[i][13:sql_statements[i].index('(')]

    regex = re.compile(r"[\(\)]")

    #Columns
    columns_string = regex.split(sql_statements[i])[1]
    columns_list = columns_string.split(",")



    for i in columns_list:
        components = i.split(" ")

        column_name = components[1]

        column_type = components[2:len(components)]

        column_dict = {
            "name": column_name,
            "type": " ".join(column_type)
        }

        table["columns"].append(column_dict)

    tables.append(table)



#Write to a document
document = Document()

style = document.styles["Normal"]
style.font.name = "Consolas"

#Loop through tables and fill in the data
for i in range(len(tables)):
    paragraph_str = ""

    paragraph_str += "Name: " + tables[i]["name"] + "\n\n"

    max_column_name_length = 0
    max_column_type_length = 0
    for j in range(len(tables[i]["columns"])):
        if len(tables[i]["columns"][j]["name"]) > max_column_name_length:
            max_column_name_length = len(tables[i]["columns"][j]["name"])
        if len(tables[i]["columns"][j]["type"]) > max_column_type_length:
            max_column_type_length = len(tables[i]["columns"][j]["type"])


    paragraph_str += "-" * (7 + max_column_name_length + max_column_type_length) + "\n"

    for j in range(len(tables[i]["columns"])):
        paragraph_str += "| " + tables[i]["columns"][j]["name"] + ( " " * (max_column_name_length - len(tables[i]["columns"][j]["name"])) ) + " | "
        paragraph_str += tables[i]["columns"][j]["type"] + (" " * (max_column_type_length - len(tables[i]["columns"][j]["type"])) ) + " |\n"

        paragraph_str += "-" * (7 + max_column_name_length + max_column_type_length) + "\n"
    document.add_paragraph(paragraph_str)
document.save("MySQL Tables.docx")
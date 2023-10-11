import os


def convert_table_to_tabs(table_content, file_name_without_extension):
    lines = table_content.strip().split("\n")
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = [[cell.strip() for cell in row.split("|")[1:-1]] for row in lines[2:]]

    if len(headers) <= 2:
        return table_content

    tabs = []
    for index, header in enumerate(headers[1:], start=1):
        tab = []
        tab.append(f"| {headers[0]} | {header} | Image |")
        tab.append("| --- | --- | --- |")

        for row in rows:
            first_col = row[0]
            cell_content = row[index]
            new_cell = f"[{cell_content}](/everycase/{cell_content[:5]})"
            image_cell = f"![{first_col} Case](/everyphone/{cell_content[:5]}.png)"
            tab.append(f"| {first_col} | {new_cell} | {image_cell} |")

            # Creating the everycase file for this SKU
            with open(f"pages/everycase/{cell_content[:5]}.md", "w") as sku_file:
                sku_file_content = (
                    f"# {header} {headers[0]} - {first_col}\n\n"
                    f"[Return to previous page](/{file_name_without_extension})\n\n"
                    f"[High-resolution image from Apple](https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is//{cell_content[:5]}?wid=4500&hei=4500&fmt=png)\n\n"
                    f"# {image_cell}\n\n"
                    "## Under construction\n"
                )
                sku_file.write(sku_file_content)

        tabs.append("\n".join(tab))

    previous_headers = ""
    formatted_headers = []
    for header in headers[1:]:
        if "iPhone" in header and "iPhone" in previous_headers:
            formatted_headers.append(header.replace("iPhone ", ""))
        elif "iPad" in header and "iPad" in previous_headers:
            formatted_headers.append(header.replace("iPad ", ""))
        else:
            formatted_headers.append(header)
            previous_headers += header + " "

    # Formatting the output
    header_items = ", ".join([f"'{header}'" for header in formatted_headers])
    all_tabs = "\n\n".join([f"<Tabs.Tab>\n\n{tab}\n\n</Tabs.Tab>" for tab in tabs])
    final_output = f"<Tabs\n  items={{[{header_items}]}}>\n\n{all_tabs}\n</Tabs>"

    return final_output


def extract_tables_from_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    tables = []
    current_table = []
    in_table = False

    for line in lines:
        if line.startswith("|"):
            in_table = True
            current_table.append(line.strip())
        else:
            if in_table:
                tables.append("\n".join(current_table))
                current_table = []
                in_table = False

    # Handling the case where the file ends with a table
    if current_table:
        tables.append("\n".join(current_table))

    return tables


def convert_and_print_tables(filename):
    tables = extract_tables_from_file(filename)
    for i, table in enumerate(tables, start=1):
        converted_table = convert_table_to_tabs(table)
        print(f"Converted Table {i}:\n")
        print(converted_table)
        print("=" * 40)


def convert_and_save_to_mdx(input_filename, output_filename):
    file_name_without_extension = os.path.basename(input_filename).replace(".md", "")
    with open(input_filename, "r") as f:
        content = f.read()

    tables = extract_tables_from_file(input_filename)
    for table in tables:
        converted_table = convert_table_to_tabs(table, file_name_without_extension)
        content = content.replace(table, converted_table)

    content = 'import { Tabs } from "nextra/components";\n\n' + content

    with open(output_filename, "w") as f:
        f.write(content)


# Test
input_filename = "trash/pages/iphone_15.md"
output_filename = input_filename.replace(
    ".md", ".mdx"
)  # replace .md extension with .mdx
convert_and_save_to_mdx(input_filename, output_filename)

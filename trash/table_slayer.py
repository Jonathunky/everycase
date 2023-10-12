import os
import re


def convert_table_to_tabs(
    table_content, file_name_without_extension, generate_everycase=True
):
    lines = table_content.strip().split("\n")
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = [[cell.strip() for cell in row.split("|")[1:-1]] for row in lines[2:]]

    if len(headers) == 2:
        new_table = []
        new_table.append(f"| {headers[0]} | {headers[1]} | Image |")
        new_table.append("| --- | --- | --- |")

        for row in rows:
            first_col = row[0]
            cell_content = row[1]
            new_cell = f"[{cell_content}](/everycase/{cell_content[:5]})"
            image_cell = (
                f"![{first_col} {headers[0]}](/everyphone/{cell_content[:5]}.png)"
            )
            new_table.append(f"| {first_col} | {new_cell} | {image_cell} |")

            if generate_everycase:
                with open(f"pages/everycase/{cell_content[:5]}.md", "w") as sku_file:
                    match = re.search(r"iPhone (\d+)", headers[1])
                    if match:
                        iphone_number = int(match.group(1))
                        if iphone_number >= 12:
                            new_header = f"# {headers[1]} {headers[0]} with MagSafe - {first_col}\n\n"
                        else:
                            new_header = (
                                f"# {headers[1]} {headers[0]} - {first_col}\n\n"
                            )
                    else:
                        new_header = f"# {headers[1]} {headers[0]} - {first_col}\n\n"

                    sku_file_content = (
                        f"{new_header}"
                        f"[Return to previous page](/{file_name_without_extension})\n\n"
                        f"[High-resolution image from Apple](https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{cell_content[:5]}?wid=4500&hei=4500&fmt=png)\n\n"
                        f'<div style="width: 500px">'
                        f'<img src="/everyphone/{cell_content[:5]}.png" alt="{first_col}">'
                        "</div>\n\n"
                        "## Under construction\n"
                    )
                    sku_file.write(sku_file_content)
        return "\n".join(new_table)

    tabs = []
    for index, header in enumerate(headers[1:], start=1):
        tab = []
        tab.append(f"| {headers[0]} | {header} | Image |")
        tab.append("| --- | --- | --- |")

        for row in rows:
            first_col = row[0]
            cell_content = row[index]
            new_cell = f"[{cell_content}](/everycase/{cell_content[:5]})"
            image_cell = (
                f"![{first_col} {headers[0]}](/everyphone/{cell_content[:5]}.png)"
            )
            tab.append(f"| {first_col} | {new_cell} | {image_cell} |")

            # Creating the everycase file for this SKU
            if generate_everycase:
                with open(f"pages/everycase/{cell_content[:5]}.md", "w") as sku_file:
                    match = re.search(r"iPhone (\d+)", headers[1])
                    if match:
                        iphone_number = int(match.group(1))
                        if iphone_number >= 12:
                            new_header = f"# {headers[1]} {headers[0]} with MagSafe - {first_col}\n\n"
                        else:
                            new_header = (
                                f"# {headers[1]} {headers[0]} - {first_col}\n\n"
                            )
                    else:
                        new_header = f"# {headers[1]} {headers[0]} - {first_col}\n\n"

                    sku_file_content = (
                        f"{new_header}"
                        f"[Return to previous page](/{file_name_without_extension})\n\n"
                        f"[High-resolution image from Apple](https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{cell_content[:5]}?wid=4500&hei=4500&fmt=png)\n\n"
                        f'<div style="width: 500px">'
                        f'<img src="/everyphone/{cell_content[:5]}.png" alt="{first_col}">'
                        "</div>\n\n"
                        "## Under construction\n"
                    )
                    sku_file.write(sku_file_content)

        tabs.append("\n".join(tab))

    previous_headers = ""
    formatted_headers = []
    for header in headers[1:]:
        if "iPhone" in header and "iPhone" in previous_headers and len(headers) > 3:
            formatted_headers.append(header.replace("iPhone ", ""))
        elif "iPad" in header and "iPad" in previous_headers and len(headers) > 3:
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


def process_directory(directory_path, generate_mdx=True, generate_everycase=True):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):
                input_filename = os.path.join(root, file)
                output_filename = os.path.join("pages", file + "x")
                convert_and_save_to_mdx(
                    input_filename, output_filename, generate_mdx, generate_everycase
                )


def convert_and_save_to_mdx(
    input_filename, output_filename, generate_mdx=True, generate_everycase=True
):
    file_name_without_extension = os.path.basename(input_filename).replace(".md", "")
    with open(input_filename, "r") as f:
        content = f.read()

    tables = extract_tables_from_file(input_filename)
    for table in tables:
        converted_table = convert_table_to_tabs(
            table, file_name_without_extension, generate_everycase
        )
        content = content.replace(table, converted_table)

    if generate_mdx:
        content = 'import { Tabs } from "nextra/components";\n\n' + content
        with open(output_filename, "w") as f:
            f.write(content)


# Test
directory_path = "trash/pages"
process_directory(directory_path, generate_mdx=True, generate_everycase=True)

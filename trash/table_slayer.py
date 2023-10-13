import os
import re


def generate_sku_file_content(
    header, head, first_col, cell_content, file_name_without_extension
):
    match = re.search(r"iPhone (\d+)", header)
    if match:
        iphone_number = int(match.group(1))
        if iphone_number >= 12:
            new_header = f"# {header} {head} with MagSafe - {first_col}\n\n"
        else:
            new_header = f"# {header} {head} - {first_col}\n\n"
    else:
        new_header = f"# {header} {head} - {first_col}\n\n"

    return (
        f"{new_header}"
        f"[Return to previous page](/{file_name_without_extension})\n\n"
        f"[High-resolution image from Apple](https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{cell_content[:5]}?wid=4500&hei=4500&fmt=png)\n\n"
        f'<div style="width: 512px">'
        f'<img src="/almost_uncompressed/{cell_content[:5]}.webp" alt="{first_col}">'
        "</div>\n\n"
        "## Under construction\n"
    )


KEYWORDS = ["iPhone", "iPad", "AirTag", "Apple Pencil", "MacBook"]


def generate_tab_or_table(
    headers, rows, generate_everycase, file_name_without_extension
):
    table = []

    if any(keyword in headers[0].strip() for keyword in KEYWORDS):
        table.append(
            f"| {headers[1]} | {headers[0]} | Image |"
        )  # "for iPhone..." could be done here
        heading = headers[1]
    else:
        table.append(f"| {headers[0]} | {headers[1]} | Image |")
        heading = headers[0]

    table.append("| --- | --- | --- |")

    for row in rows:
        first_col = row[0]
        cell_content = row[1]
        new_cell = (
            f"[{cell_content}](/{file_name_without_extension}/{cell_content[:5]})"
        )
        image_cell = f"![{first_col} {heading}](/everyphone/{cell_content[:5]}.png)"
        table.append(f"| {first_col} | {new_cell} | {image_cell} |")

        if generate_everycase:
            directory = f"pages/{file_name_without_extension}"

            # Create directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            with open(f"{directory}/{cell_content[:5]}.md", "w") as sku_file:
                if any(keyword in headers[0].strip() for keyword in KEYWORDS):
                    sku_file_content = generate_sku_file_content(
                        headers[0],
                        headers[1],
                        first_col,
                        cell_content,
                        file_name_without_extension,
                    )
                else:
                    sku_file_content = generate_sku_file_content(
                        headers[1],
                        headers[0],
                        first_col,
                        cell_content,
                        file_name_without_extension,
                    )

                sku_file.write(sku_file_content)

    return table


def convert_table_to_tabs(
    table_content, file_name_without_extension, generate_everycase=True
):
    lines = table_content.strip().split("\n")

    headers = [h.strip() for h in lines[0].split("|")[1:-1]]

    rows = [[cell.strip() for cell in row.split("|")[1:-1]] for row in lines[2:]]

    # If cell 1:1 contains the word "Item", return the table directly
    if "Item" in headers[0]:
        return table_content

    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = [[cell.strip() for cell in row.split("|")[1:-1]] for row in lines[2:]]

    if len(headers) == 2:
        return "\n".join(
            generate_tab_or_table(
                headers, rows, generate_everycase, file_name_without_extension
            )
        )

    tabs = []
    for index, header in enumerate(headers[1:], start=1):
        current_header = [headers[0], header]
        current_rows = [[row[0], row[index]] for row in rows]
        tabs.append(
            "\n".join(
                generate_tab_or_table(
                    current_header,
                    current_rows,
                    generate_everycase,
                    file_name_without_extension,
                )
            )
        )

    formatted_headers = []
    previous_headers = ""
    for header in headers[1:]:
        if "iPhone" in header and "iPhone" in previous_headers and len(headers) > 3:
            formatted_headers.append(header.replace("iPhone ", ""))
        elif "iPad" in header and "iPad" in previous_headers and len(headers) > 3:
            formatted_headers.append(header.replace("iPad ", ""))
        else:
            formatted_headers.append(header)
            previous_headers += header + " "

    header_items = ", ".join([f"'{header}'" for header in formatted_headers])
    all_tabs = "\n\n".join([f"<Tabs.Tab>\n\n{tab}\n\n</Tabs.Tab>" for tab in tabs])

    return f"<Tabs\n  items={{[{header_items}]}}>\n\n{all_tabs}\n</Tabs>"


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

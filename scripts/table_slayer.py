import os
import re
import json
import concurrent.futures

# Read the SKUs from the file and store them in a set
with open("trash/skus.txt", "r") as file:
    extended_skus = set(file.read().splitlines())


def get_extended_sku(original_sku):
    """Searches for the extended SKU in the cache and returns it.
    If not found, returns the original SKU."""

    # Search for a SKU that starts with the original SKU
    for sku in extended_skus:
        if sku.startswith(original_sku):
            return sku

    # If no extended SKU is found in the cache, return the original SKU
    return original_sku


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
        f'<div style="width: 384px">'
        f'<img src="/everypreview/{cell_content[:5]}.png" alt="{first_col}">'  # almost_uncompressed
        "</div>\n\n"
        "### Under construction\n"
    )


def write_meta_to_file(folder_path):
    data = {
        "*": {
            "theme": {
                "pagination": False,
                "toc": True,
                "breadcrumb": True,
                "typesetting": "article",
                "footer": False,
                "sidebar": True,
                "layout": "full",
            },
            "display": "hidden",
        }
    }

    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Create the full path to the _meta.json file
    file_path = os.path.join(folder_path, "_meta.json")

    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


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
        new_cell = f"[{cell_content[:5]}<wbr/>{cell_content[5:]}](/{file_name_without_extension}/{cell_content[:5]})"
        image_cell = f"![{first_col} {heading}](/everypreview/{get_extended_sku(cell_content[:5])}.png)"
        table.append(f"| {first_col} | {new_cell} | {image_cell} |")

        if generate_everycase:
            directory = f"pages/{file_name_without_extension}"
            write_meta_to_file(directory)

            # Create directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            if cell_content[:5].strip():  # suspicious check
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


def process_single_file(file_info):
    root, file, generate_mdx, generate_everycase = file_info
    if file.endswith(".md"):
        input_filename = os.path.join(root, file)
        output_filename = os.path.join("pages", file + "x")
        convert_and_save_to_mdx(
            input_filename, output_filename, generate_mdx, generate_everycase
        )


def replace_mdx_content(filename):
    with open(filename, "r") as file:
        content = file.read()

        # Check if the patterns are present
        if (
            "SPLIT_TABLE_1" in content
            and "SPLIT_TABLE_2" in content
            and "SPLIT_TABLE_END" in content
        ):
            # Extract the blocks of content
            split_table_1_content = re.search(
                'SPLIT_TABLE_1 = "(.*?)"\n\n(.*?)\n\nSPLIT_TABLE_2', content, re.DOTALL
            ).group(2)
            split_table_2_content = re.search(
                'SPLIT_TABLE_2 = "(.*?)"\n\n(.*?)\n\nSPLIT_TABLE_END',
                content,
                re.DOTALL,
            ).group(2)
            table_1_title = re.search('SPLIT_TABLE_1 = "(.*?)"', content).group(1)
            table_2_title = re.search('SPLIT_TABLE_2 = "(.*?)"', content).group(1)

            new_content = f"""<Tabs items={{['{table_1_title}', '{table_2_title}']}}>
              <Tabs.Tab>
            {split_table_1_content}
            </Tabs.Tab>
              <Tabs.Tab>
            {split_table_2_content}
            </Tabs.Tab>
            </Tabs>"""

            # Replace the old block with the new Tabs syntax
            content = re.sub(
                "SPLIT_TABLE_1.*?SPLIT_TABLE_END", new_content, content, flags=re.DOTALL
            )

            # Save the changes
            with open(filename, "w") as file:
                file.write(content)


def process_directory(directory_path, generate_mdx=True, generate_everycase=True):
    file_infos = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_infos.append((root, file, generate_mdx, generate_everycase))

    # Process files in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_single_file, file_infos)

    for root, dirs, files in os.walk("pages"):
        for file in files:
            if file.endswith(".mdx"):
                replace_mdx_content(os.path.join(root, file))


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
        with open(
            input_filename.replace("trash/layout/", "trash/pages/"), "r"
        ) as md_file:
            content = (
                'import { Tabs } from "nextra/components";\n\n'
                + md_file.read()
                + "\n"
                + content
            )
        with open(output_filename, "w") as f:
            f.write(content)


if __name__ == "__main__":
    directory_path = "trash/layout"
    process_directory(directory_path, generate_mdx=True, generate_everycase=True)
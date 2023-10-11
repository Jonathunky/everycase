import os
import sys


def append_to_models_file(sku):
    with open("models.txt", "a") as f:
        f.write(sku[:5] + "\n")


def process_sku(sku):
    if sku.endswith(("ZM/A", "LL/A", "AM/A")):
        short_sku = sku[:5]
        append_to_models_file(short_sku)
        return f"[{sku}](/everycase/{short_sku})"
    return sku


def split_table(table_str):
    rows = table_str.strip().split("\n")
    headers = rows[0].split("|")[1:-1]  # Exclude the first and last empty items
    if len(headers) < 3:
        return None, None  # Skip tables with only two columns

    # Create tabs header with reduced redundancy
    base_name = headers[1].strip()
    tab_items = [base_name]  # Start with the first name
    for h in headers[2:]:
        tab_items.append(h.replace(base_name, "").strip())

    tabs_header = f"<Tabs\n  items={{{str(tab_items)}}}\n>"

    new_tables = []
    for h in tab_items:
        new_table_rows = [f"| {headers[0]} | {h} | Image |", "| --- | --- | --- |"]
        for row in rows[2:]:
            values = row.split("|")[1:-1]
            if len(values) < 2:  # Safety check
                continue
            processed_sku = process_sku(values[1].strip())
            sku_part = values[1].strip()[
                :5
            ]  # Extract the first 5 characters for the SKU part
            new_row = f"| {values[0]} | {processed_sku} | ![Image](/everyphone/{sku_part}.png) |"
            new_table_rows.append(new_row)
        new_table_content = "\n".join(new_table_rows)
        new_table_wrapped = f"<Tabs.Tab>\n\n{new_table_content}\n\n</Tabs.Tab>"
        new_tables.append(new_table_wrapped)

    return tabs_header, new_tables


def process_md_file(input_file, output_folder):
    with open(input_file, "r") as file:
        content = file.read()

    new_content = (
        'import { Tabs } from "nextra/components";\n\n'  # Add the import statement
    )

    tables = content.split("\n\n")
    for i, table in enumerate(tables):
        if "|" in table:
            tabs_header, wrapped_tables = split_table(table)
            if (
                tabs_header and wrapped_tables
            ):  # Check if they're not None (for skipped tables)
                tabs_content = (
                    tabs_header + "\n\n" + "\n\n".join(wrapped_tables) + "\n</Tabs>"
                )
                new_content += tabs_content + "\n\n"
            else:
                new_content += table + "\n\n"  # For skipped tables
        else:
            new_content += table + "\n\n"

    output_file = os.path.join(
        output_folder, os.path.basename(input_file).replace(".md", ".mdx")
    )
    with open(output_file, "w") as file:
        file.write(new_content)


def process_single_file(filepath):
    print(f"Processing {filepath}...")
    try:
        process_md_file(filepath, os.path.dirname(filepath))
        print(f"Processed {filepath} and saved as {filepath.replace('.md', '.mdx')}.")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")


def process_folder(folder_name):
    for filename in os.listdir(folder_name):
        if filename.endswith(".md"):
            full_path = os.path.join(folder_name, filename)
            process_single_file(full_path)


if __name__ == "__main__":
    path = input("Enter the path to the file or directory: ")
    if os.path.isfile(path):
        process_single_file(path)
    elif os.path.isdir(path):
        process_folder(path)
    else:
        print("Error: The provided path is neither a file nor a directory.")

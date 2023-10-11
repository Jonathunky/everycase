import os
import re


def append_to_models_txt(sku):
    with open("models.txt", "a+") as model_file:
        model_file.write(sku + "\n")


def split_table(table_str):
    rows = table_str.strip().split("\n")
    headers = rows[0].split("|")[1:-1]
    if len(headers) < 3:
        return None, None

    base_name = headers[0].strip()
    tab_items = headers[1:]

    tabs_header = f"<Tabs\n  items={{{str(tab_items)}}}\n>"

    new_tables = []
    for idx, h in enumerate(tab_items):
        new_table_rows = [f"| {base_name} | {h} | Image |", "| --- | --- | --- |"]
        for row in rows[2:]:
            values = row.split("|")[1:-1]
            if idx + 1 < len(values):
                sku_part = values[idx + 1].strip()[:5]
                new_row = f"| {values[0]} | {values[idx+1]} | ![Image](/everyphone/{sku_part}.png) |"
                new_table_rows.append(new_row)
                append_to_models_txt(sku_part)
                phone_model = values[0].strip()
                image_link = f"/everyphone/{sku_part}.png"
                generate_individual_md(
                    sku_part, phone_model, h, image_link, "individual"
                )

        new_tables.append("\n".join(new_table_rows))

    return tabs_header, new_tables


def process_md_file(input_file, output_folder):
    with open(input_file, "r") as file:
        content = file.read()

    new_content = 'import { Tabs } from "nextra/components";\n\n'

    tables = content.split("\n\n")
    for i, table in enumerate(tables):
        if "|" in table:
            tabs_header, wrapped_tables = split_table(table)
            if tabs_header and wrapped_tables:
                tabs_content = (
                    tabs_header + "\n\n" + "\n\n".join(wrapped_tables) + "\n</Tabs>"
                )
                new_content += tabs_content + "\n\n"
            else:
                new_content += table + "\n\n"
        else:
            new_content += table + "\n\n"

    output_file_mdx = os.path.join(
        output_folder, os.path.basename(input_file).replace(".md", ".mdx")
    )
    with open(output_file_mdx, "w") as file:
        file.write(new_content)


def generate_individual_md(sku, phone_model, case_name, image_link, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    md_filename = os.path.join(output_folder, f"{sku}.md")
    with open(md_filename, "w") as md_file:
        md_file.write(f"# {phone_model} {case_name}\n")
        md_file.write(f"![Image]({image_link})\n")


def process_folder(folder_path):
    output_folder = os.path.join(folder_path, "converted")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            process_md_file(os.path.join(folder_path, file), output_folder)


if __name__ == "__main__":
    folder_name = input("Enter folder path: ")
    process_folder(folder_name)

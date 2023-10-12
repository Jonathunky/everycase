import os


def convert_tables_to_tabs(tables):
    # Extract tab names
    tab_names = [table[0].split("|")[1].strip() for table in tables]

    tabs_content = []

    for table in tables:
        tabs_content.append("\n".join(table))

    final_output = f"<Tabs\n  items={{['{tab_names[0]}', '{tab_names[1]}']}}>\n\n"

    for tab in tabs_content:
        final_output += f"<Tabs.Tab>\n\n{tab}\n\n</Tabs.Tab>\n\n"

    final_output += "</Tabs>"

    return final_output


def extract_target_tables_from_file(filename):
    with open(filename, "r") as f:
        content = f.read()

    parts = content.split("\nmerge\n")

    if len(parts) != 2:
        raise ValueError(
            "The file should contain two target tables separated by the word 'merge' on its own line!"
        )

    # Identify tables using a more robust approach
    def get_table(lines):
        table_lines = []
        delimiter_found = False

        while lines and (lines[-1].startswith("|") or not delimiter_found):
            if "| ---" in lines[-1]:
                delimiter_found = True
            table_lines.insert(0, lines.pop())

        return table_lines if delimiter_found else []

    lines_before_merge = parts[0].split("\n")
    lines_after_merge = parts[1].split("\n")

    upper_table = get_table(lines_before_merge)
    lower_table = get_table(lines_after_merge)

    pre_merge_content = "\n".join(lines_before_merge)
    post_merge_content = "\n".join(lines_after_merge)

    if not upper_table or not lower_table:
        raise ValueError("Could not extract the tables properly from the content.")

    return upper_table, lower_table, pre_merge_content, post_merge_content


# ... rest of the script remains the same ...


def tabify_markdown_file(input_file, output_file):
    (
        upper_table,
        lower_table,
        pre_merge_content,
        post_merge_content,
    ) = extract_target_tables_from_file(input_file)
    tabified_content = convert_tables_to_tabs([upper_table, lower_table])

    full_content = (
        pre_merge_content + "\n\n" + tabified_content + "\n\n" + post_merge_content
    )

    with open(output_file, "w") as f:
        f.write(full_content)


if __name__ == "__main__":
    input_file = "a.mdx"
    output_file = input("Enter the path to save the output: ")

    tabify_markdown_file(input_file, output_file)
    print(f"Processed {input_file} and saved output to {output_file}!")

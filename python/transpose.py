import os


def transpose_table(table):
    # Remove the separator line before transposing
    actual_table = table[:1] + table[2:]
    return list(zip(*actual_table))


def format_table_for_md(table):
    md_table = []

    # First row - Headers
    md_table.append("| " + " | ".join(table[0]) + " |")

    # Separator row based on header sizes
    separator_row = ["-" * len(cell.strip()) for cell in table[0]]

    # If the first cell of the original table is empty
    if not table[0][0].strip():
        # Add a separator for the empty cell
        separator_row[0] = "-" * (len(separator_row[1]) - 2)

    md_table.append("| " + " | ".join(separator_row) + " |")

    # Remaining rows
    for row in table[1:]:
        md_table.append("| " + " | ".join(row) + " |")

    return "\n".join(md_table)


def transpose_tables_in_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    new_lines = []
    table_in_progress = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("|"):
            table_in_progress.append(stripped_line.split("|")[1:-1])
        else:
            if table_in_progress:
                transposed = transpose_table(table_in_progress)
                new_lines.extend(format_table_for_md(transposed).split("\n"))
                table_in_progress = []
            new_lines.append(stripped_line)

    if table_in_progress:
        transposed = transpose_table(table_in_progress)
        new_lines.extend(format_table_for_md(transposed).split("\n"))

    with open(file_path, "w") as file:
        file.write("\n".join(new_lines))


def process_folder(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith((".mdx", ".md")):
                file_path = os.path.join(root, filename)
                transpose_tables_in_file(file_path)


if __name__ == "__main__":
    import sys

    directory_path = sys.argv[1]
    process_folder(directory_path)

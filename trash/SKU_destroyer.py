import os
import re
from collections import defaultdict


def extract_models_from_md(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Regular expression to match table rows and columns
    row_pattern = re.compile(r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|")

    # Extracting the table headers
    headers_match = re.search(r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|", content)
    if not headers_match:
        return defaultdict(list)

    header1, header2 = headers_match.groups()
    header1 = (
        header1.lower()
        .replace(" ", "-")
        .replace("|", "-")
        .replace("/", "-")
        .replace("\\", "-")
    )
    header2 = (
        header2.lower()
        .replace(" ", "-")
        .replace("|", "-")
        .replace("/", "-")
        .replace("\\", "-")
    )

    models = defaultdict(list)
    for match in row_pattern.findall(content):
        column1, column2 = match
        # Checking if the cell value is a model number
        if "ZM/A" in column1:
            models[header1].append(column1.split("ZM/A")[0])
        if "ZM/A" in column2:
            models[header2].append(column2.split("ZM/A")[0])

    return models


def process_directory(directory):
    grouped_models = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                extracted_models = extract_models_from_md(file_path)
                for header, models in extracted_models.items():
                    grouped_models[header].extend(models)

    with open("models_output.txt", "w", encoding="utf-8") as output_file:
        for header, models in grouped_models.items():
            output_file.write(f"{header}:\n" + "\n".join(models) + "\n\n")

    print("Models have been extracted to models_output.txt.")


if __name__ == "__main__":
    directory = input(
        "Please provide the path to the directory with .md files: "
    ).strip()
    process_directory(directory)

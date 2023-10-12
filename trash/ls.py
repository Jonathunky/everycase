import os


def list_markdown_files(directory, output_file="models.txt"):
    # List all files in the directory
    all_files = os.listdir(directory)

    # Filter out the markdown files and remove the extension
    md_files = [os.path.splitext(file)[0] for file in all_files if file.endswith(".md")]

    with open(output_file, "w") as f:
        f.write("everyphone:\n")
        for file_name in md_files:
            f.write(file_name + "\n")

    # Join file names with a newline and return
    return "\n".join(md_files)


# Example usage:
directory_path = "./pages/everycase"  # Replace with your folder path
list_markdown_files(directory_path)

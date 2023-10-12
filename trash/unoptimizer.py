import re


def replace_md_images_with_html(content):
    # Regular expression pattern to identify markdown images
    pattern = r"!\[([^]]*)\]\(([^)]+)\)"  # Group 1: alt text, Group 2: image link

    # Function to perform replacement for each match
    def repl(matchobj):
        alt_text = matchobj.group(1)
        link = matchobj.group(2)
        return f'<img src="{link}" alt="{alt_text}"/>'

    # Substitute using the pattern and replacement function
    return re.sub(pattern, repl, content)


def process_markdown_file(file_path):
    # Read the markdown file content
    with open(file_path, "r") as file:
        content = file.read()

    # Replace markdown images with HTML img tags
    new_content = replace_md_images_with_html(content)

    # Save the converted content back to the file
    with open(file_path, "w") as file:
        file.write(new_content)


if __name__ == "__main__":
    file_path = input("Enter the path to the Markdown file: ")
    process_markdown_file(file_path)
    print(f"Processed {file_path} successfully!")

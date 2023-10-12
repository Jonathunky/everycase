import re


def replace_html_img_with_md(content):
    # Regular expression pattern to identify <img> tags
    pattern = (
        r'<img src="([^"]+)" alt="([^"]*)"/>'  # Group 1: image link, Group 2: alt text
    )

    # Function to perform replacement for each match
    def repl(matchobj):
        link = matchobj.group(1)
        alt_text = matchobj.group(2)
        return f"![{alt_text}]({link})"

    # Substitute using the pattern and replacement function
    return re.sub(pattern, repl, content)


def process_html_file(file_path):
    # Read the HTML file content
    with open(file_path, "r") as file:
        content = file.read()

    # Replace <img> tags with markdown images
    new_content = replace_html_img_with_md(content)

    # Save the converted content back to the file
    with open(file_path, "w") as file:
        file.write(new_content)


if __name__ == "__main__":
    file_path = input("Enter the path to the HTML or Markdown file with <img> tags: ")
    process_html_file(file_path)
    print(f"Processed {file_path} successfully!")

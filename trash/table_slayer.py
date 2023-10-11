import re


def convert_table_to_tabs(table_content):
    # Parsing headers and rows from the table content
    lines = table_content.strip().split("\n")
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = [[cell.strip() for cell in row.split("|")[1:-1]] for row in lines[2:]]

    if len(headers) <= 2:
        return table_content

    # Creating Tabs
    tabs = []
    for index, header in enumerate(headers[1:]):
        tab = []
        tab.append(f"| {headers[0]} | {header} | Image |")
        tab.append("| --- | --- | --- |")

        for row in rows:
            first_col = row[0]
            cell_content = row[index + 1]
            new_cell = f"[{cell_content}](/everycase/{cell_content[:5]})"
            image_cell = f"![Image](/everyphone/{cell_content[:5]}.png)"
            tab.append(f"| {first_col} | {new_cell} | {image_cell} |")

        tabs.append("\n".join(tab))

    # Formatting the output
    header_items = ", ".join([f"'{header}'" for header in headers[1:]])
    all_tabs = "\n\n".join([f"<Tabs.Tab>\n\n{tab}\n\n</Tabs.Tab>" for tab in tabs])
    final_output = f"<Tabs\n  items={[{header_items}]}\n>\n\n{all_tabs}\n</Tabs>"

    return final_output


# Test
table_content = """
| Silicone Case | iPhone 15 | iPhone 15 Plus | iPhone 15 Pro | iPhone 15 Pro Max |
| ------------- | --------- | -------------- | ------------- | ----------------- |
| Black         | MT0J3ZM/A | MT103ZM/A      | MT1A3ZM/A     | MT1M3ZM/A         |
| Storm Blue    | MT0N3ZM/A | MT123ZM/A      | MT1D3ZM/A     | MT1P3ZM/A         |
| Clay          | MT0Q3ZM/A | MT133ZM/A      | MT1E3ZM/A     | MT1Q3ZM/A         |
| Light Pink    | MT0U3ZM/A | MT143ZM/A      | MT1F3ZM/A     | MT1U3ZM/A         |
| Guava         | MT0V3ZM/A | MT163ZM/A      | MT1G3ZM/A     | MT1V3ZM/A         |
| Orange Sorbet | MT0W3ZM/A | MT173ZM/A      | MT1H3ZM/A     | MT1W3ZM/A         |
| Cypress       | MT0X3ZM/A | MT183ZM/A      | MT1J3ZM/A     | MT1X3ZM/A         |
| Winter Blue   | MT0Y3ZM/A | MT193ZM/A      | MT1L3ZM/A     | MT1Y3ZM/A         |
"""
print(convert_table_to_tabs(table_content))

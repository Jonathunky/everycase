def sort_table_columns(table):
    # Find the indices of the columns based on alphabetical order in the first non-header row
    first_row = table[1][1:]  # Skip the first column ('Model / Color')
    alpha_indices = sorted(range(len(first_row)), key=lambda i: first_row[i])

    # Rearrange the table columns based on the sorted indices
    sorted_table = []
    for row in table:
        sorted_row = [row[0]] + [row[i + 1] if i + 1 < len(row) else "" for i in alpha_indices]
        sorted_table.append(sorted_row)

    return sorted_table


def create_table_from_dict(data_dict):
    # Create the header row for the table
    header_row = [1, "      "]
    colors = list(set(color for _, color in data_dict.values()))
    header_row.extend(colors)
    table_data = [header_row]

    # Create a list of unique models
    models = list(set(model for model, _ in data_dict.values()))

    # Create rows for each model
    for idx, model in enumerate(models, start=2):
        row_data = [idx, model]
        for color in colors:
            for key, value in data_dict.items():
                if value == [model, color]:
                    row_data.append(key)
        table_data.append(row_data)

    table_data = [row[1:] for row in table_data]
    # Print the table
    print("table = [")
    for row in table_data:
        print(row, end="")
        print(',')
    print("]")

    return table_data


def generate_markdown_file(tables, title, filename):
    markdown_content = "import Image from \"next/image\"\n\n"

    markdown_content += f"# {title}\n\n"

    markdown_content += "## In the Wild\n\n"
    markdown_content += "## Pricing / Availability\n\n"
    markdown_content += "## Compatibility\n\n"
    markdown_content += "## Part numbers\n\n"

    for table in tables:
        table_data = sort_table_columns(table)

        # Generate the Markdown table
        table_content = "|" + "|".join(table_data[0]) + "|\n"
        table_content += "|" + "|".join(":--" for _ in table_data[0]) + "|\n"
        for row in table_data[1:]:
            table_content += "|" + "|".join(row) + "|\n"

        markdown_content += table_content
        markdown_content += "\n\n"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(markdown_content)


early_2011 = {
    "MC360ZM/A": "iPad Dock",
    "MC531ZM/A": "iPad Camera Connection Kit",
    "MC533LL/B": "iPad Keyboard Dock",
    "MC552ZM/B": "iPad Dock connector to VGA adapter",
    "MC940ZM/A": "iPad 2 Dock",
}

late_2017 = {
    "MQHX2AM/A": "iPhone Lightning Dock – Gold"  # to match gold iPhone 8
}

table2 = [create_table_from_dict(ipad129), create_table_from_dict(ipadleather)]
generate_markdown_file(table2, "iPad Pro 12.9", "ipadpro.mdx")
table3 = [create_table_from_dict(summeriphone), create_table_from_dict(summersili)]
generate_markdown_file(table3, "iPhone 7", "iphone.mdx")

Autumn_2017 = {
    "MQHA2ZM/A": ["iPhone 8 / 7 Leather Case", "(PRODUCT)RED"],
    "MQH92ZM/A": ["iPhone 8 / 7 Leather Case", "Black"],
    "MQH82ZM/A": ["iPhone 8 / 7 Leather Case", "Midnight Blue"],
    "MQH72ZM/A": ["iPhone 8 / 7 Leather Case", "Saddle Brown"],
    "MQH62ZM/A": ["iPhone 8 / 7 Leather Case", "Taupe"],
    "MQHF2ZM/A": ["iPhone 8 / 7 Leather Case", "Cosmos Blue"],

    "MQGP2ZM/A": ["iPhone 8 / 7 Silicone Case", "(PRODUCT)RED"],
    "MQGK2ZM/A": ["iPhone 8 / 7 Silicone Case", "Black"],
    "MQGM2ZM/A": ["iPhone 8 / 7 Silicone Case", "Midnight Blue"],
    "MQGQ2ZM/A": ["iPhone 8 / 7 Silicone Case", "Pink Sand"],
    "MQGL2ZM/A": ["iPhone 8 / 7 Silicone Case", "White"],
    # something else maybe?

    "MQHN2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "(PRODUCT)RED"],
    "MQHM2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Black"],
    "MQHL2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Midnight Blue"],
    "MQHK2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Saddle Brown"],
    "MQHJ2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Taupe"],
    "MQHR2FE/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Cosmos Blue"],

    "MQH12ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "(PRODUCT)RED"],
    "MQGW2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Black"],
    "MQGY2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Midnight Blue"],
    "MQH22ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Pink Sand"],
    "MQGX2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "White"],

    "MQTE2ZM/A": ["iPhone X Leather Case", "(PRODUCT)RED"],
    "MQTD2ZM/A": ["iPhone X Leather Case", "Black"],
    "MQTC2ZM/A": ["iPhone X Leather Case", "Midnight Blue"],
    "MQTA2ZM/A": ["iPhone X Leather Case", "Saddle Brown"],
    "MQT92ZM/A": ["iPhone X Leather Case", "Taupe"],

    # TODO there are more!!
    "MQRV2ZM/A": ["iPhone X Leather Folio", "Black"],
    # Cosmos Blue, Taupe, Black, and Berry

    "MQT52ZM/A": ["iPhone X Silicone Case", "(PRODUCT)RED"],
    "MQT12ZM/A": ["iPhone X Silicone Case", "Black"],
    "MQT32ZM/A": ["iPhone X Silicone Case", "Midnight Blue"],
    "MQT62ZM/A": ["iPhone X Silicone Case", "Pink Sand"],
    "MQT22ZM/A": ["iPhone X Silicone Case", "White"],
    # 9 colors in total!

    "MR5L2ZM/A": ["iPad Pro 10.5″ Leather Sleeve", "(PRODUCT)RED"],
    "MR5G2ZM/A": ["iPad Pro 10.5″ Leather Smart Cover", "(PRODUCT)RED"],
    "MR592ZM/A": ["iPad Pro 10.5″ Smart Cover", "(PRODUCT)RED"],

    "MQG02ZM/A": ["Leather Sleeve for 12-inch MacBook", "Midnight Blue"],
    "MQG12ZM/A": ["Leather Sleeve for 12-inch MacBook", "Saddle Brown"]
}

spring_2018 = {
    "MRG82ZM/A": ["iPhone 8 / 7 Leather Case", "Bright Orange"],
    "MRG52ZM/A": ["iPhone 8 / 7 Leather Case", "Electric Blue"],
    "MRG62ZM/A": ["iPhone 8 / 7 Leather Case", "Soft Pink"],
    "MRG72ZM/A": ["iPhone 8 / 7 Leather Case", "Spring Yellow"],

    "MRFR2ZM/A": ["iPhone 8 / 7 Silicone Case", "Denim Blue"],
    "MRFU2ZM/A": ["iPhone 8 / 7 Silicone Case", "Lemonade"],
    "MRFQ2ZM/A": ["iPhone 8 / 7 Silicone Case", "Red Raspberry"],

    "MRGD2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Bright Orange"],
    "MRG92ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Electric Blue"],
    "MRGA2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Soft Pink"],
    "MRGC2ZM/A": ["iPhone 8 Plus / 7 Plus Leather Case", "Spring Yellow"],

    "MRFX2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Denim Blue"],
    "MRFY2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Lemonade"],
    "MRFW2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Red Raspberry"],

    "MRGK2ZM/A": ["iPhone X Leather Case", "Bright Orange"],
    "MRGG2ZM/A": ["iPhone X Leather Case", "Electric Blue"],
    "MRGH2ZM/A": ["iPhone X Leather Case", "Soft Pink"],
    "MRGJ2ZM/A": ["iPhone X Leather Case", "Spring Yellow"],

    "MRGE2ZM/A": ["iPhone X Leather Folio", "Electric Blue"],
    "MRGF2ZM/A": ["iPhone X Leather Folio", "Soft Pink"],
    "MRQD2ZM/A": ["iPhone X Leather Folio", "(PRODUCT)RED"],

    "MRG22ZM/A": ["iPhone X Silicone Case", "Denim Blue"],
    "MRG32ZM/A": ["iPhone X Silicone Case", "Lemonade"],
    "MRG12ZM/A": ["iPhone X Silicone Case", "Red Raspberry"],

    "MRFL2ZM/A": ["iPad Pro 10.5″ Leather Sleeve ", "Electric Blue"],
    "MRFM2ZM/A": ["iPad Pro 10.5″ Leather Sleeve ", "Soft Pink"],
    "MRFJ2ZM/A": ["iPad Pro 10.5″ Leather Smart Cover", "Electric Blue"],
    "MRFK2ZM/A": ["iPad Pro 10.5″ Leather Smart Cover", "Soft Pink"],
    "MRFG2ZM/A": ["Smart Cover for 10.5‐inch iPad Pro", "Lemonade"],
    "MRFF2ZM/A": ["Smart Cover for 10.5‐inch iPad Pro", "Raspberry"]
    # no iPad Pro 12.9 covers back because...
}

wwdc_2018 = {
    "MRR72ZM/A": ["iPhone 8 / 7 Silicone Case", "Marine Green"],
    "MRR52ZM/A": ["iPhone 8 / 7 Silicone Case", "Peach"],
    "MRR62ZM/A": ["iPhone 8 / 7 Silicone Case", "Sky Blue"],

    "MRRA2ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Marine Green"],
    "MRR82ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Peach"],
    "MRR92ZM/A": ["iPhone 8 Plus / 7 Plus Silicone Case", "Sky Blue"],

    "MRRE2ZM/A": ["iPhone X Silicone Case", "Marine Green"],
    "MRRC2ZM/A": ["iPhone X Silicone Case", "Peach"],
    "MRRD2ZM/A": ["iPhone X Silicone Case", "Sky Blue"],
}

late_2018 = {
    # https://www.macrumors.com/2018/09/12/apple-releases-iphone-xs-xs-max-cases/
    # + XR Clear Case
}

# https://www.macrumors.com/2019/03/20/spring-colors-cases-bands/

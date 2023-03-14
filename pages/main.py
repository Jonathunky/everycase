import json
import os


def normalize_filename(filename):
	# Remove any braces
	filename = filename.replace('(', '').replace(')', '')

	# Replace any spaces with underscores
	filename = filename.replace(' ', '_')

	return filename


colors = {  # let's use colors as a baseline! I'm a fucking genius!!! Hell yes!
	# TODO Late 2017, Early 2017, Late 2016, Early 2016, Late 2015, Late 2014, etc...
	"Early 2018": {
		# https://www.macstories.net/news/apple-introduces-new-spring-colors-for-iphone-and-ipad-accessories-space-gray-mac-accessories-now-available/
		"Electric Blue": ["iphone_x_folio", "iphone_2017_leather"],
		"Soft Pink": ["iphone_x_folio", "iphone_2017_leather"],
		"Spring Yellow": ["iphone_2017_leather"],
		"Bright Orange": ["iphone_2017_leather"],
		"Red Raspberry": ["iphone_2017_silicone"],
		"Lemonade": ["iphone_2017_silicone"],
		"Denim Blue": ["iphone_2017_silicone"]
	},
	"Late 2018": {
		"Peony Pink": ["iphone_xs_leather", "iphone_xs_folio"],
		"Cape Cod Blue": ["iphone_xs_leather", "iphone_xs_folio"],
		"Forest Green": ["iphone_xs_leather", "iphone_xs_folio"],
		"Taupe": ["iphone_xs_leather"],
		"Midnight Blue": ["iphone_xs_leather", "iphone_xs_silicone"],
		"Saddle Brown": ["iphone_xs_leather"],
		"Black": ["iphone_xs_leather", "iphone_xs_folio", "iphone_xs_silicone", "iphone_xs_battery",
							"iphone_xr_battery"],
		"(PRODUCT) RED": ["iphone_xs_leather", "iphone_xs_folio", "iphone_xs_silicone"],
		"Nectarine": ["iphone_xs_silicone"],
		"Lavender Gray": ["iphone_xs_silicone"],
		"Blue Horizon": ["iphone_xs_silicone"],
		"Stone": ["iphone_xs_silicone"],
		"Pink Sand": ["iphone_xs_silicone"],
		"White": ["iphone_xs_silicone", "iphone_xs_battery", "iphone_xr_battery"],
		"Clear": ["iphone_xr"]
	},
	"Early 2019": {
		# https://www.macrumors.com/2019/03/20/spring-colors-cases-bands/
		"Spearmint": ["iphone_xs_silicone"],
		"Papaya": ["iphone_xs_silicone"],
		"Delft Blue": ["iphone_xs_silicone"],
		"Cornflower": ["iphone_xs_leather", "iphone_xs_folio"],
		"Sunset": ["iphone_xs_leather", "iphone_xs_folio"],
		"Lilac": ["iphone_xs_leather", "iphone_xs_folio"],
		"Pink Sand": ["iphone_xs_battery", "iphone_xr_battery"]
	},
	"Late 2019": {
		# https://www.macrumors.com/2019/09/10/new-cases-for-iphone-11/
		"Meyer Lemon": ["iphone_2019_leather"],
		"Forest Green": ["iphone_2019_leather"],
		"Midnight Blue": ["iphone_2019_leather", "iphone_2019_silicone"],
		"Saddle Brown": ["iphone_2019_leather"],
		"Black": ["iphone_2019_leather", "iphone_11_silicone", "iphone_11_battery"],
		"(PRODUCT) RED": ["iphone_2019_leather", "iphone_2019_silicone"],
		"Clementine": ["iphone_2019_silicone"],
		"Pine Green": ["iphone_2019_silicone"],
		"Alaskan Blue": ["iphone_2019_silicone"],
		"Pink Sand": ["iphone_2019_silicone", "iphone_2019_battery"],
		"White": ["iphone_11_silicone", "iphone_11_battery"],
		"Aubergine": ["iphone_2019_folio"],
		"Clear": ["iphone_2019_clear"]
	},
	"Early 2020": {
		# https://www.macrumors.com/2020/03/18/apple-cases-spring-color-options/
		"Peacock": ["iphone_2019_folio"],
		"Cactus": ["iphone_11_silicone"],
		"Grapefruit": ["iphone_11_silicone"],
		"Surf Blue": ["iphone_11_silicone"]
	},
	"Late 2020": {
		"Black": ["iphone_2020_leather", "iphone_2020_silicone"],
		"Saddle Brown": ["iphone_2020_leather", "iphone_2020_sleeve", "magsafe_wallet"],
		"(PRODUCT) RED": ["iphone_2020_leather", "iphone_2020_sleeve", "iphone_2020_silicone"],
		"Blue": ["iphone_2020_leather"],
		"California Poppy": ["iphone_2020_leather", "magsafe_wallet"],
		"Baltic Blue": ["iphone_2020_sleeve", "magsafe_wallet"],
		"Pink Citrus": ["iphone_2020_sleeve", "iphone_2020_silicone"],
		"White": ["iphone_2020_silicone"],
		"Deep Navy": ["iphone_2020_silicone"],
		"Cyprus Green": ["iphone_2020_silicone"],
		"Kumquat": ["iphone_2020_silicone"],
		"Plum": ["iphone_2020_silicone"],
		"Clear": ["iphone_2020_clear"]
	},
	"Early 2021": {
		"Arizona": ["iphone_2020_leather"],
		"Baltic Blue": ["iphone_2020_leather"],
		"California Poppy": ["iphone_2020_leather"],
		"Golden Brown": ["iphone_2020_leather"],
		"Red": ["iphone_2020_leather"],
		"Amethyst": ["iphone_2020_silicone"],
		"Cantaloupe": ["iphone_2020_silicone"],
		"Capri Blue": ["iphone_2020_silicone"],
		"Pistachio": ["iphone_2020_silicone"],
		"Sunflower": ["iphone_2020_silicone"]
	}
	# TODO there were also Early 2021 wallets!!
	# TODO Late 2021, Early 2022, Late 2022, Early 2023
	# TODO iPads, AirTag zaloopas, and such
}

models = {
	"iphone_x_folio": "iPhone X Leather Folio",
	"iphone_2017_leather": "iPhone X / 8 / 8 Plus Leather Case",
	"iphone_2017_silicone": "iPhone X / 8 / 8 Plus Silicone Case",

	"ipad_pro_105_leather": "iPad Pro 10.5-inch Leather Cover",
	"ipad_pro_105_sleeve": "iPad Pro 10.5-inch Leather Sleeve",
	"ipad_pro_105_silicone": "iPad Pro 10.5-inch Smart Cover",

	"iphone_xs_leather": "iPhone Xs / Xs Max Leather Case",
	"iphone_xs_folio": "iPhone Xs / Xs Max Leather Folio",
	"iphone_xs_silicone": "iPhone Xs / Xs Max Silicone Case",
	"iphone_xr": "iPhone Xr Clear Case",
	"iphone_xs_battery": "iPhone Xs / Xs Max Battery Case",
	"iphone_xr_battery": "iPhone Xr Battery Case",

	"iphone_2019_leather": "iPhone 11 Pro / Max Leather Case",
	"iphone_2019_folio": "iPhone 11 Pro / Max Leather Folio",
	"iphone_2019_silicone": "iPhone 11 Pro / Max Silicone Case",
	"iphone_11_silicone": "iPhone 11 / Pro / Max Silicone Case",
	"iphone_2019_battery": "iPhone 11 Pro / Max Smart Battery Case",
	"iphone_11_battery": "iPhone 11 / Pro / Max Smart Battery Case",
	"iphone_2019_clear": "iPhone 11 / Pro / Max Clear Case",

	"iphone_2020_leather": "iPhone 12 series Leather Case with MagSafe",
	"iphone_2020_sleeve": "iPhone 12 series Leather Sleeve with MagSafe",
	"iphone_2020_silicone": "iPhone 12 series Silicone Case with MagSafe",
	"iphone_2020_clear": "iPhone 12 series Clear Case with MagSafe",

	"magsafe_wallet": "iPhone Leather Wallet with MagSafe",
	"magsafe_wallet_findmy": "iPhone Leather Wallet with MagSafe"
}

# Year / Color / Device
for drop, drop_data in colors.items():
	os.makedirs(normalize_filename(drop), exist_ok=True)  # create Year folder
	color_folders = {}

	# color | released things
	for color, things in drop_data.items():

		# create folder for each color
		dir = normalize_filename(drop + "/" + color)
		os.makedirs(dir, exist_ok=True)
		color_folders[normalize_filename(color)] = color

		# now inside of that folder let's create a json
		jsonchik = {}
		for model in things:
			array = dict(title=models[model], href=normalize_filename(drop + "/" + model.split('_')[0] + "-drop.md"))
			jsonchik[model] = array
			open(os.path.join(normalize_filename(drop + "/" + model.split('_')[0] + "-drop.md")), "a")
		# print(json.dumps(jsonchik, indent=4))

		with open(os.path.join(normalize_filename(drop + "/" + color), "_meta.json"), "w") as color_file:
			color_file.write(json.dumps(jsonchik, indent=4))

	with open(os.path.join(normalize_filename(drop + "/"), "_meta.json"), "w") as drop_file:
		drop_file.write(json.dumps(color_folders, indent=4))
		'''
				# JSON generation
		color_folders[normalize_filename(color)] = color
		device_files = {}

		# create markdown file for each model
		for model in things:
			device_files[normalize_filename(model)] = models[model]
			filename = os.path.join(dir, normalize_filename(model) + ".md")
			if os.path.exists(filename):
				with open(filename, "r+") as color_file:
					color_file.seek(0)
					color_file.write("# " + models[model] + " – " + color + "\n")
			else:
				with open(filename, "w") as color_file:
					color_file.write("# " + models[model] + " – " + color + "\n ")


'''

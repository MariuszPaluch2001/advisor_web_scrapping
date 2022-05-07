import sys
from laptop import LaptopFabric
from func_lib import *
import db_module

def main(argc: int, argv: list):
    if argc < 3:
        return 1

    filename = argv[1]
    with open(filename) as f:
        config = read_config(f)


    NUMBER_OF_PAGES = int(argv[2])
    URL = config["page_URL"]
    SHORT_URL = config["short_page_URL"]
    PAGE_SUFFIX = config["page_suffix"]
    lapt_creator = LaptopFabric("price",
                                "link",
                                config["screen_atr"],
                                config["CPU_atr"],  
                                config["RAM_atr"],  
                                config["disc_atr"],  
                                config["GPU_atr"],  
                                config["OS_atr"])  
    db = db_module.DB_Adapter()
    db.connect(config["db_path"]) #@to do - don't use entire path 
    for index in range(1, NUMBER_OF_PAGES):
        soup = preparing_soup(URL + PAGE_SUFFIX + str(index),
                              {'User-Agent': 'Mozilla/5.0'}, "html.parser")
        result = soup.find(id="section_list-items")
        offerts = result.find_all("div", "offer-box")

        for off in offerts:
            # get standard price
            price = off.find(class_="main-price is-big")
            if price is None:
                price = off.find(class_="main-price price-regular is-medium")
            price = price.find(class_="whole")
            lapt_creator.set_value("price", price.get_text().strip())
            # get link to offer
            link = off.find(class_="is-animate spark-link")["href"]
            lapt_creator.set_value("link", "{}{}".format(SHORT_URL, link))

            content = off.find(class_="column-right")
            list_attributes = content.find(class_="list attributes")
            items = list_attributes.find_all("tr", "item")

            for item in items:
                name_attr = item.find(class_="name attribute")
                value_attr = item.find(class_="values attribute")
                lapt_creator.set_value(
                    name_attr.get_text().strip(), value_attr.get_text().strip())

            lapt = lapt_creator.create_laptop_object()
            lapt_creator.initialization()
            db.statement("INSERT INTO laptops VALUES (?,?,?,?,?,?,?,?, datetime('now'))", lapt.get_values())

    db.commit()
    return 0


if __name__ == "__main__":
    out = main(len(sys.argv), sys.argv)
    if out == 1:
        print("Correct usage : python3 main.py config_file_path number_of_pages")

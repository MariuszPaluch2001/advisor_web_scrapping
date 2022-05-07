import sys
from laptop import LaptopFabric
from func_lib import *
import db_module
import logging
import datetime

def main(argc: int, argv: list):


    if argc < 3:
        return 1

    filename = argv[1]
    try:
        with open(filename) as f:
            config = read_config(f)
    except FileNotFoundError :
        return 2

    log_path = config["log_path"]
    logging.basicConfig(level=logging.INFO, filename=f"{log_path}scrapper_log_{datetime.datetime.now()}.log",
        format="%(asctime)s = %(levelname)s - %(message)s")

    NUMBER_OF_PAGES = int(argv[2])
    try:
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
        db.connect(config["db_path"]) 
    except KeyError:
        logging.exception(f"Wrong key in {filename} config file.")
        return 3

    for index in range(1, NUMBER_OF_PAGES + 1):
        page_URL = URL + PAGE_SUFFIX + str(index)
        try:
            soup = preparing_soup(page_URL,
                                {'User-Agent': 'Mozilla/5.0'}, "html.parser")
        except:
            logging.exception(f"Couldn't connect with page {page_URL}")
            return 4
        
        try:
            result = soup.find(id="section_list-items")
            offerts = result.find_all("div", "offer-box")
        except AttributeError:
            logging.exception(f"Probably page change internal structure.")
            return 5

        for off in offerts:
            # get standard price
            try:
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
            except AttributeError:
                logging.exception(f"Probably page change internal structure.")
                return 5

            lapt = lapt_creator.create_laptop_object()
            lapt_creator.initialization()
            try:
                db.statement_with_param("INSERT INTO laptops VALUES (?,?,?,?,?,?,?,?, datetime('now'))", lapt.get_values())
            except:
                logging.exception(f"Problem with database.")
                return 6
    db.commit()
    return 0


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)

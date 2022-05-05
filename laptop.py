class LaptopFabric:
    def __init__(self, price_name, link_name, screen_name, procesor_name, ram_name, disc_name, graphic_card_name, os_name) -> None:
        self.price_name = price_name
        self.link_name = link_name
        self.screen_name = screen_name
        self.procesor_name = procesor_name
        self.ram_name = ram_name
        self.disc_name = disc_name
        self.graphic_card_name = graphic_card_name
        self.os_name = os_name

        self.values = None

        self.initialization()

    def initialization(self):
        self.values = {
            self.price_name: None,
            self.link_name: None,
            self.screen_name: None,
            self.procesor_name: None,
            self.ram_name: None,
            self.disc_name: None,
            self.graphic_card_name: None,
            self.os_name: None
        }

    def create_laptop_object(self):
        return Laptop(
            self.values[self.price_name],
            self.values[self.link_name],
            self.values[self.screen_name],
            self.values[self.procesor_name],
            self.values[self.ram_name],
            self.values[self.disc_name],
            self.values[self.graphic_card_name],
            self.values[self.os_name]
        )

    def set_value(self, attr_name, attr_value):
        self.values[attr_name] = attr_value


class Laptop:
    def __init__(self, price, link, screen, procesor, ram, disc, graphic_card, os) -> None:
        self.price = price
        self.link = link
        self.screen = screen
        self.procesor = procesor
        self.ram = ram
        self.disc = disc
        self.graphic_card = graphic_card
        self.os = os

    def get_values(self):
        return (self.price,
                self.link,
                self.screen,
                self.procesor,
                self.ram,
                self.disc,
                self.graphic_card,
                self.os
                )

    def __str__(self) -> str:
        return f" Price : {self.price}\n Link  : {self.link}\n \
Screen: {self.screen}\n \
Proc  : {self.procesor}\n \
RAM   : {self.ram}\n \
Disc  : {self.disc}\n \
GPU   : {self.graphic_card}\n \
OS    : {self.os}\n "

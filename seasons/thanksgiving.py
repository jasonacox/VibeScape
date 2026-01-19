"""
Thanksgiving season prompt generator.

Generates Thanksgiving scenes with family gatherings, feasts,
gratitude themes, and historical celebration elements.
"""
from .base import SeasonBase


class Thanksgiving(SeasonBase):
    """
    Thanksgiving season prompt generator.

    Creates warm family gathering scenes, traditional feasts,
    harvest celebrations, and gratitude-themed imagery.
    """

    @property
    def name(self) -> str:
        return "Thanksgiving"

    @property
    def scene_keywords(self) -> list[str]:
        return [
            # Close-up food shots
            "close-up of golden roasted turkey with crispy skin, garnished with herbs",
            "tight shot of cranberry sauce in crystal bowl, glistening red berries",
            "close-up of pumpkin pie slice with whipped cream swirl",
            "overhead view of mashed potatoes with melting butter pool",
            "macro shot of green bean casserole with crispy onions on top",
            "close-up of stuffing spilling from carved turkey",
            "tight crop of sweet potato casserole with marshmallow topping",
            "detailed shot of gravy being poured over turkey and mashed potatoes",
            "close-up of warm dinner rolls in woven basket with butter",
            "overhead view of pecan pie with caramelized nuts",
            "tight shot of apple pie with lattice crust, steam rising",
            "close-up of cornbread stuffing with celery and herbs",
            "detailed view of brussels sprouts with bacon bits",
            "overhead shot of mac and cheese with golden crusty top",
            "close-up of corn on the cob with melting butter",
            # Table setting close-ups
            "close-up of elegant Thanksgiving place setting with autumn napkins",
            "tight shot of wine glasses and candles on Thanksgiving table",
            "overhead view of full Thanksgiving table spread, all dishes visible",
            "close-up of centerpiece with mini pumpkins and fall flowers",
            "detailed shot of autumn-themed table runner with place cards",
            # Traditional feast scenes
            "family gathered around Thanksgiving dinner table, feast spread",
            "golden roasted turkey centerpiece on dining table with sides",
            "traditional Thanksgiving feast with all the trimmings displayed",
            "Thanksgiving table setting with autumn decorations everywhere",
            "rustic farmhouse Thanksgiving celebration with harvest theme",
            # Cooking and preparation
            "kitchen counter with Thanksgiving meal prep in progress",
            "hands carving turkey on serving platter, steam rising",
            "family cooking together in warm kitchen, multiple dishes",
            "warm kitchen with homemade pies cooling on counter",
            "oven view of turkey roasting, golden brown",
            # Family gathering moments
            "multi-generational family giving thanks before meal",
            "family sharing gratitude around candlelit table",
            "grateful family holding hands at table for prayer",
            "children helping set Thanksgiving table",
            "cozy dining room filled with family and food",
            "warm gathering with friends and family, laughter and food",
            # Harvest and decoration
            "cornucopia overflowing with harvest bounty and gourds",
            "autumn harvest display with pumpkins and wheat sheaves",
            "autumn-themed centerpiece with candles and fall leaves",
        ]

    @property
    def extras(self) -> list[str]:
        return [
            "warm candlelight",
            "autumn colors and textures",
            "golden hour lighting",
            "family togetherness",
            "grateful expressions",
            "harvest decorations",
            "cozy atmosphere",
            "traditional recipes",
            "steaming hot dishes",
            "rustic wooden table",
            "seasonal abundance",
            "warm inviting glow",
            "festive tablecloth",
            "thankful mood",
            "home-cooked warmth",
            "soft bokeh lights",
            "shallow depth of field",
            "overhead food photography",
            "garnished beautifully",
            "rich textures and details",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "roasted turkey",
            "pumpkin pie",
            "cornucopia",
            "gravy boat",
            "wooden serving platter",
            "woven basket",
            "autumn wreath",
            "candle holder",
            "copper pot",
            "rustic pitcher",
            "harvest gourd",
            "wheat sheaf",
            "wooden bowl",
            "cast iron skillet",
            "linen napkins",
            "cider jug",
            "pie dish",
            "ceramic platter",
            "farmhouse table",
            "rocking chair",
        ]

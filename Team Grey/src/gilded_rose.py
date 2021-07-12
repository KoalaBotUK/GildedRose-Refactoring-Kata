# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        qualityFactor = 1

        for item in self.items:
            if (item.name.startsWith("Conjured")):
                qualityFactor = 2


            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - qualityFactor
            else:
                if item.quality < 50:
                    item.quality = item.quality + qualityFactor
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < (50 - qualityFactor*2):
                                item.quality = item.quality + qualityFactor*2
                        if item.sell_in < 6:
                            if item.quality < (50 - qualityFactor*3):
                                item.quality = item.quality + qualityFactor*3
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality >= qualityFactor:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - qualityFactor
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < (50 - qualityFactor):
                        item.quality = item.quality + qualityFactor


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

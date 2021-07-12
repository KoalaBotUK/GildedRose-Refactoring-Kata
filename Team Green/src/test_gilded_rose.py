# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose


class TestGildedRose():
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        assert "foo" == items[0].name

    def test_item_has_sell_in_val(self):
        items = [Item("foo", 0, 0)]
        assert items[0].sell_in is not None

    def test_item_has_quality_val(self):
        items = [Item("foo", 0, 0)]
        assert items[0].quality is not None

    def test_update_quality(self):
        starting_quality = 30
        item = Item("foo", starting_quality, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality < starting_quality and item.sell_in < starting_quality

    def test_item_quality_degrades_fast_after_sell_by(self):
        starting_quality = 30
        starting_sell_in = -1
        item = Item("foo", starting_sell_in, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 28

    def test_quality_of_item_not_negative(self):
        starting_quality = 5
        sell_by = -3
        item = Item("foo", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        for i in range(4):
            gilded_rose.update_quality()
        assert item.quality >= 0

    def test_aged_brie_increases_in_quality(self):
        starting_quality = 5
        sell_by = 10
        item = Item("Aged Brie", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality > starting_quality

    def test_item_quality_less_than_50(self):
        starting_quality = 5
        sell_by = 10
        item = Item("Aged Brie", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        for i in range(100):
            gilded_rose.update_quality()
        assert item.quality <= 50

    def test_sulfuras_never_decreases_in_quality(self):
        starting_quality = 80
        sell_by = 10
        item = Item("Sulfuras, Hand of Ragnaros", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == starting_quality and item.sell_in == sell_by

    def test_backstage_increases_by_two(self):
        starting_quality = 10
        sell_by = 9
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 12

    def test_backstage_increases_by_three(self):
        starting_quality = 10
        sell_by = 4
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 13

    def test_backstage_loses_quality(self):
        starting_quality = 10
        sell_by = 0
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 0

    def test_conjured_ages_faster(self):
        starting_quality = 10
        sell_by = 10
        item = Item("Conjured foo", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 8

    def test_conjured_ages_even_faster_after_sell_by(self):
        starting_quality = 10
        sell_by = -1
        item = Item("Conjured foo", sell_by, starting_quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 6
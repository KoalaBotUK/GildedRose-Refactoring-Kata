# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose

#Spec part 1
def test_qualityDegrading():
    items = [Item("foo", 3, 10), Item("foo", 0, 10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[1].quality == items[0].quality

#Spec part 2
def test_nonNegative():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 0 <= items[0].quality

#Spec part 3
def test_fasterAgingBrie():
    items = [Item("Aged Brie", 0, 2)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 3 == items[0].quality

#Spec part 4
def test_qualityUnder50():
    items = [Item("Aged Brie", 0, 50)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 50 == items[0].quality

#Spec part 5
def test_sulfurasUnchanging():
    items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 80 == items[0].quality
    assert 5 == items[0].sell_in

#Spec part 6.1
def test_increasingPassQuality():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 25 < items[0].quality

#Spec part 6.2
def test_increasingPassQualityTen():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 9, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 27 == items[0].quality

#Spec part 6.3
def test_increasingPassQualityFive():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 4, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 28 == items[0].quality

#Spec part 6.4
#If the day of the concert == sellinday of 0
def test_increasingPassQualityZero():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 1, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert  0 == items[0].quality

#Spec part 7
#Conjured aged brie
#??????
def test_conjuredQualityDecrease():
    items = [Item("Conjured Axe", 2, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert  23 == items[0].quality
#Spec part 7.2
def test_conjuredBrieQualityIncrease():
    items = [Item("Conjured Aged Brie", 2, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert  27 == items[0].quality

#Spec part 7.3
def test_conjuredBrieQualityIncrease():
    items = [Item("Conjured Aged Brie", 2, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert  27 == items[0].quality

#Spec part 7.4
def test_conjuredSulfurasUnchanging():
    items = [Item("Conjured Sulfuras, Hand of Ragnaros", 5, 80)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 80 == items[0].quality
    assert 5 == items[0].sell_in

#Spec part 7.5
def test_increasingPassQuality():
    items = [Item("Conjured Backstage passes to a TAFKAL80ETC concert", 12, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 24 < items[0].quality

#Spec part 7.6
def test_increasingConjuredPassQualityTen():
    items = [Item("Conjured Backstage passes to a TAFKAL80ETC concert", 9, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 29 == items[0].quality

#Spec part 7.7
def test_increasingConjuredPassQualityFive():
    items = [Item("Conjured Backstage passes to a TAFKAL80ETC concert", 4, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert 31 == items[0].quality

#Spec part 7.8
def test_increasingConjuredPassQualityZero():
    items = [Item("Conjured Backstage passes to a TAFKAL80ETC concert", 1, 25)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert  0 == items[0].quality

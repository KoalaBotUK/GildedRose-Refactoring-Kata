# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose


class TestGildedRose():
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        assert "fixme" == items[0].name


if __name__ == '__main__':
    unittest.main()

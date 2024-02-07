from __future__ import annotations


class Filter:
    """Model of a filter for a graph.

    Represents a model of a filter that can be applied to a graph.

    Attributes:
        attribute_name: The name of the attribute to filter on.
        comparator: The comparator to use for the filter.
        attribute_value: The value to compare the attribute to.
    """

    def __init__(self, attribute_name: str, comparator: str, attribute_value: str):
        self._attribute_name = attribute_name
        self._comparator = comparator
        self._attribute_value = attribute_value

    @property
    def attribute_name(self):
        return self._attribute_name

    @property
    def comparator(self):
        return self._comparator

    @property
    def attribute_value(self):
        return self._attribute_value

    def __eq__(self, other: Filter) -> bool:
        return self._attribute_name == other._attribute_name and self._comparator == other._comparator and self._attribute_value == other._attribute_value

    def __str__(self):
        return f"<{self._attribute_name} {self._comparator} {self._attribute_value}>"

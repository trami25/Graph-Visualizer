from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class FilterStrategy(ABC):
    """
    The FilterStrategy interface declares a method for evaluating if a given data
    satisfies the filter criteria.
    """

    @abstractmethod
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        pass


class EqualsFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        try:
            casted_value = type(data)(attribute_value)
            return data == casted_value
        except TypeError:
            return str(data) == attribute_value


class NotEqualsFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        try:
            casted_value = type(data)(attribute_value)
            return data != casted_value
        except TypeError:
            return str(data) != attribute_value


class GreaterThanFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        try:
            casted_value = type(data)(attribute_value)
            return data > casted_value
        except TypeError:
            return str(data) > attribute_value


class LessThanFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        try:
            casted_value = type(data)(attribute_value)
            return data < casted_value
        except TypeError:
            return str(data) < attribute_value


class GreaterThanOrEqualsFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        try:
            casted_value = type(data)(attribute_value)
            return data >= casted_value
        except TypeError:
            return str(data) >= attribute_value


class LessThanOrEqualsFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        try:
            casted_value = type(data)(attribute_value)
            return data <= casted_value
        except TypeError:
            return str(data) <= attribute_value


class SearchFilterStrategy(FilterStrategy):
    def satisfies_filter(self, data: Any, attribute_value: str) -> bool:
        for value in data:
            if str(attribute_value).lower() in str(value).lower():
                return True
        return False
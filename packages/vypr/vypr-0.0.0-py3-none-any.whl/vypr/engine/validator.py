from __future__ import annotations

import re

from abc import ABC, abstractmethod
from typing import Any, Collection, Optional, Tuple, Type, Union

from vypr.errors import VpValidationError


class VpValidator(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def fix(self, value: Any) -> Any:
        pass

    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


class VpNullValidator(VpValidator):
    def fix(self, value):
        return value

    def validate(self, value):
        pass


class VpChoiceValidator(VpValidator):
    def __init__(self, choices: Collection):
        super().__init__(self)
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            choices = ", ".join([f"'{x}'" for x in self.choices])
            raise VpValidationError(f"Invalid choice: '{value}', valid choices: {choices}")


class VpFloatValidator(VpValidator):
    def __init__(self, min_value: Optional[float] = None, max_value: Optional[float] = None):
        super().__init__(self)
        self.min_value = min_value
        self.max_value = max_value

    def fix(self, value):
        try:
            return float(value)
        except ValueError:
            raise VpValidationError(
                f"Unable to convert value of type: '{type(value).__name__}' to expected type: 'int'"
            )

    def validate(self, value):
        if not isinstance(value, float):
            raise VpValidationError(f"Bad type: '{type(value).__name__}' expected: 'float'")
        if self.min_value is not None and value < self.min_value:
            raise VpValidationError(f"Value must be no less than: {self.min_value}, given: {value}")
        if self.max_value is not None and value > self.max_value:
            raise VpValidationError(f"Value must be no more than: {self.max_value}, given: {value}")


class VpIntValidator(VpValidator):
    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None):
        super().__init__(self)
        self.min_value = min_value
        self.max_value = max_value

    def fix(self, value):
        try:
            return int(value)
        except ValueError:
            raise VpValidationError(
                f"Unable to convert value of type: '{type(value).__name__}' to expected type: 'int'"
            )

    def validate(self, value):
        if not isinstance(value, int):
            raise VpValidationError(f"Bad type: '{type(value).__name__}' expected: 'int'")
        if self.min_value is not None and value < self.min_value:
            raise VpValidationError(f"Value must be no less than: {self.min_value}, given: {value}")
        if self.max_value is not None and value > self.max_value:
            raise VpValidationError(f"Value must be no more than: {self.max_value}, given: {value}")


class VpStrValidator(VpValidator):
    def __init__(self, pattern: Optional[Union[str, re.Pattern]] = None):
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.pattern = pattern

    def fix(self, value):
        try:
            return str(value)
        except ValueError:
            raise VpValidationError(
                f"Unable to convert value of type: '{type(value).__name__}' to expected type: 'str'"
            )

    def validate(self, value):
        if not isinstance(value, str):
            raise VpValidationError(f"Bad type: '{type(value).__name__}' expected: 'str'")
        if self.pattern is not None:
            match = self.pattern.match(value)
            if not match or match.group() != value:
                raise VpValidationError(f"Value does not match regex: '{self.pattern.pattern}', given: {value}")


class VpTypeValidator(VpValidator):
    def __init__(self, types: Union[Type, Tuple[Type, ...]]):
        self.types = types

    def validate(self, value):
        if not isinstance(value, self.types):
            types = ", ".join([f"'{x.__name__}'" for x in self.types])
            raise VpValidationError(
                f"Bad type: '{type(value).__name__}' valid type{'s' if len(self.types) > 1 else ''}: {types}"
            )

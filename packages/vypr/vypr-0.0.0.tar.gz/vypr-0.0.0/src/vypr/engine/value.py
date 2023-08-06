from __future__ import annotations

import copy

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Collection, Dict, Iterable, List

from vypr.errors import VpValidationError, VpValueError
from vypr.engine.validator import VpValidator, VpNullValidator

if TYPE_CHECKING:
    from vypr.engine.node import VpSocket


class VpValue:

    __slots__ = [
        "_socket",
        "_value",
        "_validator",
    ]

    _socket: VpSocket

    def __init__(self, value: Any, validator: VpValidator = VpNullValidator()):
        self._validator = validator
        self._value = self.convert(value)

    def __str__(self):
        return str(self._value)

    def __copy__(self):
        return type(self)(copy.copy(self._value), self.validator)

    @property
    def validator(self) -> VpValidator:
        return self._validator

    def convert(self, value: Any) -> Any:
        try:
            self.validator.validate(value)
        except VpValidationError:
            try:
                value = self.validator.fix(value)
            except VpValidationError as err:
                raise VpValueError(self, str(err))
        return value

    def decode(self, state):
        pass

    def encode(self):
        pass

    def get(self) -> Any:
        return self._value

    def set(self, value: Any):
        self._value = self.convert(value)

    @property
    def socket(self) -> VpSocket:
        return self._socket

    @socket.setter
    def socket(self, socket: VpSocket):
        self._socket = socket


class VpMultiValue(VpValue):

    __slots__ = ["_resizeable"]

    def __init__(
        self,
        value: Any,
        validator: VpValidator = VpNullValidator(),
        resizeable: bool = False,
    ):
        super().__init__(value=value, validator=validator)
        self._resizeable = resizeable

    def __copy__(self):
        return type(self)(copy.copy(self._value), self.validator, self._resizeable)

    @abstractmethod
    def add_item(self, key: Any, value: Any):
        if not self.resizeable:
            raise VpValueError(self, "Cannot add item to value of fixed size")

    @abstractmethod
    def get(self) -> List[Any]:
        return self._value

    @abstractmethod
    def get_item(self, key: Any) -> Any:
        pass

    @abstractmethod
    def remove_item(self, key: Any):
        if not self.resizeable:
            raise VpValueError(self, "Cannot remove item from value of fixed size")

    @property
    def resizeable(self) -> bool:
        return self._resizeable

    @abstractmethod
    def set(self, value: Collection):
        # Confirm value is an interable sequence.
        if not isinstance(value, Iterable):
            raise VpValueError(self, f"Bad type: '{type(value).__name__}', iterable object required")

        # Check value size.
        if not self.resizeable:
            old_size = len(self._value)
            new_size = len(value)
            if new_size != old_size:
                raise VpValueError(self, f"Value of fixed size: {old_size} cannot be set to object of size: {new_size}")

    @abstractmethod
    def set_item(self, key: Any, value: Any):
        pass


class VpListValue(VpMultiValue):
    def __init__(
        self,
        value: Collection[Any],
        validator: VpValidator = VpNullValidator(),
        resizeable: bool = False,
    ):
        super().__init__(value=value, validator=validator, resizeable=resizeable)

    def add_item(self, key: int, value: Any):
        super().add_item(key=key, value=value)
        value = self.convert(value)
        if key == -1:
            self._value.append(value)
        else:
            self._value.insert(key, value)

    def remove_item(self, key: int):
        super().remove_item(key=key)
        try:
            self._value.pop(key)
        except IndexError:
            raise VpValueError(self, f"Index: {key} out of range.")

    def get(self) -> List[Any]:
        return self._value[:]

    def get_item(self, key: int) -> Any:
        try:
            return self._value[key]
        except IndexError:
            raise VpValueError(self, f"Index: {key} out of range.")

    def set(self, value: Collection):
        super().set(value)
        self._value = [self.convert(x) for x in value]

    def set_item(self, key: int, value: Any):
        try:
            self._value[key] = self.convert(value)
        except IndexError:
            raise VpValueError(self, f"Index: {key} out of range.")


class VpMapValue(VpMultiValue):
    def __init__(
        self,
        value: Dict[str, Any],
        validator: VpValidator = VpNullValidator(),
        resizeable: bool = False,
    ):
        super().__init__(value=value, validator=validator, resizeable=resizeable)

    def add_item(self, key: str, value: Any):
        super().add_item(key=key, value=value)
        value = self.convert(value)
        self._value[key] = value

    def remove_item(self, key: str):
        super().remove_item(key=key)
        try:
            self._value.pop(key)
        except IndexError:
            raise VpValueError(self, f"Index: {key} out of range.")

    def get(self) -> Dict[str, Any]:
        return self._value.copy()

    def get_item(self, key: str) -> Any:
        try:
            return self._value[key]
        except KeyError:
            raise VpValueError(self, f"Index: {key} out of range.")

    def set(self, value: Dict[str, Any]):
        super().set(value)
        self._value = {x[0]: self.convert(x[1]) for x in value.items()}

    def set_item(self, key: str, value: Any):
        try:
            self._value[key] = self.convert(value)
        except KeyError:
            raise VpValueError(self, f"Key: '{key}' not found.")

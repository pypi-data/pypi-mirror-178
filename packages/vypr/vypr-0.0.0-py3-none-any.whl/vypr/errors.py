"""Exception classes for all Vypr specific error conditions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vypr.engine.value import VpValue


class VpError(Exception):
    """Base class for all Vypr error handlers."""


class VpValidationError(VpError):
    """Exception handler for VpValue validation errors."""


class VpValueError(VpError):
    """Exception handler for errors encountered in VpValue get and set operations."""

    def __init__(self, value: VpValue, reason: str = ""):
        self.value = value
        self.reason = reason

    def __str__(self):
        message = f"Invalid {type(self.value).__name__}: "
        if self.value.socket:
            message += f"'{self.value.socket.attr_name}' at: '{self.value.socket.path}', "
        message += self.reason
        return message

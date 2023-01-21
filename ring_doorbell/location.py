"""Python Ring location wrapper."""
from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Optional
from enum import Enum
from ring_doorbell.const import LOCATION_MODE_ENDPOINT, APP_URI

if TYPE_CHECKING:  # pragma: no cover
    from ring_doorbell import Ring

_LOGGER = logging.getLogger(__name__)


class RingLocationMode(Enum):
    """Enumeration of Ring location modes"""

    DISARMED = "disarmed"
    HOME = "home"
    AWAY = "away"


class RingLocation:
    """Implementation for RingLocation."""

    # pylint: disable=redefined-builtin
    def __init__(self, ring: Ring, location_id: str):
        self._ring = ring
        self.id = location_id  # pylint:disable=invalid-name

        self._location_mode_url = LOCATION_MODE_ENDPOINT.format(self.id)

    @property
    def _attrs(self):
        """Return attributes."""
        return self._ring.location_data[self.id]

    @property
    def owner_id(self):
        """Return owner ID"""
        return self._attrs["owner_id"]

    @property
    def name(self):
        """Return name"""
        return self._attrs["name"]

    @property
    def latitude(self):
        """Return latitude"""
        return self._attrs["geo_coordinates"]["latitude"]

    @property
    def longitude(self):
        """Return longitude"""
        return self._attrs["geo_coordinates"]["longitude"]

    @property
    def address1(self):
        """Return address1"""
        return self._attrs["address"]["address1"]

    @property
    def address2(self):
        """Return address2"""
        return self._attrs["address"]["address2"]

    @property
    def cross_street(self):
        """Return cross_street"""
        return self._attrs["address"]["cross_street"]

    @property
    def city(self):
        """Return city"""
        return self._attrs["address"]["city"]

    @property
    def state(self):
        """Return state"""
        return self._attrs["address"]["state"]

    @property
    def zip_code(self):
        """Return state"""
        return self._attrs["address"]["zip_code"]

    @property
    def country(self):
        """Return state"""
        return self._attrs["address"]["country"]

    @property
    def timezone(self):
        """Return state"""
        return self._attrs["address"]["timezone"]

    def get_mode(self) -> Optional[RingLocationMode]:
        """Gets the current house mode for the location"""
        data = self._ring.query(self._location_mode_url, host_uri=APP_URI).json()
        try:
            retval = RingLocationMode(data["mode"])
            return retval
        except ValueError:
            pass

        return None

    def set_mode(self, mode: RingLocationMode):
        """Sets the current house mode for the location"""
        self._ring.query(
            self._location_mode_url,
            host_uri=APP_URI,
            method="POST",
            json={"mode": mode.value},
        )

"""Fake device for testing purposes. No parameters needed."""
from collections.abc import Iterable

from flowchem.components.base_component import FlowchemComponent
from flowchem.devices.flowchem_device import DeviceInfo, Person
from flowchem.devices.flowchem_device import FlowchemDevice

from .test_component import TestComponent


__all__ = ["FakeDevice"]

dario = Person(name="Dario Cambiè", email="2422614+dcambie@users.noreply.github.com")


class FakeDevice(FlowchemDevice):

    metadata = DeviceInfo(
        authors=[dario],
        maintainers=[dario],
        manufacturer="virtual-device",
        model="FakeDevice",
        serial_number=42,
        version="v1.0",
    )

    def components(self) -> Iterable[FlowchemComponent]:
        """Returns a test Component."""
        component = TestComponent(name="test-component", hw_device=self)
        component.add_api_route("/test", lambda: True, methods=["GET"])
        return (component,)

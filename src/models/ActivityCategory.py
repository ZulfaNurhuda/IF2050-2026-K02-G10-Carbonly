from typing import Optional


class ActivityCategory:
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self._name = name
        self._description = description

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

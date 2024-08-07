from typing import Any, ClassVar, Dict, Protocol


class IsDataclass(Protocol):
    # Checking for this attribute is the most reliable way to check if something
    # is a dataclass
    __dataclass_fields__: ClassVar[Dict[str, Any]]

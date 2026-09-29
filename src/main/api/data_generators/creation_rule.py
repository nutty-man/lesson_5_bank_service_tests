from dataclasses import dataclass


@dataclass
class CreationRule:
    regex: str

@dataclass
class RangeCreationRule:
    min_value: int
    max_value: int
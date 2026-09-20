import uuid
import random
from enum import Enum

import rstr

from typing import get_type_hints, get_origin, Annotated, get_args, Any
from main.api.data_generators.creation_rule import CreationRule
from main.utils.enums.role import Role


class RandomModelGenerator:

    @staticmethod
    def generate(model_class: type, role: Role = Role.USER) -> Any:
        type_hints = get_type_hints(model_class, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            if field_name == "role":
                init_data[field_name] = role
                continue

            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)

                for annotation in annotations:
                    if isinstance(annotation, CreationRule):
                        rule = annotation
                        break

            if rule:
                value = RandomModelGenerator._generate_from_regex(
                    rule.regex,
                    actual_type,
                )
            else:
                value = RandomModelGenerator._generate_value(actual_type)

            init_data[field_name] = value

        return model_class(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            return random.choice(list(field_type))

        if field_type is str:
            return str(uuid.uuid4())[:8]

        if field_type is int:
            return random.randint(1, 9999)

        if field_type is float:
            return round(random.uniform(0, 100), 2)

        if field_type is bool:
            return random.choice([True, False])

        return None



import re
from collections import OrderedDict
from typing import Union, Any, Optional

from markupsafe import Markup

from .base_elements import BaseInput
from .factories import MethodFactory


def update_value(element, value) -> str:
    def process(raw, new_value):
        if 'type="text"' in raw:
            pattern, replace = r'value="(.*?)"', rf'value="{new_value}"'
            if re.search(pattern, raw) is not None:
                return re.sub(pattern, replace, raw)
            return raw.replace('<input ', f'<input value="{new_value}" ')

        if 'type="checkbox"' in raw:
            if isinstance(new_value, bool):  # if value is bool
                if new_value:  # if value is True
                    if 'checked="checked"' in raw:
                        return raw
                    return raw.replace('>', ' checked="checked">')
                # if value is False
                if 'checked="checked"' in raw:
                    return raw.replace(' checked="checked"', '')
                return raw

    if isinstance(element, Markup):
        return Markup(process(element.unescape(), value))
    if isinstance(element, str):
        return process(element, value)
    if hasattr(element, "compile"):
        return process(element.compile(raw=True), value)

    return "Element is not a valid type"


class Input(BaseInput):

    def compile(self, raw: bool = False) -> Union[str, Markup]:
        name = id_ = value = class_ = str()
        required = checked = str()
        if self._name:
            name = f'name="{self._name}" '
        if self._id:
            id_ = f'id="{self._id}" '
        if self._value:
            value = f'value="{self._value}" '
        if self._class:
            class_ = f'class="{self._class}" '
        if self._required:
            required = 'required="required" '
        if self._checked:
            checked = 'checked="checked" '

        out = (
            '<input '
            f'{self._type}'
            f'{name}'
            f'{id_}'
            f'{value}'
            f'{class_}'
            f'{required}'
            f'{checked}'
            '>'
        )

        if raw:
            return out
        return Markup(out)


class InputGroup:
    elements: OrderedDict = OrderedDict()
    _wrap_count: int

    def __init__(self, *args: Input) -> None:
        self._wrap_count = 0
        if not self.elements:
            self.elements = OrderedDict()
        self.elements = MethodFactory.add_inputs(args, self.elements)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.elements})"

    def wrap(self, class_: Optional[str] = None, id_: Optional[str] = None,
             style: Optional[str] = None) -> 'InputGroup':
        self._wrap_count += 1
        _id = _class = _style = str()
        if class_:
            _class = f'class="{class_}" '
        if id_:
            _id = f'id="{id_}" '
        if style:
            _style = f'style="{style}" '
        start = (
            '<div '
            f'{_class}'
            f'{_id}'
            f'{_style}'
            '>'
        )
        self.elements = OrderedDict(({
            f'__start_{self._wrap_count}__': start,
            **self.elements,
            f'__end_{self._wrap_count}__': '</div>'
        }))
        return self

    def compile(self, raw: bool = False) -> Union[str, Markup]:
        out = [v for v in self.elements.values()]
        if raw:
            return "".join(out)
        return Markup("".join(out))

    def markup(self) -> dict:
        return {k: Markup(v.compile()) for k, v in self.elements.items()}


class Form:
    name: str
    elements: OrderedDict[Any, Any]
    _wrap_count: int = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self.elements = OrderedDict()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.elements})"

    def add_inputs(self, *args):
        """Adds elements to the form"""
        self.elements = MethodFactory.add_inputs(args, self.elements)
        return self

    def add_input_groups(self, *args: InputGroup):
        self.elements = MethodFactory.add_input_groups(args, self.elements)
        return self

    def wrap(self, class_: Optional[str] = None, id_: Optional[str] = None,
             style: Optional[str] = None) -> 'Form':
        self._wrap_count += 1
        _id = _class = _style = str()
        if class_:
            _class = f'class="{class_}" '
        if id_:
            _id = f'id="{id_}" '
        if style:
            _style = f'style="{style}" '
        start = (
            '<div '
            f'{_class}'
            f'{_id}'
            f'{_style}'
            '>'
        )
        self.elements = OrderedDict(({
            f'__start_{self._wrap_count}__': start,
            **self.elements,
            f'__end_{self._wrap_count}__': '</div>'
        }))
        return self

    def compile(self, raw: bool = False) -> Union[str, Markup]:
        out = list()
        for element in self.elements.values():
            if isinstance(element, Input):
                out.append(element.compile(raw=raw))
            if isinstance(element, str):
                out.append(element)
        if raw:
            return "".join(out)
        return Markup("".join(out))

    def markup(self) -> dict:
        out = OrderedDict()
        for k, v in self.elements.items():
            if hasattr(v, "compile"):
                out[k] = v.compile()
            if isinstance(v, str):
                out[k] = Markup(v)
        return out

    def update_value(self, input_field: str, value: Union[bool, str, int, Input]) -> None:
        if input_field in self.elements:
            if isinstance(value, Input):
                self.elements[input_field] = value
            else:
                if isinstance(self.elements[input_field], Input):
                    self.elements[input_field].value(value)

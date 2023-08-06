from typing import Union

from markupsafe import Markup

from .base_elements import BaseInput


class BootstrapInput(BaseInput):

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
            class_ = f' {self._class}'
        if self._required:
            required = 'required="required" '
        if self._checked:
            checked = 'checked="checked" '

        class_wrapper_ = f'class="form-control{class_}"'

        out = (
            '<input '
            f'{self._type}'
            f'{name}'
            f'{id_}'
            f'{value}'
            f'{class_wrapper_}'
            f'{required}'
            f'{checked}'
            '>'
        )

        if raw:
            return out
        return Markup(out)

    def prepend(self):
        pass

    def append(self):
        pass

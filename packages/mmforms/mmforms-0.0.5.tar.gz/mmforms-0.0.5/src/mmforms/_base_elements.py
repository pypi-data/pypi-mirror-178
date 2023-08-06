from collections import OrderedDict
from typing import TypeVar, Union, Any

from markupsafe import Markup

from .factories import MethodFactory

Input = TypeVar('Input')
Select = TypeVar('Select')
InputGroup = TypeVar('InputGroup')


class BaseForm:
    name: str
    elements: OrderedDict[Any, Any]

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

    def compile(self, raw: bool = False, markup: bool = False, objects: bool = False) -> Union[str, Markup, dict, OrderedDict]:
        return MethodFactory.compile(raw, markup, objects, self.elements)

    def element_method(self, element_name: str, method: str, value: str) -> None:
        if element_name in self.elements:
            if hasattr(self.elements[element_name], method):
                self.elements[element_name].__getattribute__(method)(value)
        return None


class BaseInputGroup:
    elements: OrderedDict
    attributes: dict

    def __init__(self, *args: Union[Input, Select]) -> None:
        self.attributes = dict()
        self.elements = OrderedDict(**MethodFactory.add_inputs(args))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.elements})"

    def prep_output(self):
        attributes = [value for value in self.attributes.values()]
        self.elements = OrderedDict(({
            '__start___': f"<div {''.join(attributes)}>",
            **self.elements,
            '__end___': '</div>'
        }))

    def compile(self, raw: bool = False, markup: bool = False, objects: bool = False) -> Union[str, Markup, dict, OrderedDict]:
        self.prep_output()
        return MethodFactory.compile(raw, markup, objects, self.elements)

    def class_(self, class_: str):
        self.attributes["class"] = f'class="{class_}" '
        return self

    def id(self, id_: str):
        self.attributes["id"] = f'id="{id_}" '
        return self

    def style(self, style: str):
        self.attributes["style"] = f'style="{style}" '
        return self

    def attr(self, value: str):
        self.attributes[f"attr_{(len(self.attributes) + 1)}"] = f'{value} '
        return self


class BaseSelect:
    element_name: str
    attributes: dict
    options_: dict
    selected_: str

    def __init__(self, element_name: str, disable_default: bool = False):
        self.attributes = dict()
        self.options_ = dict()
        self.element_name = element_name
        if not disable_default:
            self._name = f'name="{element_name}" '
            self._id = f'id="{element_name}" '

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.element_name} -> {dict(**self.attributes)} -> {dict(**self.options_)}"

    def compile(self, raw: bool = False) -> Union[str, Markup]:
        start_tag = f'<select {"".join([value for value in self.attributes.values()])}>'
        options = [f'<option value="{key}" {"selected" if key == self.selected_ else ""}>{value}</option>' for key, value in self.options_.items()]
        out = f'{start_tag} {"".join(options)} </select>'
        if raw:
            return out
        return Markup(out)

    def options(self, options: dict):
        self.options_.update(**options)
        return self

    def selected(self, selected: str):
        self.selected_ = selected
        return self

    def name(self, name: str):
        self.attributes["name"] = f'name="{name}" '
        return self

    def id(self, id_: str):
        self.attributes["id"] = f'id="{id_}" '
        return self

    def name_and_id(self, name_id_: str):
        self.attributes["id"] = f'id="{name_id_}" '
        self.attributes["name"] = f'name="{name_id_}" '
        return self

    def class_(self, class_: str):
        self.attributes["class"] = f'class="{class_}" '
        return self

    def style(self, style: str):
        self.attributes["style"] = f'style="{style}" '
        return self

    def required(self):
        self.attributes["required"] = 'required="required" '
        return self

    def disabled(self):
        self.attributes["checked"] = 'disabled="disabled" '
        return self

    def readonly(self):
        self.attributes["checked"] = 'readonly="readonly" '
        return self

    def multiple(self):
        self.attributes["multiple"] = 'multiple="multiple" '
        return self

    def size(self, size: int):
        self.attributes["size"] = f'size="{size}" '
        return self


class BaseInput:
    element_name: str
    attributes: dict

    def __init__(self, element_name: str, disable_default: bool = False):
        self.element_name = element_name
        self.attributes = dict()
        if not disable_default:
            self._name = f'name="{element_name}" '
            self._id = f'id="{element_name}" '

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.element_name} -> {dict(**self.attributes)}"

    def compile(self, raw: bool = False) -> Union[str, Markup]:
        attributes = [value for value in self.attributes.values()]
        out = f'<input {"".join(attributes)}>'

        if raw:
            return out
        return Markup(out)

    def name(self, name: str):
        self.attributes["name"] = f'name="{name}" '
        return self

    def id(self, id_: str):
        self.attributes["id"] = f'id="{id_}" '
        return self

    def name_and_id(self, name_id_: str):
        self.attributes["id"] = f'id="{name_id_}" '
        self.attributes["name"] = f'name="{name_id_}" '
        return self

    def value(self, value: str):
        self.attributes["value"] = f'value="{value}" '
        return self

    def class_(self, class_: str):
        self.attributes["class"] = f'class="{class_}" '
        return self

    def style(self, style: str):
        self.attributes["style"] = f'style="{style}" '
        return self

    def placeholder(self, value: str):
        self.attributes["placeholder"] = f'placeholder="{value}" '
        return self

    def required(self):
        self.attributes["required"] = 'required="required" '
        return self

    def checked(self):
        self.attributes["checked"] = 'checked="checked" '
        return self

    def disabled(self):
        self.attributes["checked"] = 'disabled="disabled" '
        return self

    def readonly(self):
        self.attributes["checked"] = 'readonly="readonly" '
        return self

    def attr(self, value: str):
        self.attributes[f"attr_{(len(self.attributes) + 1)}"] = f'{value} '
        return self

    def t_button(self):
        self.attributes["type"] = 'type="button" '
        return self

    def t_checkbox(self):
        self.attributes["type"] = 'type="checkbox" '
        return self

    def t_color(self):
        self.attributes["type"] = 'type="color" '
        return self

    def t_date(self):
        self.attributes["type"] = 'type="date" '
        return self

    def t_datetime_local(self):
        self.attributes["type"] = 'type="datetime-local" '
        return self

    def t_email(self):
        self.attributes["type"] = 'type="email" '
        return self

    def t_file(self):
        self.attributes["type"] = 'type="file" '
        return self

    def t_hidden(self):
        self.attributes["type"] = 'type="hidden" '
        return self

    def t_image(self):
        self.attributes["type"] = 'type="image" '
        return self

    def t_month(self):
        self.attributes["type"] = 'type="month" '
        return self

    def t_number(self):
        self.attributes["type"] = 'type="number" '
        return self

    def t_password(self):
        self.attributes["type"] = 'type="password" '
        return self

    def t_radio(self):
        self.attributes["type"] = 'type="radio" '
        return self

    def t_range(self):
        self.attributes["type"] = 'type="range" '
        return self

    def t_reset(self):
        self.attributes["type"] = 'type="reset" '
        return self

    def t_search(self):
        self.attributes["type"] = 'type="search" '
        return self

    def t_submit(self):
        self.attributes["type"] = 'type="submit" '
        return self

    def t_tel(self):
        self.attributes["type"] = 'type="tel" '
        return self

    def t_text(self):
        self.attributes["type"] = 'type="text" '
        return self

    def t_time(self):
        self.attributes["type"] = 'type="time" '
        return self

    def t_url(self):
        self.attributes["type"] = 'type="url" '
        return self

    def t_week(self):
        self.attributes["type"] = 'type="week" '
        return self

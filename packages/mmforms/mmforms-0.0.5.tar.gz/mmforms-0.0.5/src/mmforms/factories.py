from collections import OrderedDict
from typing import TypeVar, Optional, Union

from markupsafe import Markup

Div = TypeVar('Div')
BaseInput = TypeVar('BaseInput')


class MethodFactory:
    @staticmethod
    def add_inputs(args, elements: Optional[OrderedDict] = None) -> OrderedDict:
        if elements is None:
            elements = OrderedDict()
        if args:
            for arg in args:
                elements[arg.element_name] = arg
        return elements

    @staticmethod
    def add_input_groups(args, elements: OrderedDict) -> OrderedDict:
        for i, arg in enumerate(args):
            if hasattr(arg, "elements"):
                for ii, (ik, iv) in enumerate(arg.compile(objects=True).items()):
                    if "__" in ik:
                        elements.update({f"__{i}:{ii}__": iv})
                    elif ik in elements:
                        elements.update({f"{ik}_{i}": iv})
                    else:
                        elements.update({ik: iv})
        return elements

    @staticmethod
    def compile(raw: bool, markup: bool, objects: bool, elements: OrderedDict) -> Union[str, Markup, dict]:

        if objects:
            return elements

        _compile = dict()
        for k, v in elements.items():
            if isinstance(v, str):
                _compile[k] = Markup(v)
                continue
            if hasattr(v, "compile"):
                _compile[k] = Markup(v.compile())

        if raw:
            return "".join([value for value in _compile.values()])

        if markup:
            return Markup("".join([value for value in _compile.values()]))

        return _compile

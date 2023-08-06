from collections import OrderedDict
from typing import TypeVar

Div = TypeVar('Div')
BaseInput = TypeVar('BaseInput')


class MethodFactory:
    @staticmethod
    def add_inputs(args, elements: OrderedDict) -> OrderedDict:
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
                for ii, (ik, iv) in enumerate(arg.elements.items()):
                    if "__" in ik:
                        elements.update({f"__{i}:{ii}__": iv})
                    elif ik in elements:
                        elements.update({f"{ik}_{i}": iv})
                    else:
                        elements.update({ik: iv})
        return elements

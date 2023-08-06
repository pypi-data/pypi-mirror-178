from ._base_elements import BaseInput, BaseInputGroup, BaseSelect


class Select(BaseSelect):
    def __init__(self, *args):
        super().__init__(*args)
        if "class" not in self.attributes:
            self.attributes["class"] = 'class="form-control" '

    def class_(self, class_: str):
        self.attributes["class"] = f'class="form-control {class_}" '
        return self


class Input(BaseInput):

    def __init__(self, *args):
        super().__init__(*args)
        if "class" not in self.attributes:
            self.attributes["class"] = 'class="form-control" '

    def class_(self, class_: str):
        self.attributes["class"] = f'class="form-control {class_}" '
        return self


class InputGroup(BaseInputGroup):

    def __init__(self, *args):
        super().__init__(*args)
        if "class" not in self.attributes:
            self.attributes["class"] = 'class="input-group" '

    def class_(self, class_: str):
        self.attributes["class"] = f'class="input-group {class_}" '
        return self

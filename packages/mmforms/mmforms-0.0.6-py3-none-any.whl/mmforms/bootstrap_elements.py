from ._base_elements import BaseInput, BaseLabel, BaseForm, BaseInputSelect


class Form(BaseForm):
    def __init__(self, *args):
        super().__init__(*args)


# Disabling this for now, as I'm finding it hard to see the use case.
# class InputGroup(BaseInputGroup):
#
#     def __init__(self, *args):
#         super().__init__(*args)
#         if "class" not in self.attributes:
#             self.attributes["class"] = 'class="input-group" '
#
#     def class_(self, class_: str):
#         self.attributes["class"] = f'class="input-group {class_}" '
#         return self

class Label(BaseLabel):

    def __init__(self, *args):
        super().__init__(*args)


class InputSelect(BaseInputSelect):
    def __init__(self, *args):
        super().__init__(*args)
        if "class" not in self.attributes:
            self.attributes["class"] = 'class="form-select" '

    def class_(self, class_: str):
        self.attributes["class"] = f'class="form-select {class_}" '
        return self


# Still working on this one.
# class InputRadio(BaseInputRadio):
#     def __init__(self, *args):
#         super().__init__(*args)
#         if "class" not in self.attributes:
#             self.attributes["class"] = 'class="form-select" '
#
#     def class_(self, class_: str):
#         self.attributes["class"] = f'class="form-select {class_}" '
#         return self


class Input(BaseInput):

    def __init__(self, *args):
        super().__init__(*args)
        if "class" not in self.attributes:
            type_ = self.attributes.get("type", None)
            if type_ == '"type="radio" "':
                self.attributes["class"] = 'class="form-check-input" '
            else:
                self.attributes["class"] = 'class="form-control" '

    def class_(self, class_: str):
        type_ = self.attributes.get("type", None)
        if type_ == '"type="radio" "':
            self.attributes["class"] = f'class="form-check-input {class_}" '
        else:
            self.attributes["class"] = f'class="form-control {class_}" '
        return self

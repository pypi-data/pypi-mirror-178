from ._base_elements import BaseLabel, BaseInput, BaseForm, BaseInputSelect, BaseInputRadio


class Form(BaseForm):
    def __init__(self, *args):
        super().__init__(*args)


# Disabling this for now, as I'm finding it hard to see the use case.
# class InputGroup(BaseInputGroup):
#     def __init__(self, *args):
#         super().__init__(*args)

class Label(BaseLabel):
    def __init__(self, *args):
        super().__init__(*args)


class InputSelect(BaseInputSelect):
    def __init__(self, *args):
        super().__init__(*args)


class InputRadio(BaseInputRadio):
    def __init__(self, *args):
        super().__init__(*args)


class Input(BaseInput):
    def __init__(self, *args):
        super().__init__(*args)

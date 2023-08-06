import re

from markupsafe import Markup


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

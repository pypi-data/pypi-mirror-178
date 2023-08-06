# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# %run __init__.py
# %load_ext lab_black

"""
extends standard ipywidgets to facilitate initialisation from jsonschema
"""

from ipyautoui.constants import MAP_JSONSCHEMA_TO_IPYWIDGET
import ipywidgets as w
import traitlets as tr
from copy import deepcopy
from ipyautoui._utils import obj_from_importstr
from ipyautoui.custom import modelrun, markdown_widget, editgrid, filechooser
from ipyautoui._utils import remove_non_present_kwargs
from datetime import datetime


#  -- CHANGE JSON-SCHEMA KEYS TO IPYWIDGET KEYS -------------


def update_keys(di, di_map=MAP_JSONSCHEMA_TO_IPYWIDGET):
    update_key = lambda key, di_map: di_map[key] if key in di_map.keys() else key
    return {update_key(k, di_map): v for k, v in di.items()}


def create_widget_caller(schema, calling=None):
    """
    creates a "caller" object from the schema.
    this renames schema keys as follows to match ipywidgets:
        ```
        {
            'minimum': 'min',
            'maximum': 'max',
            'enum': 'options',
            'default': 'value',
            'description': 'autoui_description'
        }
        ```


    Args:
        schema: dict, json schema
        calling, default=None: the class that will be called by the
            returned "caller" object. if not None, args not present in the class
            are removed from "caller"

    Returns:
        caller: dict, object that is passed the "calling" widget
            initialised like ```calling(**caller)```

    """
    caller = deepcopy(schema)
    caller = update_keys(schema)
    caller = {k: v for k, v in caller.items() if k != "description"}
    caller = {k: v for k, v in caller.items() if k != "title"}
    if calling is not None:
        caller = remove_non_present_kwargs(calling, caller)
    return caller


class IntText(w.IntText):  # TODO: add value to these as arg?
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class IntSlider(w.IntSlider):
    """Example:
    >>> from ipyautoui.test_schema import TestAutoLogic
    >>> import ipywidgets as w
    >>> sch = TestAutoLogic.schema()["properties"]['int_slider']
    >>> IntSlider(sch)
    IntSlider(value=2, max=3, min=1)
    >>> sch['type']
    'integer'
    """

    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


# TODO: add `schema` as a `tr.Dict()` with a validator and observe
#       on_change re-initialize the widget...


class FloatText(w.FloatText):
    """Example:
    >>> from ipyautoui.test_schema import TestAutoLogic
    >>> import ipywidgets as w
    >>> sch = TestAutoLogic.schema()["properties"]['float_text']
    >>> FloatText(sch)
    FloatText(value=2.2)
    >>> sch['type']
    'number'
    """

    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class FloatSlider(w.FloatSlider):
    """Example:
    >>> from ipyautoui.test_schema import TestAutoLogic
    >>> import ipywidgets as w
    >>> sch = TestAutoLogic.schema()["properties"]['float_slider']
    >>> FloatSlider(sch)
    FloatSlider(value=2.2, max=3.0, min=1.0)
    >>> sch['type']
    'number'
    """

    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class IntRangeSlider(w.IntRangeSlider):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        self.caller["min"] = self.schema["items"][0]["minimum"]
        self.caller["max"] = self.schema["items"][0]["maximum"]
        super().__init__(**self.caller)


class FloatRangeSlider(w.FloatRangeSlider):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        self.caller["min"] = self.schema["items"][0]["minimum"]
        self.caller["max"] = self.schema["items"][0]["maximum"]
        super().__init__(**self.caller)


class Text(w.Text):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class Textarea(w.Textarea):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class Combobox(w.Combobox):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class Dropdown(w.Dropdown):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class SelectMultiple(w.SelectMultiple):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class Checkbox(w.Checkbox):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class DatePickerString(w.HBox, tr.HasTraits):
    _value = tr.Unicode(allow_none=True, default_value=None)

    def __init__(self, schema):
        """thin wrapper around ipywidgets.DatePicker that stores "value" as
        json serializable Unicode"""
        self.picker = w.DatePicker()
        self.schema = schema
        self._init_controls()
        super().__init__()
        self.children = [self.picker]

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        if "strftime_format" not in value.keys():
            self._strftime_format = "%Y-%m-%d"
        else:
            self._strftime_format = value["strftime_format"]
        if "disabled" not in value.keys():
            self.disabled = False
        else:
            self.disabled = value["disabled"]
        if "default" in value.keys():
            self.value = value["default"]
        self._schema = value

    @property
    def disabled(self):
        return self.picker.disabled

    @disabled.setter
    def disabled(self, value):
        self.picker.disabled = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) == str:
            self.picker.value = datetime.strptime(value, self.strftime_format)
        else:
            self.picker.value = value

    @property
    def strftime_format(self):
        return self._strftime_format

    @strftime_format.setter
    def strftime_format(self, value):
        self._strftime = value
        self._update_change("change")

    def _init_controls(self):
        self.picker.observe(self._update_change, "value")

    def _get_value(self):
        try:
            return self.picker.value.strftime(self.strftime_format)
        except:
            return None

    def _update_change(self, on_change):
        self._value = self._get_value()


class FileChooser(filechooser.FileChooser):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


# class Grid(w.Grid):
#     def __init__(self, schema):
#         self.schema = schema
#         self.caller = create_widget_caller(schema)
#         super().__init__(**self.caller)


class ColorPicker(w.ColorPicker):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema)
        super().__init__(**self.caller)


class AutoPlaceholder(w.Textarea):
    def __init__(self, schema):
        txt = f"""
PLACEHOLDER WIDGET 
schema: 
{str(schema)}
"""
        super().__init__(value=txt)


class RunName(modelrun.RunName):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(schema, calling=modelrun.RunName)
        super().__init__(**self.caller)


# class EditGrid(editgrid.EditGrid):
#     def __init__(self, schema):
#         self.schema = schema
#         self.caller = create_widget_caller(schema, calling=editgrid.EditGrid)
#         super().__init__(**self.caller)


class AutoMarkdown(markdown_widget.MarkdownWidget):
    def __init__(self, schema):
        self.schema = schema
        self.caller = create_widget_caller(
            schema, calling=markdown_widget.MarkdownWidget
        )
        super().__init__(**self.caller)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

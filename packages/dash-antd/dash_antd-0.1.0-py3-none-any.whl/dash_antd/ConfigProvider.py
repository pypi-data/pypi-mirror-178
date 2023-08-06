# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ConfigProvider(Component):
    """A ConfigProvider component.
Set components spacing.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- components (dict; optional):
    Set component specific design tokens.

    `components` is a dict with keys:


- input (dict; optional):
    Set common properties for Input component.

    `input` is a dict with keys:

    - autoComplete (string; optional)

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- space (dict; optional):
    Set sizing in Space component.

    `space` is a dict with keys:

    - size (number; optional)

- token (dict; optional):
    Set global design tokens.

    `token` is a dict with keys:


- use_compact (boolean; optional):
    Create a dark theming for all child components.

- use_dark_theme (boolean; optional):
    Create a dark theming for all child components."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_antd'
    _type = 'ConfigProvider'
    @_explicitize_args
    def __init__(self, children=None, input=Component.UNDEFINED, space=Component.UNDEFINED, components=Component.UNDEFINED, token=Component.UNDEFINED, use_dark_theme=Component.UNDEFINED, use_compact=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'components', 'input', 'key', 'space', 'token', 'use_compact', 'use_dark_theme']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'components', 'input', 'key', 'space', 'token', 'use_compact', 'use_dark_theme']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(ConfigProvider, self).__init__(children=children, **args)

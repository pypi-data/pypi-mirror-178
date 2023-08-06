<img src="https://raw.githubusercontent.com/NaturalHistoryMuseum/ckantools/main/.github/nhm-logo.svg" align="left" width="150px" height="100px" hspace="40"/>

# ckantools

[![CKAN](https://img.shields.io/badge/ckan-2.9.5-orange.svg?style=flat-square)](https://github.com/ckan/ckan)
[![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg?style=flat-square)](https://www.python.org/)

_Utilities and common methods for CKAN extensions._


# Overview

A collection of methods, decorators, and anything else that might be useful.

_ckantools is still very much in development, and is prone to frequent changes that may or may not work._

# Installation

```shell
pip install ckantools
```

# Usage

## Actions

Use the `@action` decorator to add actions:
```python
# logic/actions/module_name.py

from ckantools.decorators import action

schema = {
        'parameter_1': [not_missing, str],
        'parameter_2': [ignore_missing, int_validator]
    }

helptext = 'This action only exists as an example, so does not actually anything.'

@action(schema, helptext, get=False, other_decorator_1, other_decorator_2)
def example_action(parameter_1, parameter_2):
    # ...
```

Or the `@basic_action` decorator if you want to load the action but don't want any of the other features (schema loading, auto auth, etc):
```python
from ckantools.decorators import basic_action

@basic_action
@toolkit.chained_action
def example_action(next_func, context, data_dict):
    # ...
```

And then load the action(s) in `plugin.py`:
```python
# plugin.py

from .logic.actions import module_name
from ckantools.loaders import create_actions
from ckan.plugins import implements, interfaces, SingletonPlugin

class ExamplePlugin(SingletonPlugin):
    implements(interfaces.IActions)

    # IActions
    def get_actions(self):
        return create_actions(module_name)
```

Main benefits to using the decorator:
- automatically calls relevant auth function
- injects items defined in schema as function args
- allows you to define long or complex schemas and helptexts without cluttering up code and/or affecting readability
- neater and easier to maintain than having to list out all of the actions you want to load, e.g.
  ```python
        ## IActions
  def get_actions(self):
    return {
        'example_action': module_name.example_action,
        'other_action': module_name.other_action,
        'other_other_action': module_name.other_other_action,
        # etc
    }
  ```

## Auth

Loading auth functions is similar to actions, i.e. use the `@auth` decorator.

The decorator has three args, all of which are optional:
- `proxy`: the name of an existing auth function to call that function first
- `keymapping`: if the keys are different between this auth function and the proxy auth function, use this to rename them
- `anon`: boolean, if true, apply the `toolkit.auth_allow_anonymous_access` decorator.

```python
# logic/auth/module_name.py

from ckantools.decorators import auth

# all of the args are optional
@auth(anon=True)
def example_action(context, data_dict):
    # no proxy
    # anonymous access is allowed
    # then the custom auth logic:
    return {'success': data_dict.get('parameter_2') == 'carrots'}

# with args
@auth('example_action', {'param_1': 'parameter_2'})
def other_action(context, data_dict):
    # checks access to example_action first
    # the arg param_1 from this action is the same as parameter_2 in example_action (not all args/parameters have to be mapped, just the relevant ones)
    # anonymous access is not allowed
    # if it passes all that:
    return {'success': True}
```

The auth functions can then be loaded in `plugin.py`:
```python
# plugin.py

from .logic.auth import module_name
from ckantools.loaders import create_auth
from ckan.plugins import implements, interfaces, SingletonPlugin

class ExamplePlugin(SingletonPlugin):
    implements(interfaces.IActions)

    # IAuthFunctions
    def get_auth_functions(self):
        return create_auth(module_name)
```

Main benefits to using the decorator:
- reduces repetition of complex auth logic
- as with the action decorator, it's neater and easier to maintain than having to list out all of the auth functions to load

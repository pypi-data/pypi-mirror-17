mock_import
~~~~~~~~~

A helper function to mask `ImportError` s on a scoped code, using the `with`
statement, or in method a method used as a decorator.
Failed imports will be ignored, unless specified by the *do_not_mock* argument.

The *do_not_mock* argument is a package or module name, or package or module
names list. When specified, and imported in the scoped mocked code, importing
them must succeed. If `None` (the default) then no import must succeed.


Mocking import for a code block:
    >>> with mock_import():
    ...     import do_not_exists


Mocking import as a decorator:
    >>> @mock_import()
    ... def method():
    ...     import do_not_exists



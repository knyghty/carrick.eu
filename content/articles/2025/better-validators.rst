A slight simplification of class based validators
#################################################

:date: 2025-08-02
:tags: django
:has_code: true

Lately I'm trying to find ways to use Django in a more modern way.
Being able to use type hints for validation, knowing what's going
to be in ``form.cleaned_data``. That sort of thing. I'm mostly failing.

The best I've managed lately is to reduce some boilerplate in class
based validators. I'm not sure if it's really expected to make your own
class based validators since I couldn't find any good documentation on it.

However, you can read through the source code to see how it's done there.

Typically you declare them like this:

.. code-block:: python

    from django.core.exceptions import ValidationError
    from django.utils.deconstruct import deconstructible


    @deconstructible
    class FileSizeValidator:
        def __init__(self, max_size):
            self.max_size = max_size

        def __call__(self, file):
            if file.size > self.max_size:
                raise ValidationError(_("Max file size is %s") % self.max_size)

        def __eq__(self, other):
            return isinstance(other, FileSizeValidator) and self.max_size == other.max_size

The reason ``__eq__`` is needed is because Django needs to check
if a validator has changed, so a new migration is needed. Quite
annoying to need to write this, however. Another small issue is that
my linter enjoys complaining about implementing ``__eq__`` but not
``__hash__``.

Dataclasses can save the day since they have default implementations
of ``__eq__`` and ``__hash__``. So we can at least do this:

.. code-block:: python

    import dataclasses
    from django.core.exceptions import ValidationError
    from django.utils.deconstruct import deconstructible


    @deconstructible
    @dataclasses.dataclass
    class FileSizeValidator:
        max_size: int

        def __call__(self, file: "FieldFile") -> None:
            if file.size > self.max_size:
                raise ValidationError(_("Max file size is %s") % self.max_size)

It's a small win.

There's a small difference. A dataclass's ``__eq__`` checks the exact type,
whereas before we were using ``isinstance``, to allow for subclassing.

Still, in most cases, I would do this differently. Unless I have a lot of
different file size requirements, I'd rather just use a ``partial``:

.. code-block:: python

    from functools import partial
    from django.core.exceptions import ValidationError


    def validate_file_size(file: "FieldFile", max_size: int) -> None:
        if file.size > max_size:
            raise ValidationError(_("Max file size is %s") % max_size)


    validate_small_file = partial(validate_file_size, max_size=524_288)
    validate_medium_file = partial(validate_file_size, max_size=1_048_576)
    validate_large_file = partial(validate_file_size, max_size=10_485_760)

Shorter, and if you ask me, easier to read.

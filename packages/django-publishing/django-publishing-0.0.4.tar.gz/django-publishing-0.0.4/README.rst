==========
PUBLISHING
==========

Publishing is a simple publishing tool for django to make changes on your
models based on a workflow.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "publishing" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'publishing',
    ]

2. Add the model mixin `PublishModelMixin` to your model class.

3. Add the admin mixin `PublishAdminMixin` to your admin class.

4. Run `python manage.py migrate` to add publishing related fields to models.

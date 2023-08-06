``django-model-reference`` defines a simple :cls:`model_reference.Reference`
model that hold named references to specific instances of any Django model.

Usage
=====

References are controlled by the :func:`register()` and :func:`load` functions of
the ``model_reference`` module. These function are also mirrored by the
corresponding methods in the ``Reference.objects`` manager. To register a
reference, simply pass the object and either a unique name or a unique suffix::

    from model_reference import register, load
    from django.contrib.auth.models import User

    # Fetch some objects
    john = User.objects.get(username='john')
    ringo = User.objects.get(username='ringo')

    # Register references in the database
    register(john, 'favorite beatle')
    register(ringo, suffix='drummer')

The name for each reference is unique. If the register function is called with
the explicit ``suffix`` argument, it will register the instance as
``<app_label>.<model>:suffix``, which in our case becomes ``'auth.user:drummer'``.

In order to retrieve the objects referred by the Reference object, we can use
the :func:`load` function::

>>> load('favorite beatle')
<User: john>
>>> load('drummer', model=User)
<User: ringo>

Objects registered with the suffix form of the register function should pass a
model class in order to construct the complete name string. This is equivalent
as creating the string by hand:

>>> load('auth.user:drummer')
<User: ringo>


Empty references
================

If one request a non-existing reference to the load() function, it raises an
:error:`model_reference.EmptyReferenceError`. Users can register factory
functions to create these objects on-the-fly.

The default way of registering factory function is via the :func:`model_reference.factory`
decorator. It must be called with a reference string (or suffix + model) and
decorates a function that return a new instance and is called without arguments::

    @factory('drummer', model=User)
    def make_ringo():
        user, created = User.object.get_or_create(
            username=ringo,
            first_name='Richard'
            last_name='Starkley',
            email='ringo@applerecords.co.uk'
        )
        return user

If a new instance is created, the function is responsible to save it in the
database
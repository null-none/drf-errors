DRF Errors
===================

**Extension for Django REST framework error display**

Requirements
------------
-  Python (2.7, 3.5, 3.6)
-  Django (3.0.6+)
-  Django REST framework (>=3.5)

Installation
------------

By running installation script

Using pip

.. code:: bash

    $ pip install drf-errors


Overview
--------

This package extends default error JSON body providing configurable error codes
and more consumable response structure.

It turns default JSON body of HTTP 400 response, which look like this

.. code:: python

    {
        "name": ["This field is required."],
        "password": ["This field may not be blank."]
    }

into

.. code:: python

    {
      "message": "This field is required.",
      "errors": [
        {
          "field": "email",
          "message": "This field is required."
        },
        {
          "field": "password",
          "message": "This field is required."
        }
      ],
      "status_code": 400
    }

Usage
-----

Simply add a SerializerErrorMessagesMixin to your serializer or model serializer class

.. code:: python

    from drf_errors.mixins import SerializerErrorMessagesMixin

    class MySerializer(SerializerErrorMessagesMixin, ModelSerializer):

If you want to change default library settings and provide your own set of error codes just add following in your
settings.py

.. code:: python

    DRF_ERRORS = {
        FIELD_ERRORS = {
            'CharField': {'required': 'my_custom_error_code', 'null': 'my_custom_error_code'}
        }
        VALIDATOR_ERRORS = {
            'UniqueValidator': 'my_custom_error_code'
        },
        EXCEPTION_DICT = {
            'PermissionDenied': 'my_custom_error_code'
        }
    }

Custom serializer validation
----------------------------

If you need custom field validation or validation for whole serializer register your validation in serializer class

.. code:: python

    class PostSerializer(SerializerErrorMessagesMixin,
                         serializers.ModelSerializer):
        class Meta:
            model = Post

        def validate_title(self, value):
            if value[0] != value[0].upper():
                raise ValidationError('First letter must be an uppercase')
            return value

        def validate(self, attrs):
            category = attrs.get('category)
            title = attrs.get('title')
            if category and category not in title:
                raise ValidationError('Title has to include category')
            return attrs

        FIELD_VALIDATION_ERRORS = {'validate_title': 'invalid_title'} # register your own validation method and assign it to error code
        NON_FIELD_ERRORS = {'Title has to include category': 'no_category'} # register non field error messages and assign it to error code

If you want to raise field error in validate method use register_error method provided by a mixin

.. code:: python

    class PostSerializer(SerializerErrorMessagesMixin,
                         serializers.ModelSerializer):
        class Meta:
            model = Post

        def validate(self, attrs):
            category = attrs.get('category')
            title = attrs.get('title')
            if category and category not in title:
                self.register_error(error_message='Title has to include category',
                                    error_code='no_category',
                                    field_name='title')
            return attrs

Error codes not related to serializer validation
------------------------------------------------

To turn other type of errors responses into friendly errors responses with error codes
add this exception handler to your REST_FRAMEWORK settings

.. code:: python

    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER':
        'drf_errors.handlers.drf_exception_handler'
    }

.. image:: https://travis-ci.org/adrianoveiga/django-file-validator.svg?branch=master
    :target: https://travis-ci.org/adrianoveiga/django-file-validator

.. image:: https://badge.fury.io/py/django-file-validator.svg
    :target: https://badge.fury.io/py/django-file-validator


django-file-validator
------------------------

Simple project to validate FileFields/ImageFields, like max size of uploaded file.

Until now, there is only one validator: MaxSizeValidator.

NOT WORKING WITH NEW DJANGO 1.10.

Dependencies
------------

- Django 1.8 or higher (not tested on previous versions) but lower than 1.10!!


Installation
------------

.. code-block:: python

   pip install django-file-validator


Usage
-----

In your models, import and use MaxSizeValidator:

.. code-block:: python

    from django_file_validator.validators import MaxSizeValidator

    class YourModel(models.Model):
        
        . . .

        image = models.ImageField( null=True, blank=True, upload_to='uploads/yourmodel/img/', validators=[MaxSizeValidator()])

        . . . 


You can change the max size value passing a parameter on each attibute:

.. code-block:: python

    from django_file_validator.validators import MaxSizeValidator

    class YourModel(models.Model):
        
        . . .

        default_image = models.ImageField( null=True, blank=True, upload_to='uploads/yourmodel/img/', validators=[MaxSizeValidator()])
        big_image = models.ImageField( null=True, blank=True, upload_to='uploads/yourmodel/img/', validators=[MaxSizeValidator(2048)])
        small_image = models.ImageField( null=True, blank=True, upload_to='uploads/yourmodel/img/', validators=[MaxSizeValidator(256)])

        . . . 



Configurations
--------------

- FILE_SIZE_LIMIT_IN_KILOBYTES
    You can change the default max size limit of uploaded files, just putting this variable on settings.py. Default value is 512 kB.

    .. code-block:: python
        
        FILE_SIZE_LIMIT_IN_KILOBYTES=512


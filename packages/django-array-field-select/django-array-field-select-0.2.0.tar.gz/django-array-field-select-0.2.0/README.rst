=====
About
=====
A replacement for Django's ArrayField with a multiple select form field.  This
only makes sense if the underlying base_field is using choices.

How To Use
==========
Replace all instances of your Django ArrayField model field with the new
ArrayField.  No functionality will be changed, except for the form field.

**Example**

.. code:: python

    from django.db import models
    from array_field_select.fields import ArrayField

    class Student(models.Model):
        YEAR_IN_SCHOOL_CHOICES = (
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
        )
        years_in_school = ArrayField(
            models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
        )

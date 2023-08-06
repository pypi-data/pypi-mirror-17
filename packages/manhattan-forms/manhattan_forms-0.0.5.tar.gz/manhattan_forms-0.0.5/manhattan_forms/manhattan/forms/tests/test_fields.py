from datetime import time

from mongoframes import *
from pymongo import MongoClient
import pytest
from werkzeug.datastructures import MultiDict

from manhattan.forms import BaseForm
from manhattan.forms import fields


# Fixtures

class Dragon(Frame):
    """
    A dragon.
    """

    _fields = {
        'name',
        'breed'
        }

    def __str__(self):
        return '{d.name} ({d.breed})'.format(d=self)


@pytest.fixture(scope='session')
def mongo_client(request):
    """Connect to the test database"""

    # Connect to mongodb and create a test database
    Frame._client = MongoClient('mongodb://localhost:27017/manhattan_forms')

    def fin():
        # Remove the test database
        Frame._client.drop_database('manhattan_forms')

    request.addfinalizer(fin)

    return Frame._client

@pytest.fixture(scope='function')
def dragons(mongo_client):
    """Create a collection of dragons"""

    Dragon(name='Burt', breed='Fire-drake').insert()
    Dragon(name='Fred', breed='Fire-drake').insert()
    Dragon(name='Albert', breed='Cold-drake').insert()


# Tests

def test_checkbox_field():
    """Support for multiple checkboxes"""

    class MyForm(BaseForm):

        foo = fields.CheckboxField(
            'Foo',
            choices=[
                ('bar', 'Bar'),
                ('zee', 'Zee'),
                ('omm', 'Omm')
                ]
            )

    # Check a valid selections are supported
    form = MyForm(MultiDict({'foo': ['bar', 'zee', 'omm']}))
    assert form.validate() == True
    assert form.data['foo'] == ['bar', 'zee', 'omm']

    # Check invalid selections raise an error
    form = MyForm(MultiDict({'foo': ['one', 'zee', 'omm']}))
    assert form.validate() == False
    assert form.errors['foo'][0] == "'one' is not a valid choice for this field"

def test_document_checkboxes_form(dragons):
    """
    Support for multiple checkboxes generated from documents in the database.
    """

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            filter=Q.breed == 'Fire-drake',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    assert my_form.foo.choices == choices

    # Check setting id and label attributes
    class MyForm(MyForm):

        class Meta:
            csrf = False

        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            id_attr='name',
            label_attr='breed',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [(d.name, d.breed) for d in Dragon.many(sort=[('name', ASC)])]
    assert my_form.foo.choices == choices

    # Check setting a projection
    class MyForm(MyForm):

        class Meta:
            csrf = False

        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            label_attr='breed',
            sort=[('name', ASC)],
            projection={'name': True}
            )

    my_form = MyForm()
    choices = [(d._id, None) for d in Dragon.many(sort=[('name', ASC)])]
    assert my_form.foo.choices == choices

    # Check setting a filter as a lambda argument
    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            filter=lambda form, field: Q.breed == 'Fire-drake',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    assert my_form.foo.choices == choices

    # Check setting a limit
    class MyForm(MyForm):

        class Meta:
            csrf = False

        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            label_attr='name',
            sort=[('name', ASC)],
            limit=2
            )

    my_form = MyForm()
    choices = [
        (d._id, d.name) for d in Dragon.many(sort=[('name', ASC)], limit=2)]
    assert my_form.foo.choices == choices

def test_time_field():
    """Accept a valid time"""

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.TimeField('Foo')

    # Check valid times are accepted
    form = MyForm(MultiDict({'foo': '22:50'}))
    assert form.validate() == True
    assert form.data['foo'] == time(22, 50)

    # Check invalid times raise an error
    form = MyForm(MultiDict({'foo': 'Ten-fifty'}))
    assert form.validate() == False
    assert form.errors['foo'][0] == 'Not a valid time value.'

    # Check a custom format can be used to accept seconds
    class MyForm(BaseForm):

        foo = fields.TimeField('Foo', format='%H:%M:%S')

    form = MyForm(MultiDict({'foo': '22:50:55'}))
    assert form.validate() == True
    assert form.data['foo'] == time(22, 50, 55)
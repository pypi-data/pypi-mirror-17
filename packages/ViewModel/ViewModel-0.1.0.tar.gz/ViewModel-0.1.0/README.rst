.. ViewModels documentation master README file.

==========
viewModels
==========

Uses_
-----

ViewModels are wrappers for the data 'model', that include details of the data
useful in generating views.  Generally the concept is to allow information
and flexibly independent of the constraints of the underlying db.

    - `Interface to provide access to database`_.
    - `Repository for description of data (schema)`_.
    - `Increasing range of types available to applications`_.

Background_
-----------

    - `History`_.
    - `Data tables/collections and data views`_.

Instructions_
-------------

    - 'Creating a ViewModel'_.


_`Uses`
-------


Interface to provide access to database
+++++++++++++++++++++++++++++++++++++++

To access a collection in a simply Mongo through pymongo could not
be much simpler. Similarly with other
However this does not provide:
    - abstraction between code and database
    - types not covered in the BSON type set
    - joins
    - a record of schema in use

All these advantages are provided by using ViewModel.  However there are times
when none of these justifies an additional layer.  The more complex the
collection, the greater the amount of code, generally the greater the value
of using ViewObject

Abstraction between code and database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Databases migrate.  The Salt database started with direct SQL, then
SQLAlchemy, then mongodb.  Abstraction assists with migrations.
The current Salt system uses Mongo and directly using the pymongo interface
is can be perfect for simple access.  A rewrite would be needed to change
the db but the code is so small it is not a large barrier for small simple
cases. But more complex cases are another matter!

Repository for description of data (schema)
+++++++++++++++++++++++++++++++++++++++++++

NoSql collections (or tables) can effectively be irregular with different
fields present potentially in every entry.  While with SQL,just examining a
row can give a reasonable view of that schema, it can be less clear from
NoSql.  Even with SQL, the schema recorded is restricted to what the database
engine requires, and lacks richer descriptions of the data and rules not
implemented by the database.

Increasing range of types available to applications
+++++++++++++++++++++++++++++++++++++++++++++++++++

ViewModel provides mapping between the data in the database and the data
seen by the application. Far more descriptive types and move complex types
can be used by the application with the mapping between these types and
the underlying storage format handle by the ViewModel


_`Background`
-------------
    - `History`_.
    - `Data tables/collections and data views`_.

History
+++++++

The original Salt project development worked with SQL at a time when
the SQLAlchemy project was still in early stages. So Salt developed its own
layer to abstract to the database in 2007 around the same time as SQLAlchemy
was developed.  Both the salt 'DataModel' and SQLAlchemy libraries developed
specific advantages, but as a popular open sourced project, SQLAlchemy became
the more mature product.
In 2015 the Salt project chose to replace the internal 'DataModel' library
with the SQLAlchemy, due to wider use and greater development of the open
source project, but then found several key features of 'DataModel' were missing
from SQLAlchemy.
The solution was a new library 'ModelView', which acted as an abstraction
layer between SQLAlchemy and the application.  The name 'ModelView' came from
the fact that the main elements present in 'DataModel' that were missing
from SQLAlchemy were data extended data schema information that were also
useful in providing data description to views.

The next step brought the current 'ViewModel', by transforming that library to
become an interface between pymongo and the application.

Data tables/collections and data views
++++++++++++++++++++++++++++++++++++++

The ViewModel package focuses on preparing data for views.  How is the data
in a table/collection to be viewed?  For example,
consider a 'Products' table or collection, where products may be viewed:
    - individually by product code,
    - as a list of products by product group, or by brand
    - as a list through a custom search

These become the views of the data from the database.  It is never relevant
to actually retrieve the entire table/collection for the products as if
processing the entire table, each document will be processed in sequence.
In contrast, there may be other table/collections with either a single or
small fixed number of rows/collections the entire table/collection may constitute
a view.

Further, product could have a join to a 'pack sizes' table/collection and
for some views these are also part of the view.

The main concept is that each table has a set of relevant views of the
table/collection for various uses.  The viewmodel specifies not just the
schema of the table/collection, but the actual views of the table/collection.


_`Instructions`
---------------
    - `Describing a table/collection`_.
    - `Using 'ViewField' derived classes`_.
    - `Building HTML forms`_.
    - `Updating from HTML forms`_.

Describing a table/collection
+++++++++++++++++++++++++++++

Create a class derived from a ModelView, add class attributes
which are 'ViewFields' for each field in the table or collection.  eg.::

    from ViewModel import ViewModel, IdField, TxtField, IntField
    class ProductView(ModelView):
        viewName_ = "Products"
        id = IdField()
        label = TxtField('Label for Email', 8)
        stock_count = IntField()

Using 'ViewField' derived classes
+++++++++++++++++++++++++++++++++

xxx

Building HTML Forms
+++++++++++++++++++

ObjDict can be initialised from lists, from JSON strings, from dictionaries,
from parameter lists or from keyword parameter lists.


Updating from HTML forms
++++++++++++++++++++++++

Custom classes allow for JSON data to result in instantiating objects other
than ObjDict from JSON data.  These custom classes can be sub-classed from ObjDict
or built simply using the :code:`@to_JSON()` and/or :code:`@from_JSON()` decorators.

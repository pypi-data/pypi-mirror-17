.. ViewModels documentation master README file.

==========
viewModels
==========

Uses_
-----

ViewModels are wrappers for the data 'model', that include details of the data
useful in generating views.  The current implementation is with mongoDB for
the bottle framework. Generally the concept is to allow information
and flexibly independent of the constraints of the underlying db.  This provides
for the model and also supports the view code, so simplifies both model and view
code.

- `Interface to provide access to database and abstraction`_.
- `Repository for all information relating to data: schema and beyond`_.
- `Increasing range of types available to applications`_.

Background_
-----------

- `History`_.
- `Data tables/collections and data views`_.

Instructions_
-------------
- `Simple Example`_.
- `Describing a table/collection with ViewFields`_.
- `Using 'ViewField' derived classes`_.
- `Building HTML forms`_.
- `Updating from HTML forms`_.


_`Uses`
-------


Interface to provide access to database and abstraction
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

To access a collection in a simply Mongo through pymongo could not
be much simpler. Similarly with other
However this does not provide:
- abstraction between code and database
- types beyond those covered in the BSON type set
- joins, and joins with 'lazy' exectuion
- a record of schema in use
- support for a web maintenance interface to the database
- web interface supports security and templates for full application

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

Repository for *all* information relating to data: schema and beyond
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A single reposity for all information about data.  Information on both storage
as well as information used for display, all in one place.

Data descriptions can be simple tables/collections or views which comprise multiple
tables which are effectively joined.

The data description provided by viewmodel library, can include extended types
described at a layer of abstraction separate from the storage specification,
allowing the application layer free of the mechanics.

ViewModel was first created for SQL based applications, but then evolved to also
work with NoSQL mongoDB applications.

NoSql collections (or tables) can effectively be irregular with different
fields present potentially in every entry.  While with SQL,just examining a
row can give a reasonable view of that schema, but this can be less clear
from NoSql.  Even with SQL, the schema recorded is restricted to what the database
engine requires, and lacks richer descriptions of the data and rules not
implemented by the database, but a repository for a schema becomes even more
essential with NoSQL.

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
The solution was a new library 'ViewModel', which acted as an abstraction
layer between SQLAlchemy and the application.  The name 'ViewModel' came from
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
- `Simple Example`_.
- `Describing a table/collection with ViewFields`_.
- `Using 'ViewField' derived classes`_.
- `Building HTML forms`_.
- `Updating from HTML forms`_.

Simple example
+++++++++++++++++++
This example is given in advance the instructions or details on how the
components of the example work.  The idea is: read the example to gain an
overview, then see more details to understand more and return to this
example.

The simple database
~~~~~~~~~~~~~~~~~~~~
The consider a database with a table of students.  Rows or Documents have

- an id
- a name
- a course
- year number within course

Code to describe table find an entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The code follows::

    from ViewModel import ViewModel, IdField, TxtField, IntField
    import pymongo

    database = pymongo.MongoClient(dbserver).get_database("example")

    class StudentView(ViewModel):
        viewName_ = "Students"
        #models_ = #<database>.Students
        id = IdField()
        name = TxtField()
        course = IntField()
        #  .... field definitions may  continue

    student = StudentView({},models = database.Students)
    # could have used 'models_' within class to avoid needing 'model' parameter
    # {} empty dictionary to ensure an empty view, not needed if the database
    # does not even exist yet, as with a new database, initial view will always
    # be an empty view

    if len(student) > 0:
        print("oh no, we already have data somehow!")

    students.insert_() #add an empty entry to our view

    with student:  #use with so changes written at end of 'with'
        student.name = 'Fred'

    #ok.... now we have a 'Student' table with one entry

Code to read and update our entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A key concept is that while the class for the view describes a table, set of
tables or joined tables (or collections in Mongo speak), an instance of
a ViewModel is the set of data, or a window of the tables.
Instancing the view actually reads from the
data base in simplest cases, although in more complex cases the data may be read
from the database when accessed, the view instance logically includes all data
from a 'read' operation::

    #same class definition and imports as above

    student = StudentView({'name': 'Fred'},model = database.Students)
    # would save if we could have 'models_' in class definition!

    if not student.course:
        with student:
            student.course_year = 2
            student.course = 'Computing'

Multiple Entry Views
~~~~~~~~~~~~~~~~~~~~~
So far our view has only one entry.  Instance of our view is a window viewing
part of the database.  This window, can be a single row/collection or a logical
group of entries(from rows/collections), and for small tables, may even be
the entire
table/collection. The code that follows adds another entry, so the sample has
more than one entry, then works with a multi entry
view::

    StudentView.models_ = database.Students
    #modify class, add 'models_' as an attribute,
    #this saves specificing 'models_' each time instancing StudentView

    student = StudentView()
    #no dictionary, this gives an empty view (not multi entry yet)

    student.insert_()
    with student:  #adding a second student
        student.name = 'Jane'
        student.course = "Computing"
        student.course_year = 2

    #now our multi entry view for all year 2 Students
    students = StudentView({'course_year':2})

    for student in students:
        print(student.name)

Note how multi entry view instances can be treated as lists. In fact, single
entry views can also be treated as a list, however for convenience view
proprerties for single entry views also allow direct access as one entry. For
a single entry view 'student'::

    student.name == student[0].name


Example Summary
~~~~~~~~~~~~~~~
The example bypasses the power of ViewModels in order to a simple introduction.
A key concept is that classes describe a table ( or collection or set/join
of tables). An *instance* of a ViewModel is one set specific subset, a set of
data from
a table (or set/join of multiple tables).

Describing a table/collection with ViewFields
++++++++++++++++++++++++++++++++++++++++++++++
When creating a class derived from a ViewModel, add class attributes
which are 'ViewFields' for each field in the table or collection.

The example ( 'Simple example'_. ) uses several types of view fields. However
each 'ViewField' can contain information well beyond the type of data.
An alternative name, a short and long description, formating and other display
defaults,  value constraints and many other settings.

In the example, only the 'value' attribute of the "name" ViewField is accessed.
'student.name' does not access the ViewField, but instead returns "value"
attribute of the "name" ViewField.  To access the
actual ViewField (or IntField, TextField etc) and have access to these other
attributes use 'student["name"]'.  thus::

    student.name == student["name"].value


Using 'ViewField' derived classes
+++++++++++++++++++++++++++++++++

All 'fields' are subclassed from ViewField, and represent individual data types.
Each field contains the following properties:

- name: set explicitlty, or defaulting to the property name
- label: set explictily but defaulting to the name
- hint: defaults to '' for display
- value: returns value when field is an attribute of a row object

'ViewModel' interface
+++++++++++++++++++++
The 'ViewModel' provides a base class defines a database table/collection, and each instance of
a ViewModel. Note all system properties and methods start of end with underscore to
avoid name collision with database field names.

ViewModel Interface Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- insert_()
- labelsList_()
- update_()
- <iterate> for row in <ViewModel instance>
- <index>  <ViewModel instance>[row]

ViewModel Interface Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- viewName\_
- models\_
- dbModels\_

ViewModel details
~~~~~~~~~~~~~~~~~
'insert_()' method adds a empty new row (ViewRow instance) to the current ViewModel
instance. At
the next 'update_()', an actual database document/row will be created, provided
some values have been set in the new row.

'labelsList_()' returns a list of the labels from the rows of the current
ViewModel instance.

'update_()' is called automatically at end of a 'with <ViewModel instance>'
statement (python keyword 'with'), or can be called directly, to update the
actual database with values
changed by assignments through  '<ViewModel Instance>.<fieldname> = statements.

'viewName\_' is simply a title for the view for display purposes.

'models\_' is a list of the names of tables, or actual database tables objects
used by the view

'dbModels\_' is a dictionary of database table objects used by the view, with
the model names as keys.

Note: all 'ViewModel' instances with one row implements all of the ViewRow
interface in addition to the methods and properties discussed. 'ViewModel'
instances with more than one row will raise errors if the 'ViewRow' interface
as it is ambiguous which row/document to use.

'ViewRow': The Row Interface
+++++++++++++++++++++++++++++
ViewRow objects and ViewModel objects both implement the 'ViewRow' interface.

Where a ViewModel contains one logical row, the operations can be performed
on the ViewModel, which also supports this interface for single row instances.

ViewRow Interface methods
~~~~~~~~~~~~~~~~~~~~~~~~~
- <iterate>:  for field in <ViewRow instance>
- loop_(case=<case>): for field in a <ViewRow instance>
- <index>:  <ViewRow instance>[<field name>]
- <attribute> <ViewRow instance>.field_name

ViewRow Interface Properites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- fields\_
- view\_
- label\_
- idx\_

ViewRow details
~~~~~~~~~~~~~~~~
'for <field> in <ViewRow instance>:' provides for using a 'for loop' to iterate
over the fields in a row of a viewfield.

Note that this iteration can be for building a view, and as such the iteration
allows for selecting which fields are included in the view.
When fields are declared
(see `'ViewField' interface`_), they can set a 'case' where they are applicable
for views.
For example, this can be in a view, on an edit panel, or the field is for
calcuation purposes and part of the model, but not revealed in a view.

<ViewRow instance>[<field name>] or indexing, retrieves the instance of the
ViewField named.  For example::

    student['name'].value = 'Jane'
    print(student['jane'].value)


'fields\_' returns
A 'ViewRow' is a logical entry in a ViewModel.  Consider the example
( 'Simple example'_. ). The line of code::

    student.name = 'Fred'

Is using the ViewRow setattribute interface to set the 'value' of the 'name'
field within the 'row' created by the insert_() method.

In this example, because the 'student' ViewModel has only one row, then.

This inteface allows retrieving and setting data 'fields' or ViewField entries
by name as object attributes.  All internal attributes of ViewRow have either
a trailing underscore to avoid name collisions with field names of the database,
or a leading undersore to indicate that these attributes should not be accessed
externally of the ViewRow or ViewModel.

Provided database fields have no leading or trailing underscore, they will not
collide with the names of internal workings of these classes.

'ViewField' interface
++++++++++++++++++++++

Getting and Setting 'Row Member' values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To be added


Building HTML Forms
+++++++++++++++++++

To be added


Updating from HTML forms
++++++++++++++++++++++++

To be added

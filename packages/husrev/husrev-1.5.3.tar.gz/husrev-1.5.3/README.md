This tool has been forked from at [GitHub](https://github.com/agronholm/sqlacodegen)
Python 3 and the latest SQLAlchemy version).  
  
This is a tool that reads the structure of an existing database and generates  
the appropriate SQLAlchemy model classes, using the declarative style if  
possible.  
  
  
Features  
========  
  
* Supports SQLAlchemy  
* Produces declarative code that almost looks like it was hand written  
* Produces [PEP 8](http://www.python.org/dev/peps/pep-0008) compliant code  
* Accurately determines relationships, including many-to-many, one-to-one  
* Automatically detects joined table inheritance  
* Excellent test coverage  
* It creates each SQLAlchemy class file separately under the ``"models"`` folder.  
  
  
Usage instructions  
==================  
  
Installation  
------------  
  
To install, do:
  
 

> pip install husrev

or, failing that:
  

>  easy_install husrev

  
Example usage  
-------------  
  
At the minimum, you have to give husrev a database URL.  
The URL is passed directly to SQLAlchemy's  
`create_engine() method so please refer to` SQLAlchemy's documentation <http://docs.sqlalchemy.org/en/latest/core/engines.html>
for instructions on how to construct a proper URL.  
  
Examples:
  
 >husrev postgresql:///some_local_db --noinflect

 >husrev mysql+oursql://user:password@localhost/dbname

 >husrev sqlite:///database.db  

To see the full list of options:
 >husrev --help

  
Model class naming logic  
------------------------  
  
The table name (which is assumed to be in English) is converted to singular  
form using the "inflect" library. Then, every underscore is removed while  
transforming the next letter to upper case. For example, ``sales_invoices``  
becomes ``SalesInvoice``.  

Use ``--noinflect`` disable inflect transform.
  
Relationship detection logic  
----------------------------  
  
Relationships are detected based on existing foreign key constraints as  
follows:  
  
* **many-to-one**: a foreign key constraint exists on the table  
* **one-to-one**: same as **many-to-one**, but a unique constraint exists on  
  the column(s) involved  
* **many-to-many**: an association table is found to exist between two tables  
  
A table is considered an association table if it satisfies all of the  
following conditions:  
  
#. has exactly two foreign key constraints  
#. all its columns are involved in said constraints  
  
  
Relationship naming logic  
-------------------------  
  
Relationships are typically named based on the opposite class name.  
For example, if an ``Employee`` class has a column named ``employer`` which  
has a foreign key to ``Company.id``, the relationship is named ``company``.  
  
A special case for single column many-to-one and one-to-one relationships,  
however, is if the column is named like ``employer_id``. Then the  
relationship is named ``employer`` due to that ``_id`` suffix.  
  
If more than one relationship would be created with the same name, the  
latter ones are appended numeric suffixes, starting from 1.  
  
  
Source code  
===========  
  
The source can be browsed at [GitHub](https://github.com/MMustafa53/husrev)
  
Reporting bugs  
==============  
  
A [bug tracker](https://github.com/MMustafa53/husrev/issues)
is provided by GitHub.
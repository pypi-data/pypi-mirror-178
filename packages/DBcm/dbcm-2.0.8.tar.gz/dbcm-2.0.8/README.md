
The DBcm.UseDatabase context manager for working with MariaDB and SQLite3.

The 1.x release of this module was based on code created for the second edition 
of Head First Python. See chapters 7, 8, 9, and 11 of the that book for information
on how this module was created.  Note: Release 1 targets MySQL server. To install the
Second Edition release, please use: pip install DBcm=1.7.4

For the third edition of Head First Python, DBcm moved to release 2 and now targets
MariaDB as its primary back-end database (although it should/might still work with a MySQL
server if that's what you're running).

The option to use SQLite3 is also supported in this new release.

Simple example usage (for a MariaDB backend):

    from DBcm import UseDatabase, SQLError

    config = { 'host': '127.0.0.1',
               'user': 'myUserid',
               'password': 'myPassword',
               'database': 'myDB' }

    with UseDatabase(config) as cursor:
        try:
            _SQL = "select * from log"
            cursor.execute(_SQL)
            data = cursor.fetchall()
        except SQLError as err:
            print('Your query caused an issue:', str(err))

If a filename (string) is used in place of a config dictionary when using 
DBcm.UseDataBase, the data is assumed to reside in a local SQLite file (which
gets created if it doesn't previously exist).

Note: It is assumed you have a working version of the MariaDB server installed
on the computer onto which you're installing release 2 of DBcm.  (If not, you'll 
likely get build errors due to the absence of the MariaDB client-side C tools).  

Note: the popular PythonAnywhere hosting service provides a MySQL backend, which
can't be used with release 2 of DBcm. Install release 1.7.4 instead (see above).


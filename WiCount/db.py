'''
Created on 29 Jun 2016

@author: Velda Conaty
need this module to carry the connection to the db across all modules. Got help from this post.
http://stackoverflow.com/questions/6829675/the-proper-method-for-making-a-db-connection-available-across-many-python-module
'''
import sqlite3 as lite
_connection = None

def get_connection():
    global _connection
    if not _connection:
        _connection = lite.connect('wicount.sqlite3')
        
    return _connection

# List of stuff accessible to importers of this module. Just in case
__all__ = [ 'getConnection' ]
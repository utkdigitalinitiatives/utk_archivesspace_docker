============================
UTK ArchivesSpace Docker Dev
============================

-----
About
-----

A development environment for UTK's ArchivesSpace instance:

- Installs our local plugin
- Adds a few our our EADs for testing
- Configures application based on a config file similar to the one in production


**Note**: This is intended for testing purposes only.


----------
How to use
----------


.. code-block:: console

    $ docker-compose up --build -d

----------
Interfaces
----------

`Public Interface <http://0.0.0.0:8081/>`_

`Staff Interface <http://0.0.0.0:8080/>`_

`Solr <http://0.0.0.0:8090/>`_

`REST API <http://0.0.0.0:8089/>`_

-------------
Default Login
-------------

username: admin
password: admin

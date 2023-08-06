=================
testrail-lib
=================

This is a Python wrapper of the test rail api according to 
`the official document <http://docs.gurock.com/testrail-api2/start>`_

-----------------
Install
-----------------
You can install it from Pypi

::

    pip install testrail-lib

-----------------    
Document
-----------------

The API is wraped to be as easy as possible, you can read the example code to know how to use.

To know the fields and parameters supported, you need to read the official document of test rail. 

`The official document is here <http://docs.gurock.com/testrail-api2/start>`_

-----------------
Example
-----------------
::

    from testrail_client import TestRailClient

    if __name__ == '__main__':
        # host may not needed to start with 'http://'
        client = TestRailClient('host', 'tester@example.com', 'password')
        client.user.all()
        client.case.add(1613, title='lalala, are you happy?')
        client.case.for_project(53, 251, 1171)
        
        # an example using filter
        client.plan.for_project(53, is_completed=1)
        
        # an example using filter with params in list
        # 164
        print len(client.test.for_run(8155, status_id=1))
        # 28
        print len(client.test.for_run(8155, status_id=5))
        # 164 + 28 = 192
        print len(client.test.for_run(8155, status_id=[1, 5]))

-----------------
Version
-----------------

* Version 0.0.1:    Implementation of basic all APIs

* Version 0.0.4:    All APIs test passed

* Version 0.0.5:    Filter function added to get requests

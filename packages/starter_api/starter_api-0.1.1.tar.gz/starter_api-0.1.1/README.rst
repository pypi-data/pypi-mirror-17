=========================
Starter Server API Client
=========================


Install
=======
pip install starter_api


Usage
=====
.. code-block:: python

    import starter_api

    starter_api.init("http://HOST:PORT")

    # simple build and submit task to server
    res = starter_api.build_submit("YOUR_SERVICE", {"myparam": 1})
    print('res = ' + str(res))

    # build task object into variable and submit to server
    task = starter_api.build_task("YOUR_SERVICE", {"myparam": 1})
    res = starter_api.submit(task)
    print('res = ' + str(res))


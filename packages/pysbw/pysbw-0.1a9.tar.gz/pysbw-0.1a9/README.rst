pysbw
=====

Python 3 implementation of the
`Stopbadware <https://www.stopbadware.org/>`
`Private API <https://stopbadware.atlassian.net/wiki/display/apidocs/StopBadware+API+Documentation+Home>`.
In its current form it only implements downloading of events from a specific timestamps, IP addresses and searching based
on timestamps.

How To Use
----------

::

    import pysbw
    import time

    api = pysbw.API('~/.stopbadware.key')

    # Retrieve event reports for past 24 hours using UNIX style timestamp
    json_response = api.retrieve(int(time.time()) - 24 * 3600)

    # Retrieve event report with report UID
    json_response = api.retrieve("564f2c78e4b0a131f050f844")
                      
    # Retrieve event reports for past 24 hours using search functionality
    end = int(time.time())
    json_response = self.api.search_between(end - 24 * 3600, end)

Installiation
-------------

::

    pip3 install pysbw --pre

Example Key File
----------------

::

    [sbw]
    apikey=<String of private key>
    publickey=<String of public key>

Instantiation
-------------

::

    api = pysbw.API('~/.virustotal.key')  # The default way of using the 
    api = pysbw.API('', private_api_key=<PRIVATE API KEY>, public_api_key=<PUBLIC API KEY>)  # Providing other parameters
    api = pysbw.API( ... , max_retires=<N: Number>)  # If specified the API will only retry <N> times to get the response
    api = pysbw.API( ... , rate_limit={"requests": 40, "seconds": 300})  # The rate limits for the number of queries to the API


API
---

Use the method ***retrieve()*** to get Reports. This method's first
argument can be:

-  a UNIX style timestamp in UTC to retrieve reports since that
   timestamp
-  an IP address in DOT notation such as '8.8.8.8' to retrieve all
   reports relating to IP address
-  an event report UID which is a 24 digit hex number.

retrieve() will attempt to auto-detect what you're giving it. If you
want to be explicit, you can use the thing\_type parameter with the
values:

-  ip
-  timestamp
-  uid

These values are provided as constants that you can use instead in the
'API\_Constans' class which you can import as follows

::

    from pysbw import API_Constansts

Use the method ***search\_between()*** to search for events between two
timestamp values.

References
----------
`SBW API Documentation <https://stopbadware.atlassian.net/wiki/display/apidocs/StopBadware+API+Documentation+Home>`.

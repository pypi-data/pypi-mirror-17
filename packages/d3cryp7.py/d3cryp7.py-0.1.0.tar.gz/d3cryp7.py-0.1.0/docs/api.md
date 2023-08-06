API
===

RESTful API

Documentation on how to use the RESTful API provided by the application

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Examples
--------

### Curl

	$ curl http://127.0.0.1:80/api/statistics

### Python Requests

	import requests

	requests.get('http://127.0.0.1:80/api/statistics').json()

The result of these examples is as follows:

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Version
-------

### GET

Returns the version of the application

	{
	  "version": "0.1.0"
	}

/api/version

Statistics
----------

### GET

Returns statistics about the application and the Python interpreter

	{
	  "python": {
	    "platform": "linux",
	    "version": "3.5.2"
	  },
	  "d3cryp7": {
	    "status_code": 0,
	    "version": "0.1.0",
	    "status": "RUNNING"
	  },
	  "time": {
	    "running": 289,
	    "start": 1475188829,
	    "current": 1475189118
	  }
	}

/api/statistics

API
===

RESTful API

Documentation on how to use the RESTful API provided by the application

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Examples
--------

### Curl

	$ curl http://127.0.0.1:80/api/statistics
	$ curl http://127.0.0.1:80/api/recognize -F "image=<base64 encoded image>" -X POST

### Python Requests

	import requests

	requests.get('http://127.0.0.1:80/api/statistics').json()
	requests.post('http://127.0.0.1:80/api/recognize', data = {'image': '<base64 encoded image>'}).json()

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

Recognize
---------

### POST

Uses optical character recognition to extract text from an image

**Args:**

| Name  |      Description       |
|-------|------------------------|
| image | A base64 encoded image |

	{
	  "result": "The quick brown fox jumps over the lazy dog."
	}

/api/recognize

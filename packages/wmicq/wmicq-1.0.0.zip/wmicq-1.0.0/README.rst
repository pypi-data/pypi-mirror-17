==============
wmicq 1.0.0
==============

The **wmicq** module is a simple wrapper for wmic Windows command allowing to query Windows Management Instrumentation (WMI).

.. contents::
   :depth: 1
   
Dependencies
------------

	- Module `enum34 <https://pypi.python.org/pypi/enum34>`_ 
	  for installations targeted to Python version below 3.4,
	  
	- There are no dependencies for installations targeted to Python 3.4 and above.
	
	  
Downloading and installation
----------------------------

The recommended way of the module downloading and installation is to use pip:

.. code-block:: bash
	
	$ pip install wmicq
	
		   
Sample usage
------------

Below you can find sample usage of the module:

.. code-block:: python

	import sys
	import wmicq

	try:
		attributes = ['Description', 'IPAddress', 'MACAddress']
		header, queryData = wmicq.query(wmicq.Category.NICCONFIG, attributes = attributes, where = "IpEnabled=True")
		maxLen = max(len(x) for x in header)

		for q in queryData:
			print("{}: MAC: {}, IP: {}".format(q["Description"], q["MACAddress"], q["IPAddress"]))
			
		sys.exit(0)
		
	except wmicq.QueryError as e:
		print("Query error: {}".format(e))
		sys.exit(1)
		
License
-------
The wmicq module may be downloaded, installed, run and used in accordance with
the terms of the MIT license:

	**Copyright (c) 2016 BaseIT**

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
	OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
	DEALINGS IN THE SOFTWARE.

	
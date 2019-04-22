QuickStart
==========
pip install . # only installs "required"
pip install .[test] # installs dependencies for tests
pip install .[windows] # installs dependencies for Windows

====

From the directory with setup.py

python setup.py test #run all tests

pytest


Scrapy
=======

scrapy shell

: fetch("http://quotes.toscrape.com/")
: response.xpath('//h1/a/text()').extract()  #extract_first()
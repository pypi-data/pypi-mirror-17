0.6.0 (2016-09-09)
------------------

* Propagate gunicorn.error log, and remove its default handler.

This allows consistant logging, making the choice in all cases that your
gunicorn logs go to the same stream as your other application loglogging,
making the choice in all cases that your gunicorn logs go to the same stream as
your other application logs.

We issue a warning if the user tries to configure errorlog manually, as it
won't work as expected.

0.5.7 (2016-09-02)
------------------

* Update publishing workflow
* Add make changelog target

0.5.6 (2016-09-02)
------------------

* more testing release process in prepartion for 0.6

0.5.5 (2016-09-02)
------------------

* testing release process in prepartion for 0.6

0.5.4 (2016-08-10)
------------------

* series of point release to fix various small bugs

0.5.0 (2016-08-10)
------------------

* add grok filters for logstash
* slight adjustment to logfmt serialisation: talisker now strips " from tag
  values. This is due to a limitation in logstash.

0.4.1 (2016-08-05)
------------------

* publish separate py2/py3 wheels, due to dependency differences
* some doc changes

0.4.0 (2016-08-05)
------------------

* First public release an PyPI.

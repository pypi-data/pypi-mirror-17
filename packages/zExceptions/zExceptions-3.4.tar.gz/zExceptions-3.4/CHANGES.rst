Changelog
=========

3.4 (20160-09-08)
----------------

- Use `HTTPException.body_template` when title and detail are set.

- Add new title and detail attributes to HTTPException.

3.3 (2016-08-06)
----------------

- Add exception classes for all HTTP status codes.

3.2 (2016-07-22)
----------------

- Implement basic subset of Response features in HTTPException class.

3.1 (2016-07-22)
----------------

- Mark exceptions with appropriate zope.publisher interfaces.

- Add a new common base class `zExceptions.HTTPException` to all exceptions.

3.0 (2016-04-03)
----------------

- Add compatibility with PyPy and Python 3.

- Arguments to the Unauthorized exception are assumed to be utf8-encoded
  if they are bytes.

2.13.0 (2010-06-05)
-------------------

- Released as separate package.

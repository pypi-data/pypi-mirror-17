.. :changelog:

Release History
===============

`1.0.7`_ (14 Sep 2016)
----------------------
- Have a default content length for responses without one

`1.0.6`_ (14 Sep 2016)
----------------------
- Move to millisecond precision

`1.0.5`_ (14 Sep 2016)
----------------------
- Remove ``content_type`` tag

`1.0.4`_ (14 Sep 2016)
----------------------
- Rework how the line protocol is marshalled and support the various data types.
- Remove the accept tag
- Strip down content_type to the ``type/subtype`` format only
- Make ``correlation_id`` a field value and not tag
- Change the precision to second precision, per the InfluxDB docs (use the most
    coarse precision for better compression)


`1.0.3`_ (13 Sep 2016)
----------------------
- Add a response ``content_length`` field, an ``accept`` tag (if set in request
    headers), and a response ``content_type`` tag.

`1.0.2`_ (13 Sep 2016)
----------------------
- Don't use RequestHandler.reverse_url to get the endpoint pattern in the mixin

`1.0.1`_ (13 Sep 2016)
----------------------
- Fixes an issue with the periodic callback

`1.0.0`_ (13 Sep 2016)
----------------------
- Initial release

.. _1.0.7: https://github.com/sprockets/sprockets-influxdb/compare/1.0.6...1.0.7
.. _1.0.6: https://github.com/sprockets/sprockets-influxdb/compare/1.0.5...1.0.6
.. _1.0.5: https://github.com/sprockets/sprockets-influxdb/compare/1.0.4...1.0.5
.. _1.0.4: https://github.com/sprockets/sprockets-influxdb/compare/1.0.3...1.0.4
.. _1.0.3: https://github.com/sprockets/sprockets-influxdb/compare/1.0.2...1.0.3
.. _1.0.2: https://github.com/sprockets/sprockets-influxdb/compare/1.0.1...1.0.2
.. _1.0.1: https://github.com/sprockets/sprockets-influxdb/compare/1.0.0...1.0.1
.. _1.0.0: https://github.com/sprockets/sprockets-influxdb/compare/0.0.0...1.0.0
.. _Next Release: https://github.com/sprockets/sprockets-influxdb/compare/1.0.7...master

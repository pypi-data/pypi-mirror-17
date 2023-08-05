check_s3_bucket
###############

Check that a filename matching the regex was added to the bucket in the given time window.

Usage
-----

.. code:: shell

    $ check_s3_bucket --help
    usage: check_s3_bucket [-h]
                           bucket [regex] [warning_threshold] [critical_threshold]

    Check that a filename matching the regex was added to the bucket in the given
    time window.

    positional arguments:
      bucket              S3 bucket to check
      regex               Filename regex to check (defaults to *)
      warning_threshold   Warning threshold in hours (defaults to 25)
      critical_threshold  Critical threshold in hours (defaults to 49)

    optional arguments:
      -h, --help          show this help message and exit

License
-------

This software is licensed under the MIT license (see the :code:`LICENSE.txt`
file).

Author
------

Nimrod Adar, `contact me <nimrod@shore.co.il>`_ or visit my `website
<https://www.shore.co.il/>`_. Patches are welcome via `git send-email
<http://git-scm.com/book/en/v2/Git-Commands-Email>`_. The repository is located
at: https://www.shore.co.il/git/.



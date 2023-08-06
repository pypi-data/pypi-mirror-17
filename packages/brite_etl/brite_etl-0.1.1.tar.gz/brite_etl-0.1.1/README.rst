========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - |version| |status| |supported-versions|

.. |docs| image:: https://readthedocs.org/projects/brite_etl/badge/?style=flat
    :target: https://brite-etl.readthedocs.io/en/latest/readme.html
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/haydenbbickerton/brite_etl.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/haydenbbickerton/brite_etl

.. |codecov| image:: https://codecov.io/github/haydenbbickerton/brite_etl/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/haydenbbickerton/brite_etl

.. |version| image:: https://img.shields.io/pypi/v/brite_etl.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/brite_etl

.. |status| image:: https://img.shields.io/pypi/status/brite_etl.svg?style=flat
    :alt: PyPI Package status
    :target: https://pypi.python.org/pypi/brite_etl

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/brite_etl.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/brite_etl


.. end-badges

A python package for working with the BriteCore ETL.

**PLEASE NOTE:** ``brite_etl`` follows `Semantic Versioning <http://semver.org/>`_, and is currently in the initial development phase (``0.x.x``). Use with caution.

Use
===========

This is all broken down on the introduction page.

.. code:: python

    import brite_etl
    from brite_etl.core.io.frame_sources import CsvSource

    # Create a "set" of frames to work with...
    contoso = brite_etl.lib.FrameSet('contoso')

    #Set the source of our csvs (can also pass BriteDataFrame/PreparedDataFrame)...
    contoso.set_data_sources(source=CsvSource(DF_ROOT), prepared_source=CsvSource(DF_PREP))

    # Easy handling of dataframes, works same for both csv and britedataframe sources.
    # Essentially a wrapper around the pandas DataFrame. Dates parsed automatically.
    contoso.frames.get('property_items')
    contoso.frames.get('agencies').df # original dataframe

    # Import BriteCore reports. Don't have to open/change/save columns in excel, hyperlinks and other
    # formatting issues are handled. Don't even have to rename the file to take out the dates.
    from brite_etl.core.io import import_report
    adv_prem = import_report('/tmp/input', 'Advance Premium', sheet='Advance Premium List', skip_rows=2) # Pandas DataFrame
    contoso.frames.set('ap', df=adv_prem) # Make custom frames in your frame set

    # Define frame-specific operations...
    contoso.frames.get('prepared.lines').endOfMonthSum()

    # Or use universal operations, chain across multiple frames...
    _contoso = contoso.chain
    (_contoso
        .filter_dates('date filter for multiple frames actually isn\'t done yet (soon, though)')
        .hash_cols(['policyId']) # MD5 hashed dataframes
        .export_excel(
            path='/tmp/output',
            file_name='end_month_integrity_hash.xlsx'
        ) # Every frame is put into it's own sheet during export
        .run()
    )

    # Computations make use of multiple frames within a frame set (also chainable)...
    trans = _contoso.get_item_transactions().value()

    # Create multiple, isolated sets of frames...
    wrk = brite_etl.lib.FrameSet('working', from_set=contoso)

Installation
============

::

    pip install brite_etl

Development
===========

To run the all tests run::

    tox

Test just your desired python version with ``tox -e py27`` or ``tox -e py35``. Much faster than running all test envirornments.

Note about testing: some of the tests require real df_cache data to run. The locations for the df_cache directories is defined in the ``setup.cfg`` file. When running, the tests will check to make sure the directories exist and contain files. If they don't those tests will be skipped, the rest of the tests should function like normal.


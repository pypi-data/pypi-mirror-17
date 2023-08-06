..  _introduction:

============
Introduction
============

To use BriteETL in a project:

.. code:: python

    import brite_etl

FrameSet
--------

For an overview on Frames & FrameSets, please see :ref:`frames_and_framesets`.

To start we'll create a FrameSet and set our frame data source.

.. code:: python

    from brite_etl.core.io.frame_sources import CsvSource

    # Create a frameset to work with...
    cfm = brite_etl.lib.FrameSet('cfm')

    #Set the source of our csvs (can also pass BriteDataFrameSource)...
    cfm.set_data_sources(source=CsvSource('/tmp/df_cache_root'), prepared_source=CsvSource('/tmp/df_prep_cache_root'))

Now that have our frameset ready, we can start using it! This call will return :class:`PropertyItems <brite_etl.frames.property_items.PropertyItems>`, populated with the data from the CSV source that we did above.

.. code:: python

    pi = cfm.frames.get('property_items')
    pi.df # This is the actual pandas.DataFrame

Frame Operations
----------------

Functions that are frame-specific can be called directly, because they should be defined in the Frames class itself.

.. code:: python

    cfm.frames.get('prepared.claims').function_that_only_applies_to_prepared_claims_and_nothing_else()


Operations (Not frame-specific)
-------------------------------

Universal functions that are not frame-specific, but are still only used on one frame at a time can be called like this.

`Note that in this example, I'm getting the revisions dataframe from the brite_etl.FrameSet, but you can also manually read the csv and pass that if you'd prefer (see bottom of page for example).`

.. code:: python

    from brite_etl.core.operations import hash_cols
    revs = cfm.frames.get('revisions').df

    result = hash_cols(revs, cols=['policyId', 'revisionId'])

You can also get the frame chain, which will chain the `frame.df` for you along multiple functions, without having to import them.

.. code:: python

    _rev = cfm.frames.get('revisions').chain

    result = _rev.hash_cols(cols=['policyId', 'revisionId']).another_universal_function().value()

Computations
------------

Computations are basically mini-reports. They take multiple frames, do some stuff to them, then return a pandas DataFrame.

To call directly:

.. code:: python

    from brite_etl.core.computations import get_item_transactions

    _frames = {
        'revisions': cfm.frames.get('revisions'),
        'property_items': cfm.frames.get('property_items'),
        'revision_items': cfm.frames.get('revision_items'),
        'prepared': {
            'accounting': cfm.frames.get('prepared')
        }
    }

    item_trans = get_item_transactions(_frames)


Or, be cool and chain the whole frameset. The frames needed will be fetched and resolved automatically. Don't even have to import the function you're calling:

.. code:: python

    _cfm = cfm.chain
    item_trans = _cfm.get_item_transactions().value()


Quick Note About Frame Sets
---------------------------

Every frame stored within a `specific` frameset is a singleton.

.. code:: python

    _cfm = cfm.chain
    item_trans1 = _cfm.get_item_transactions().value()

    rev = cfm.frames.get('revisions')

    # Do a bunch of stuf to rev...

    item_trans2 = _cfm.get_item_transactions().value()

    item_trans1 == item_trans2 # False!!!

This is done to ensure the frames inside of a frameset are exactly what you want them to be.

If you want to get a fresh copy of the frame, with data straight from the csv:

.. code:: python

    new_rev = cfm.frames.get('revisions', fresh=True)

You also don't have to use a frameset if you don't want to:

.. code:: python

    # inside a jupyter report...
    from reports.utils import BriteDataFrame
    from brite_etl.frames import Policies

    bdf = BriteDataFrame()
    df = bdf.get_dataframe('policies')

    policies = Policies(policies_df)

    _policies = polices.chain # Can still chain universal operations, without having to import brite_etl as a whole

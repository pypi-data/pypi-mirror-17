..  _frames_and_framesets:

===================
Frames & Frame Sets
===================

This is a quick overview of Frame & Frame Sets, the structures used by ``brite_etl`` to help organize data and logic.

Frames
======

In brite_etl, Frames are classes that wrap the BriteCore dataframes (the csv's you get when you run `bin/get_df_cache.py <https://github.com/IntuitiveWebSolutions/BriteCore/blob/master/bin/get_df_cache.py>`_). The dataframe is stored in the Frame class and can be accessed through the :attr:`df <brite_etl.abstracts.Frame.df>` property.

This layer of abstraction give us a nice place to put frame-specific operations, and helps when working with Frame Sets.

Each Frame class uses the :class:`brite_etl.abstracts.Frame` metaclass to ensure consistency, merge Frame configs with the default config, and reduce the amount of duplicate code.

This is how a Frame looks on imaginary paper:

.. code::

    +-----------------------------------------------+
    |              Revisions                        |
    |                                               |
    | +------------+   +--------------------------+ |
    | |    df      |   |       config             | |
    | |            |   | {                        | |
    | | The Pandas |   |  name:        revisions, | |
    | | DataFrame  |   |  display_name: Revisions,| |
    | |            |   |  prepared:     False     | |
    | +------------+   |  ...                     | |
    |                  | }                        | |
    |                  +--------------------------+ |
    |-----------------------------------------------|
    |                                               |
    | +------------------+ +---------------------+  |
    | | custom_revisions_| | revisions_specific_ |  |
    | | function_one()   | | function_blabla()   |  |
    | |                  | |                     |  |
    | +------------------+ +---------------------+  |
    |                                               |
    +-----------------------------------------------+


Frame Sets
==========

Frame Sets have 3 goals:
    1. Store our Frames in a dictionary for easy access and reuse
    2. Use data sources to build Frame classes for painless dataframe parsing
    3. Allow us to use multiple, isolated instances of Frames and their data



1 - Frame Dictionary
--------------------

All frames in a FrameSet are stored inside of a nested dictionary. Regular frames are at the root, prepared frames are nested under the ``prepared: {}`` object. The objects stored are the actual Frame **classes**, not the direct dataframes themselves. The dataframes are stored inside the Frame classes as mentioned in the above section.

When you call ``my_set.frames.get('lines')``, it checks to see if that Frame already exists in the dictionary. If it does, the frame is returned as-is. If it doesn't exist, the frame is built using the corrosponding frame class, and the dataframe retrieved by using the data_sources.

Here is a diagram of the Frame Dictionary

.. code::

    +--------------------------------------------------------------+
    |                       _FrameDict                             |
    |                                                              |
    |                        .get()                                |
    |                          +                                   |
    |                          |                                   |
    |                          v                                   |
    |                    Have we already fetched                   |
    |                    the Frame and stored it?                  |
    |                             +                                |
    |                             |                                |
    |                             |                                |
    |  return frame <---+ yes  <--+--> no +---> +--------------+   |
    |       ^                                   | Build Frame  |   |    This step is
    |       |                                   | Class    +----------+ explained below
    |       +-----------+ store frame <-------+ |              |   |    in part 2
    |                                           +--------------+   |
    +--------------------------------------------------------------+




2 - Building Frames with data sources
-------------------------------------

Look at this code, taken from the introduction page:

.. code:: python

    from brite_etl.io.frame_sources import CsvSource

    contoso = brite_etl.lib.FrameSet('contoso')

    contoso.set_data_sources(
        source=CsvSource('/tmp/df_cache_root'),
        prepared_source=CsvSource('/tmp/df_prep_cache_root')
    )


On the ``contoso.set_data_sources`` bit, we are setting the sources that will be used when our frame dictionary has not found a frame, and attempts to build one.

In this case, the :class:`CsvSource <brite_etl.core.io.frame_sources.CsvSource>` will read the csv file in the ``/tmp/df_cache_root`` directory, pass the result to :class:`FrameBuilder <brite_etl.lib.FrameBuilder>`, which will find the corrosponding Frame class and create it using the csv data.

So the ``Build Frame Class`` step in the diagram above looks like this:

.. code::

    +----------------------------------------------------------------------------------+
    |                               Building Frame Class                               |
    |                                                                                  |
    | +----------------------------------+           +-------------------------------+ |
    | |            CsvSource             |           |        FrameBuilder           | |
    | |                                  |           |                               | |
    | | _df = pandas.read_csv(           |           | import brite_etl.frames.Lines | |
    | |   '/tmp/df_cache_root/lines.csv' |           | _frame = Lines(_df)           | |
    | | )                                | +-------> | return _frame                 | |
    | | return _df                       |           |                               | |
    | |                                  |           +--------+----------------------+ |
    | +----------------------------------+                    |                        |
    |                                                         |                        |
    |                                                         |                        |
    |                                                         v                        |
 <---------------------------------------------------+ return to _FrameDict            |
    |                                                                                  |
    +----------------------------------------------------------------------------------+


3 - Multiple Isolated Frame Sets
--------------------------------

The third goal (and inital reason for creating the ``brite_etl`` package) is to allow users to juggle multiple frame sets and their data simultaneously. You can use the same data_source, or different data_sources.

Let's assume that we doing data integrity testing on the (fake) BriteCore client, Contoso. You want to check the accounting records for August 2015 and make sure they haven't changed in some way over time.

You run the following commands from your BriteCore checkout to download the df_cache:

.. code:: python

    bin/get_df_cache.py -p contoso --date 2015-09-01 /tmp/df_cache_1
    bin/get_df_cache.py -p contoso --date 2016-09-01 /tmp/df_cache_2

You now have 2 df_cache folders, each on september in both 2015 and 2016. Each should contain the full accounting records for August 2015, and it shouldn't have changed.

You write this code in a Jupyter report:

.. code:: python

    from brite_etl.lib import FrameSet
    from brite_etl.io.frame_sources import CsvSource

    con1 = FrameSet('con1')
    con.set_data_sources(prepared_source=CsvSource('/tmp/df_cache_1'))

    con2 = FrameSet('con2')
    con.set_data_sources(prepared_source=CsvSource('/tmp/df_cache_2'))


Because you've set different sources on them, any calls made to fetch frames from those sets will fetch the different csv's.

Now you go about checking the data:

*note: some of these functions don't exist yet, but you get the idea*

.. code:: python

    def _hash_aug_accounting(current_chain):
        result = (
            current_chain
            .filter_dates('limit to August 2015 plz and thank you') # TODO
            .hash_cols(['paymentId', 'changeInPaidPremium','endingAdvancedPremium'])
            .value()
        )
        return result

    # Get our frame chains ready, and hash the accounting frame
    _acc1 = con1.frames.get('prepared.accounting').chain
    acc1_hash = _hash_aug_accounting(_acc1)

    _acc2 = con2.frames.get('prepared.accounting').chain
    acc2_hash = _hash_aug_accounting(_acc2)


    # Check the MD5 hashed frames for differences
    from brite_etl.computations import compare_frames
    result = compare_frames([acc1_hash, acc2_hash])

And the result tells you that the August 2015 accounting records were changed sometime between 2015 and 2016.

This is something you could run on a cronjob to verify data integrity monthly, or manually run whenever needed.

------------

This is how a :class:`FrameSet <brite_etl.lib.FrameSet>` looks:

.. code::

    +-------------------------------------------------+
    |                  Frame Set                      |
    |                                                 |
    | +--------------+  +--------------------------+  |
    | | data sources |  |    frames (_FrameDict)   |  |
    | |              |  |                          |  |
    | | +----------+ |  |            +----------+  |  |
    | | |          | |  |  +-+  +-+  | prepared |  |  |
    | | | source   | |  |  +-+  +-+  |          |  |  |
    | | |          | |  |            | +--+ +-+ |  |  |
    | | +----------+ |  |  +-+  +-+  | +--+ +-+ |  |  |
    | |              |  |  +-+  +-+  |          |  |  |
    | | +----------+ |  |            | +--+ +-+ |  |  |
    | | |prepared  | |  |  +-+  +-+  | +--+ +-+ |  |  |
    | | |source    | |  |  +-+  +-+  |          |  |  |
    | | |          | |  |            +----------+  |  |
    | | +----------+ |  +--------------------------+  |
    | +--------------+                                |
    +-------------------------------------------------+

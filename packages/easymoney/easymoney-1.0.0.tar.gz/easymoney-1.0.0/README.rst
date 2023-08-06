EasyMoney
=========

|Build Status|

Overview
~~~~~~~~

Feature Summary:

-  Computing Inflation
-  Currency Conversion
-  Adjusting a given currency for Inflation
-  'Normalizing' a currency, i.e., adjust for inflation and then convert
   to a base currency.
-  Relating ISO Alpha2/3 Codes, Currency Codes and a region's Natural
   Name.

**NOTICE: THIS TOOL IS FOR INFORMATION PURPOSES ONLY.**

--------------

Dependencies
~~~~~~~~~~~~

EasyMoney requires: `numpy <http://www.numpy.org>`__,
`pandas <http://pandas.pydata.org>`__,
`requests <http://docs.python-requests.org/en/master/>`__ and
`wbdata <https://github.com/OliverSherouse/wbdata>`__\ †.

--------------

Installation
~~~~~~~~~~~~

``$ pip3 install easymoney``

*Note*: EasyMoney requires Python 3.4 or later.

--------------

Examples
~~~~~~~~

Import the tool
'''''''''''''''

.. code:: python

    from easymoney.money import EasyPeasy

Create an instance of the EasyPeasy Class
'''''''''''''''''''''''''''''''''''''''''

.. code:: python

    ep = EasyPeasy()

Prototypical Conversion Problems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currency Converter
''''''''''''''''''

.. code:: python

    ep.currency_converter(amount = 100, from_currency = "USD", to_currency = "EUR", pretty_print = True)

    # 88.75 EUR

Adjust for Inflation and Convert
''''''''''''''''''''''''''''''''

.. code:: python

    ep.normalize(amount = 100, currency = "USD", from_year = 2010, to_year = "latest", base_currency = "CAD", pretty_print = True)

    # 140.66 CAD

Convert Currency in a more Natural Way
''''''''''''''''''''''''''''''''''''''

.. code:: python

    ep.currency_converter(amount = 100, from_currency = "Canada", to_currency = "Ireland", pretty_print = True)

    # 68.58 EUR

Handling Common Currencies
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Currency Conversion:
'''''''''''''''''''''''

.. code:: python

    ep.currency_converter(amount = 100, from_currency = "France", to_currency = "Germany", pretty_print = True)

    # 100.00 EUR

EasyMoney understands that these two nations share a common currency.

2. Normalization
''''''''''''''''

.. code:: python

    ep.normalize(amount = 100, currency = "France", from_year = 2010, to_year = "latest", base_currency = "USD", pretty_print = True)

    # 118.98 USD

.. code:: python

    ep.normalize(amount = 100, currency = "Germany", from_year = 2010, to_year = "latest", base_currency = "USD", pretty_print = True)

    # 120.45 USD

EasyMoney also understands that, while these two nations may share a
common currency, inflation may differ.

Options
^^^^^^^

It's easy to explore the terminology understood by ``EasyPeasy``, as
well as the dates for which data is available, with ``options()``.

.. code:: python

    ep.options(info = 'all', pretty_print = True, overlap_only = True)

+--------+-------+------+------+-----------+-----------------+-----------------+------------+
| Region | Curre | Alph | Alph | Inflation | ExchangeRange   | Overlap         | Transition |
|        | ncy   | a2   | a3   | Range     |                 |                 | s          |
+========+=======+======+======+===========+=================+=================+============+
| Austra | AUD   | AU   | AUS  | [1960,    | [1999-01-04 :   | [1999-01-04 :   |            |
| lia    |       |      |      | 2015]     | 2016-09-12]     | 2015-12-31]     |            |
+--------+-------+------+------+-----------+-----------------+-----------------+------------+
| Austri | EUR   | AT   | AUT  | [1960,    | [1999-01-04 :   | [1999-01-04 :   | 1999 (ATS  |
| a      |       |      |      | 2015]     | 2016-09-12]     | 2015-12-31]     | to EUR)    |
+--------+-------+------+------+-----------+-----------------+-----------------+------------+
| Belgiu | EUR   | BE   | BEL  | [1960,    | [1999-01-04 :   | [1999-01-04 :   | 1999 (BEF  |
| m      |       |      |      | 2015]     | 2016-09-12]     | 2015-12-31]     | to EUR)    |
+--------+-------+------+------+-----------+-----------------+-----------------+------------+
| ...    | ...   | ...  | ...  | ...       | ...             | ...             | ...        |
+--------+-------+------+------+-----------+-----------------+-----------------+------------+

Above, the *InflationRange* and *ExchangeRange* columns provide the
range of dates for which inflation and exchange rate information is
available, respectively. The *Overlap* column shows the range of dates
shared by these two columns. Additionally, the dates of known
transitions from one currency to another are also provided.

Databases
^^^^^^^^^

The databases used by ``EasyPeasy()`` can be saved disk so they can be
used offline or modified. To do so, one can simply pass a directory when
creating an instance of the ``EasyPeasy()`` class.

.. code:: python

    ep = EasyPeasy('/path/of/your/choosing')

If this directory does not contain any of the required databases, it
will be populated with them. Conversely, if the the directory already
contains some of the required databases, ``EasyPeasy()`` will
automagically read in the existing databases and generate only those
databases that are missing.

--------------

Documentation
-------------

For complete documentation, including a more extensive version of this
document, please click
`here <https://tariqahassan.github.io/EasyMoney/index.html>`__.

--------------

License
-------

This software is provided under a BSD License.

--------------

Resources
---------

Indicators used:

1. `Consumer price index (2010 =
   100) <http://data.worldbank.org/indicator/FP.CPI.TOTL>`__

   -  Source: International Monetary Fund (IMF), International Financial
      Statistics.

      -  Notes:

         1. ALL INFLATION-RELATED RESULTS OBTAINED FROM EASYMONEY
            (INCLUDING, BUT NOT NECESSARILY LIMITED TO, INFLATION RATE
            AND NORMALIZATION) ARE THE RESULT OF CALCULATIONS BASED ON
            IMF DATA. THESE RESULTS ARE NOT A DIRECT REPORTING OF
            IMF-PROVIDED DATA.

2. `Euro foreign exchange reference rates - European Central
   Bank <https://www.ecb.europa.eu/stats/exchange/eurofxref/html/index.en.html>`__

   -  Source: European Central Bank (ECB).

      -  Notes:

         1. The ECB data used here can be obtained directly from the
            link provided above.
         2. Rates are updated by the ECB around 16:00 CET.
         3. The ECB states, clearly, that usage for transaction purposes
            is strongly discouraged. This sentiment is echoed here;
            ***as stated above, this tool is intended to be for
            information purposes only***.
         4. ALL EXCHANGE RATE-RELATED RESULTS OBTAINED FROM EASYMONEY
            (INCLUDING, BUT NOT NECESSARILY LIMITED TO, CURRENCY
            CONVERSION AND NORMALIZATION) ARE THE RESULT OF CALCULATIONS
            BASED ON ECB DATA. THESE RESULTS ARE NOT A DIRECT REPORTING
            OF ECB-PROVIDED DATA.

†Sherouse, Oliver (2014). Wbdata. Arlington, VA.

.. |Build Status| image:: https://travis-ci.org/TariqAHassan/EasyMoney.svg?branch=master
   :target: https://travis-ci.org/TariqAHassan/EasyMoney

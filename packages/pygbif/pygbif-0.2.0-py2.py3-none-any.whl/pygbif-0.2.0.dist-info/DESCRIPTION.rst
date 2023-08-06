pygbif
======

|pypi| |docs| |travis| |coverage|

Python client for the `GBIF API
<http://www.gbif.org/developer/summary>`_

`Source on GitHub at sckott/pygbif <https://github.com/sckott/pygbif>`_

Other GBIF clients:

* R: `rgbif`, `ropensci/rgbif <https://github.com/ropensci/rgbif>`_

Installation
============

Stable from pypi

.. code-block:: console

    pip install pygbif

Development version

.. code-block:: console

    [sudo] pip install git+git://github.com/sckott/pygbif.git#egg=pygbif

`pygbif` is split up into modules for each of the major groups of API methods.

* Registry - Datasets, Nodes, Installations, Networks, Organizations
* Species - Taxonomic names
* Occurrences - Occurrence data, including the download API

You can import the entire library, or each module individually as needed.

Note that `GBIF maps API <http://www.gbif.org/developer/maps>`_ is not included in `pygbif`.

Registry module
===============

registry module API:

* `organizations`
* `nodes`
* `networks`
* `installations`
* `datasets`
* `dataset_metrics`
* `dataset_suggest`
* `dataset_search`

Example usage:

.. code-block:: python

    from pygbif import registry
    registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')

Species module
==============

species module API:

* `name_backbone`
* `name_suggest`
* `name_usage`
* `name_lookup`
* `name_parser`

Example usage:

.. code-block:: python

    from pygbif import species
    species.name_suggest(q='Puma concolor')

Occurrences module
==================

registry module API:

* `search`
* `get`
* `get_verbatim`
* `get_fragment`
* `count`
* `count_basisofrecord`
* `count_year`
* `count_datasets`
* `count_countries`
* `count_schema`
* `count_publishingcountries`
* `download`
* `download_meta`
* `download_list`
* `download_get`

Example usage:

.. code-block:: python

    from pygbif import occurrences as occ
    occ.search(taxonKey = 3329049)
    occ.get(key = 252408386)
    occ.count(isGeoreferenced = True)
    occ.download('basisOfRecord = LITERATURE')
    occ.download('taxonKey = 3119195')
    occ.download('decimalLatitude > 50')
    occ.download_list(user = "sckott", limit = 5)
    occ.download_meta(key = "0000099-140929101555934")
    occ.download_get("0000066-140928181241064")


Contributors
============

* `Scott Chamberlain <https://github.com/sckott>`_
* `Robert Forkel <https://github.com/xrotwang>`_
* `Jan Legind <https://github.com/jlegind>`_
* `Stijn Van Hoey <https://github.com/stijnvanhoey>`_
* `Peter Desmet <https://github.com/peterdesmet>`_

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`_
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`_. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/pygbif.svg
   :target: https://pypi.python.org/pypi/pygbif

.. |docs| image:: https://readthedocs.org/projects/pygbif/badge/?version=latest
   :target: http://pygbif.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/pygbif.svg
   :target: https://travis-ci.org/sckott/pygbif

.. |coverage| image:: https://coveralls.io/repos/sckott/pygbif/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/pygbif?branch=master


Changelog
=========

0.2.0 (2016-10-18)
------------------
- Download methods much improved (#16) (#27) thanks @jlegind @stijnvanhoey @peterdesmet !
- MULTIPOLYGON now supported in `geometry` parameter (#35)
- Fixed docs for `occurrences.get`, and `occurrences.get_verbatim`, `occurrences.get_fragment` and demo that used occurrence keys that no longer exist in GBIF (#39)
- Added `organizations` method to `registry` module (#12)
- Added remainder of datasets methods: `registry.dataset_search` (including faceting support (#37)) and `registry.dataset_suggest`, for the `/dataset/search` and `/dataset/suggest` routes, respectively (#40)
- Added remainder of species methods: `species.name_lookup` (including faceting support (#38)) and `species.name_usage`, for the `/species/search` and `/species` routes, respectively (#18)
- Added more tests to cover new methods
- Changed `species.name_suggest` to give back data stucture as received from GBIF. We used to parse out the classification data, but for simplicity and speed, that is left up to the user now.
- `start` parameter in `species.name_suggest`, `occurrences.download_list`, `registry.organizations`, `registry.nodes`, `registry.networks`, and `registry.installations`, changed to `offset` to match GBIF API and match usage throughout remainder of `pygbif`

0.1.5.4 (2016-10-01)
--------------------
- Added many new `occurrence.search` parameters, including `repatriated`, `kingdomKey`, `phylumKey`, `classKey`, `orderKey`, `familyKey`, `genusKey`, `subgenusKey`, `establishmentMeans`, `facet`, `facetMincount`, `facetMultiselect`, and support for facet paging via	`**kwargs` (#30) (#34)
- Fixes to `**kwargs` in `occurrence.search` so that facet parameters can be parsed correctly and `requests` GET	request options are collected correctly (#36)
- Added `spellCheck` parameter to `occurrence.search` that goes along with the `q` parameter to optionally spell check full text searches (#31)

0.1.4 (2016-06-04)
------------------
- Added variable types throughout docs
- Changed default `limit` value to 300 for `occurrences.search` method
- `tox` now included, via @xrotwang (#20)
- Added more registry methods (#11)
- Started occurrence download methods (#16)
- Added more names methods (#18)
- All requests now send user-agent headers with `requests` and `pygbif` versions (#13)
- Bug fix for `occurrences.download_get` (#23)
- Fixed bad example for `occurrences.get` (#22)
- Fixed wheel to be universal for 2 and 3 (#10)
- Improved documentation a lot, autodoc methods now

0.1.1 (2015-11-03)
------------------
- Fixed distribution for pypi

0.1.0 (2015-11-02)
------------------
- First release



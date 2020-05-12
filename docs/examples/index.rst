Examples
========


Create a SDesk Client
---------------------
.. code-block:: python

    >>> from sdesk.api import SdeskClient
    >>>
    >>> client = SdeskClient("dev2.sciencedesk.net", disable_warning=True)
    >>> client.authenticate("thomas", "AsEDA112X*")


List Notebooks
--------------
.. code-block:: python

    >>> notebooks = client.list_notebooks()
    >>> len(notebooks)
    3
    >>> notebooks[0]
    <sdesk.api.resources.Notebook object at 0x7f9d3dedccf8>
    >>> notebooks[0].title
    'Thiagos Labbook for development'

Request Notebook by Id
----------------------
.. code-block:: python

    >>> notebook = client.get_notebook(16)
    >>> notebook
    <sdesk.api.resources.Notebook object at 0x7f9d3df0f0b8>
    >>> notebook.title
    'Stephans Labbook for Business'
    >>> notebook.id
    16

List Notebook's Entries
-----------------------
.. code-block:: python

    >>> entries = client.list_entries(notebook_id=16)
    >>> len(entries)
    2
    >>> entries[0]
    <sdesk.api.resources.Entry object at 0x7f9d3df0c978>
    >>> entries[0].title
    'medida do silicio'
    >>> entries[0].code
    1

List Files
----------
.. code-block:: python

    >>> files = client.list_files()
    >>> len(files)
    2
    >>> files[0]
    <sdesk.api.resources.File object at 0x7f9d3df0c898>
    >>> files[0].name
    'EXCELDATA.xlsx'


List Entry's Files
------------------
.. code-block:: python

    >>> files[0].owner
    <sdesk.api.resources.User object at 0x7f9d3defeb70>
    >>> files[0].owner.full_name
    'Albert Shulte'
    >>> files[0].name
    'EXCELDATA.xlsx'

Create a Notebook Entry
-----------------------
.. code-block:: python

    >>> entry = client.create_entry(
    ...     notebook_id=16,
    ...     description="This entry was created via automation script",
    ...     title="Logging Excel data file",
    ... )
    >>> entry.title
    'Logging Excel data file'
    >>> entry.id
    21
    >>> entry.code
    1

Upload File to a Notebook's Entry
---------------------------------
.. code-block:: python

    >>> file = client.upload_file(17, entry.code, 'NewFileData.xlsx')
    >>> file.id
    114
    >>> file.name
    'NewFileData.xlsx'
    >>> file.url
    '/api/notebooks/upldfiles/114/download/'


Get File Info
-------------
.. code-block:: python

    >>> file = client.get_file_info(file_id=114)
    >>> file.name
    'NewFileData.xlsx'
    >>> file.id
    114
    >>> file.url
    '/api/notebooks/upldfiles/114/download/'


References
==========

You may check :class:`sdesk.api.client.SdeskClient` for more details regarding the current methods.

For resource attributes you may refer to :mod:`sdesk.api.resources`

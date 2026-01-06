# ccl-archive
A simple set of utility tools for creating a local copy, for academic use, of the Computational Chemistry List mailing archive (https://server.ccl.net/cca/archived-messages/). These tools include downloading the original messages, creating a simple SQLite representation, and a trivial web frontend for local exploration.

## download.py
This will fetch messages from https://server.ccl.net/cca/archived-messages/ iterating over years, then months, then messages. A local CCL_Archive folder is created that mirrors the indexing of year, month, and which contains found messages.

## migrate.py
A simple utility routine that moves items from CCL_Archive with name {91, ..., 99} into {1991, ..., 1999}, and similarly from {00, ..., 25} into {2000, ...,2025}.

## database.py
Builds an SQLite databse (ccl_archive.db) from the data found in CCL_Archive

## app.py
Uses Flask to build a simple web frontend to the SQLite database that you can consume via your database of choice (default local access point: http://localhost:5001/)

HTML templates can be found in template

ccl-archive:
* ccl_archive.db            # Your SQLite DB
* app.py                    # The Flask backend
* templates/                # Folder for HTML
* templates/index.html      # Search & Browse page
* templates/message.html    # Full text display page

# prl_joai_admin

This script is used to programmatically administer scheduled harvests on jOAI, eliminating the need to use the web interface to add or remove harvests.

## System requirements

You need Python 3 to run this script.

## Installation

1. Download the files in this directory to your computer.
2. Create a virtual environment for the third-party dependencies:
    ```bash
    $ python3 -m venv venv_prl_joai_admin
    ```
3. Activate the virtual environment:
    ```bash
    $ . venv_prl_joai_admin/bin/activate
    ```
4. Install third-party dependencies:
    ```bash
    $ pip install -r requirements.txt
    ```


## Usage

Running the script takes the user to a REPL that provides usage hints. The script can be run with no arguments if interacting with the test environment. To interact with the production environment, you must point it to the production jOAI instance.

For usage instructions:
```bash
$ ./prl_joai_admin.py -h
```

The input CSV file should be filled out with a row for each harvest to add to jOAI. Here is the schema:

|field|description|example|
|---|---|---|
|`Repository name`|The human-readable name of the institution as it appears on http://prl.library.ucla.edu/institutions. MUST NOT be blank.|`University of California Los Angeles`|
|`Repository base URL`|The OAI-PMH repository base URL, as specified in https://www.openarchives.org/OAI/openarchivesprotocol.html#HTTPRequestFormat. MUST NOT be blank.|`http://digital2.library.ucla.edu/oai2_0.do`|
|`OAI-PMH SetSpec`|The OAI-PMH set identifier that specifies the set to be harvested, as specified in https://www.openarchives.org/OAI/openarchivesprotocol.html#Set. Leave blank if harvesting all sets from the repository, or if the entire repository represents one collection for PRL. **See below for usage rules.**|`east_asian_maps`|
|`Set directory`|A name for the parent directory of the harvested records. Can be any legal UNIX directory name. It is RECOMMENDED to use the `repositoryIdentifier` field in the response to the Identify request on the OAI-PMH repository, as specified in https://www.openarchives.org/OAI/2.0/guidelines-oai-identifier.htm. **See below for usage rules.**|`library.ucla.edu`|
|`Harvest every X days`|The number of days between re-harvests. MUST NOT be blank. Must be an integer.|1|
|`Harvest at time T`|The time of day (PST) to re-harvest at. MUST NOT be blank. Must be a datetime formatted like `%H%M`.|`03:00`|
|`skip`|Whether or not to skip this row during invocation of the script. May be blank.|`y`|

Further rules:
- The values in the `Repository name`, `Repository base URL`, and `OAI-PMH SetSpec` MAY be wrapped in single quotes if they contain commas. All other columns MUST NOT be wrapped in quotes.
- `OAI-PMH SetSpec` and `Set directory` MUST be used as follows:

    |objective|`OAI-PMH SetSpec`|`Set directory`|
    |---|---|---|
    |harvest a single set from a repository as a dinstinct PRL collection|fill out|*leave blank*|
    |harvest an entire repository as a distinct PRL collection|*leave blank*|fill out|
    |harvest all sets from a repository as dinstinct PRL collections|*leave blank*|*leave blank*|

- `OAI-PMH SetSpec` and `Set directory` MUST NOT both be filled out (both non-empty) at the same time, but they MAY both be blank.

You will probably want to use the CSV file at <https://ucla.app.box.com/file/511596765114>.

## Error logs

The script logs errors to rotating logfiles that are each guaranteed not to exceed 1 MiB in size.

If `prl_joai_admin.debug.log.1` exists, it contains older entries than `prl_joai_admin.debug.log`.

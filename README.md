# MOSS Plagiarism Checker

A script that checks plagiarism using [Stanford's MOSS tool](https://theory.stanford.edu/~aiken/moss/).

## Usage

    main.py [-h] --students STUDENTS --homeworks-dir HOMEWORKS_DIR --report-dir REPORT_DIR --moss-userid MOSS_USERID --moss-tag MOSS_TAG

- Students CSV contains first name, last name, ASURite (ASU username), and github username. Example -

        first_name,last_name,asurite,github_username
        Shubham,Chawla,schawl17,shubham1chawla

- Homeworks directory contains all the submissions downloaded using GitHub Classroom CLI.
- Report directory is a temporary folder where all the reports, including moss script, are exported.
- MOSS User ID is the unique ID registered with MOSS IT team.
- MOSS Tag is the name given to the report.

## Sample output from the script

    WARNING:root:No student record found for 'pqr'
    INFO:root:Loaded 145 students from 'students.csv'
    INFO:root:Exported overall javascript report to 'report/overall_javascript_report.csv'
    WARNING:root:Following students didn't follow 'asurite.js' naming convention
        asurite   github_username  js_files  naming_convention
    21  abc       abc              1         False
    INFO:root:Exported naming convention report to 'report/convention_report.csv'
    WARNING:root:Following students have multiple javascript files
        asurite github_username  js_files  naming_convention
    32  xyz     xyz              2         True
    INFO:root:Exported multiple javascript files report to 'report/multi_javascript_report.csv'
    INFO:root:Exported combined javascript files to: report/js
    INFO:root:Removing previous moss script file from 'report/moss.pl'
    INFO:root:Exported moss script output to 'report/moss_report.log'

## Sample MOSS report output

    Checking files . . . 
    OK
    Uploading report/js/abc.js ...done.
    Uploading report/js/xyz.js ...done.
    Query submitted.  Waiting for the server's response.
    http://moss.stanford.edu/results/<123>/<123456789>

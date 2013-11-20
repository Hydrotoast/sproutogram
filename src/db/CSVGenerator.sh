#!/bin/bash
sqlite3 extractions.db <<!
.headers on
.mode csv
.output overview.csv
SELECT * FROM overview;
!

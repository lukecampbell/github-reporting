github-reporting
================

Python scripts to generate reports from github repos


Installation
===

First install PyYAML
```
pip install -r requirements.txt
```

Then specify your personal github api access token in reports/config/config.yml



## Available Scripts

### Monthly Report

Once you've configured your personal github api access token, add a repositories list to reports/config/config.yml

To run the monthly report

```
python reports/monthly.py <filename> <start-date> <end-date>
```

This will generate a csv file that has a table structure like

|repo|issues created|issues closed|pull requests opened|pull requests closed|comments created|commits|releases|
|----|--------------|-------------|--------------------|--------------------|----------------|-------|--------|
|ioos/compliance-checker|1|0|1|0|0|15|3|
|ioos/catalog|24|1|0|0|6|51|3|
|ioos/pyoos|1|2|0|0|1|4|4|
|ioos/wicken|0|0|0|0|0|5|3|
|ioos/petulant-bear|1|1|1|1|2|7|3|
|ioos/metamap|0|0|0|0|0|0|0|
|asascience-open/sci-wms|0|0|0|0|0|1|0|
|asascience-open/ncsos|0|0|0|0|0|0|6|
|asascience-open/paegan|0|0|0|1|1|6|3|
|nctoolbox/nctoolbox|7|4|5|5|42|19|0|

### Issues Report

To run the issues report

```
python reports/issues.py <repository> <filename> <start-date> <end-date>
```

This will generate a csv fiel that has a table structure like

|Issue Number|Title|Status|Closed At|
|------------|-----|------|---------|
|579|Update urls (moved to production)|open|None|
|578|Modify Atlantic Salmon cartography|open|None|
|577|Homepage Layout on IE10|open|None|
|576|"Nitpick: If opening Data Download while reading content about specific theme, section where that theme's data is located should expand"|open|None|
|575|Missing more info text for NPS|closed|2014-12-17T13:59:03Z|
|574|Lite Viewer menu goes to next line|open|None|
|573|Update Coastal Wetlands metadata on download page|closed|2014-12-17T13:38:16Z|

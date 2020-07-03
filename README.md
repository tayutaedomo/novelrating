# novelfind

## Setup
```
$ git clone git@github.com:tayutaedomo/novelfind.git 
$ cd novelfind
$ python3 -m venv venv 
$ source venv/bin/activate
```


## Scraping Commands
1. Get bookmark list
```
$ export NAROU_EMAIL=<Your Email or ID>
$ export NAROU_PASSWORED=<Your Password>
$ python scripts/scraping/bookmark.py
```

2. Get ratings of the bookmark list
```
$ export NAROU_EMAIL=<Your Email or ID>
$ export NAROU_PASSWORED=<Your Password>
$ python scripts/scraping/bookmark_rating.py
```

3. Download novel pages of the bookmark list
```
$ python scripts/scraping/novel_page_bulk.py bookmark
```
or
```
$ python scripts/scraping/novel_pages.py ncode <Target ncode>
```

4. Download novel info of the bookmark list
```
$ python scripts/scraping/novel_info.py bookmark
```

5. Get ranking novel list
```
$ python scripts/scraping/ranking.py all
```
or
```
$ python scripts/scraping/ranking.py path <Target ranking_path>
```

6. Download novel pages of the bookmark list
```
$ python scripts/scraping/novel_pages.py ranking
```

7. Download novel info of the ranking novel list
```
$ python scripts/scraping/novel_info.py ranking
```

8. Create page summary files
```
$ python scripts/model/novel_page_summary.py (all|bookmark|ranking)
```


# novelrating

## Setup
```
$ git clone git@github.com:tayutaedomo/novelrating.git 
$ cd novelrating
$ python3 -m venv venv 
$ source venv/bin/activate
```


## Commands
### Create Train Data
1: Get novel list of your bookmark
```
$ export NAROU_EMAIL=<Your Email or ID>
$ export NAROU_PASSWORED=<Your Password>
$ python scripts/scraping/bookmark.py
```

2: Get ratings of the bookmark list
```
$ export NAROU_EMAIL=<Your Email or ID>
$ export NAROU_PASSWORED=<Your Password>
$ python scripts/scraping/bookmark_rating.py
```

3: Download novel info of the bookmark list
```
$ python scripts/scraping/novel_info.py bookmark
```

4: Download novel pages of the bookmark list
```
$ python scripts/scraping/novel_pages.py bookmark
```

5: Create novel pages summary
```
$ python scripts/converting/novel_page_summary.py bookmark
```

6: Create train data
```
$ python scripts/converting/bookmark_data_create.py
```

### Create Test Data
1: Get novel ranking list
```
$ python scripts/scraping/ranking.py all
```
or
```
$ python scripts/scraping/ranking.py path <Target ranking_path>
```

2: Download novel info of the ranking list
```
$ python scripts/scraping/novel_info.py ranking
```

3: Download novel pages of the ranking list
```
$ python scripts/scraping/novel_pages.py ranking
```

4: Create novel pages summary
```
$ python scripts/converting/novel_page_summary.py ranking
```

5: Create test data
```
$ python scripts/converting/ranking_data_create.py
```


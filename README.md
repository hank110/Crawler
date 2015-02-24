# Crawler
=======

### Weibo Content Crawler 

#### 2015-01-27:

- All crawling modules completed
- Revisions to error completed
- Need to put them in json format

#### 2015-02-02:  
- Changed the target URL to only crawl the actual weibo excluding the ads and sponsored pages (this can be easily implemented later depending on the circumstances)
- Need to surmount the issue of logging in to view the entire list of tweet and resolve the issue of crawling frequency



#### 2015-02-03:
- can log in the weibo through input ID and PASS
- Can crawl the page after logging in and continue to move to next pages  

#### 2015-02-08:
##### Things to Tweak Around
- How to stop this crawler? When to stop this crawler?
	- doesn't take long time to compare the latest (one-by-one) prior to making it in json file
- What happens after page 50? (It repeats)
	- Repeat of page 1 
	- Stopped at max 50
- Duplicate prevention method to prevent the crawler from crawling duplicate posts compared with previous crawling session
- Exception handling for weird posts without names & urls (Resolved)
	- possibly exception handling for index error
	- Or is there a better way to handle this without loss of posts?

#### 2015-02-24:
- How to stop this crawler? When to stop this crawler? (Resolved)
	- Stopped when click button doesn't exit
	- consequently move to different time period
- perhaps better naming?
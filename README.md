# Crawling_Team_L
Search Engine Crawler for Fall 2017 Large Scale Programming &amp; Testing at Rensselaer Polytechnic Institute

# Running the crawler
To run the crawler, you must first run Crawling_L_REST.py and that will wait for a post.  Then you must send and HTTP POST to the default address http://0.0.0.0:8080/new_links.

The body of the post should be in the format:
```
{
	"links": ["http://rpi.edu/", "http://www.cs.rpi.edu/~goldsd/index.php"]
}
```

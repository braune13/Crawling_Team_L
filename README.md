# Crawling_Team_L
Search Engine Crawler for Fall 2017 Large Scale Programming and Testing at Rensselaer Polytechnic Institute

# Running the crawler
To run the crawler, you must first run Crawling_L_REST.py , which will start the crawler's Flask server. The server will wait for a POST to /new_links in order to kick off the crawler. You must send an HTTP POST to the default server address http://0.0.0.0:8080/new_links.

The body of the post should be in the format below and have a content type of "application/json":
```
{
	"links": ["http://rpi.edu/", "http://www.cs.rpi.edu/~goldsd/index.php"]
}
```

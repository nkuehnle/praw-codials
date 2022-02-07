# PRAW-CoDiaLS

A niche CLI tool built using the Python Reddit API Wrapper (PRAW) for **Co**mmunity & **D**oma**i**n-T**a**rgeted **L**ink **S**craping.

Written for Python 3 (3.6 required due to liberal use of fstrings). **Third party modules needed**: praw, pyaml, and pandas.

## Installation

PRAW-CoDiaLS is available from either this repository or via PyPI:

Recommended:

```
$ pip install praw-codials
```

Alternatives:

Download the .whl file or .tar.gz file and then run the appropriate command.

```
$ pip install praw_codials-1.0.1-py3-none-any.whl -r requirements.txt
```

```
$ praw-codials-1.0.1.tar.gz -r requirements.txt
```

You can also build a wheel locally from source to incorporate new changes.

```
python -r setup.py bdist_wheel
```

## Usage

Valid Reddit OAuth is required for usage. [See Reddit's guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example) on how to obtain this and set it up. In short you will need to provide a client_id, client_secret, username, password, and client_agent.

<pre>
usage: praw-codials [-h] -s list,of,subs -d list,of,domains -o client_id,client_secret,password,username,user_agent [-p PATH] /path/to/save/output/ [-l LIMIT] #of posts to search [--new] [--controversial] [--hot] [--top] [--quiet] [--nocomments]

_Python Reddit API Wrapper (PRAW) for Community & Domain-Targeted Link Scraping._

  -h, --help            show this help message and exit
  -s SUBS, --subs SUBS  Subreddit(s) to target. (Comma-separate multiples)
  -d DOMAINS, --domains DOMAINS
                        Domain(s) to collect URLs from. (Comma-separate multiples)

  -o OAUTH, --oauth OAUTH
                        OAuth information, either comma separated values in order (client_id, client_secret, password, username, 
                        user_agent) or a path to a key/value file in YAML format.
 
  -p PATH, --path PATH  Path to save output files (Posts_[DATETIME].csv and Posts_[DATETIME].csv. Default: working directory
  -l LIMIT, --limit LIMIT
                        Maximum threads to check (cannot exceed 1000).
  -t TOP, --top TOP     Search top threads. Specify the timeframe to consider (hour, day, week, month, year, all)
  -c CONTROVERSIAL, --controversial CONTROVERSIAL
                        Search controversial threads. Specify the timeframe to consider (hour, day, week, month, year, all)
  --hot                 Search hot posts.
  -n, --new             Search new posts.
  -q, --quiet           Supress progress reports until jobs are complete.
  -x, --nocomments      Don't collect links in top-level commentsReduces performance limitations caused by the Reddit API
</pre>


## Implementation Details
By default, this tool will return URLs collected from both link submissions (the main post for each thread) and the top-level comments for either text or link submissions (self/link posts), but not their children. This can be optionally disabled at the command line (see below). In a future update, I plan to provide an argument for setting a comment recursion depth; however, any such features will drastically impact performance due to the Reddit API rate-limit.

On that train of thought, please note that Reddit enforces rate limits. This means that this script will likely check between 80-100 pieces of content per minute. To improve performance, this script opens multiple PRAW instances and makes use of the Python multi-threading module to gain a small performance boost. In my limited testing, this improved throughput by approximately 33% from ~65 posts/min to ~85 posts/min when enabling all subreddit search methods (hot/top (all)/new/controversial (all)) with the default post limit (1000) across two subreddits and two domains. This ammounts to checking approximately 8K posts and tens of thousands of comments).

To further limit requests, it tries to ensure that it minimizes the number of comments it could access twice (i.e. in Top and Hot) by storing lists of submission and comment IDs that have already been encountered.

Output reports the following statistics as columns of two separate multi-row CSV files (one for submissions and one for comments, if included):

* Submissions: post author, post ID, title, url, subreddit, score, upvote ratio (note: these are approximate/obfuscated), and post flair
* Comments: comment author,comment ID, body (including Markdown), subreddit, score, all of the above attributes as they pertain to the comment's parent submission/thread, and URL's obtained by simple RegEx (multiple entries/rows are generated if multiple links matching the target domain(s) are found in the text body)

If you think that I've missed an important attribute, please let me know!


## License

PRAW-CoDiaLS is released under the MIT License. See LICENSE for details.


## Contact

To report issues or contribute to this project, please contact me on [the GitHub repo for this project](http://github.com/nkuehnle/praw-codials).

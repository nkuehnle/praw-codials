"""
A module for creating the CLI parser instance.
"""
from pathlib import Path
from argparse import ArgumentParser

# Global variables
CWD = Path.cwd()

CLI_DESCR = "Python Reddit API Wrapper (PRAW) for Community & Domain-Targeted \
Link Scraping."

PATH_HELP = f"Path to save output files (Posts_[DATETIME].csv and\
 Posts_[DATETIME].csv. Default: working directory ({CWD})"

OAUTH_HELP = "OAuth information, either comma separated values in order\
 (client_id, client_secret, password, username, user_agent) or\
 a path to a key/value file in YAML format."

DOMAINS_HELP = "Domain(s) to collect URLs from. (Comma-separate multiples)"

SUBS_HELP = "Subreddit(s) to target. (Comma-separate multiples)"

LIMIT_HELP = "Maximum threads to check (cannot exceed 1000)."

TOP_HELP = "Search top threads. Specify the timeframe to consider\
 (hour, day, week, month, year, all)"

CONTROVERSIAL_HELP = "Search controversial threads. Specify the timeframe to\
 consider (hour, day, week, month, year, all)"

NO_CMTS_HELP = "Don't collect links in top-level comments\
 Reduces performance limitations caused by the Reddit API."

REGEX_HELP = "Override automatically generated regular expressions.\
 NOTE: Assumes escape characters are provided in such as way that the\
 shell pass a properly escaped literal string to python."

###########  Define Argument Parser ###########
# TODO: Implement arguments to supresse flair, score, etc.
# TODO: Implement argument(s) for comment recursion level limits.
CLI = ArgumentParser(description = CLI_DESCR)
CLI.add_argument(
                 "-s",
                 "--subs",
                 type = str,
                 required = True,
                 help = SUBS_HELP
                 )
CLI.add_argument(
                 "-d",
                 "--domains",
                 type = str,
                 required = True,
                 help = DOMAINS_HELP
                 )
CLI.add_argument(
                 "-o",
                 "--oauth",
                 type = str,
                 required = True,
                 help = OAUTH_HELP
                 )
CLI.add_argument(
                 "-p",
                 "--path",
                 type = str,
                 required = False,
                 default = str(CWD),
                 help = PATH_HELP
                 )
CLI.add_argument(
                 "-l",
                 "--limit",
                 type=int,
                 required = False,
                 default = 1000,
                 help = LIMIT_HELP
                 )
CLI.add_argument(
                 "-t",
                 "--top",
                 type = str,
                 required = False,
                 help = TOP_HELP
                 )
CLI.add_argument(
                 "-c",
                 "--controversial",
                 type = str,
                 required = False,
                 help=CONTROVERSIAL_HELP
                 )
CLI.add_argument(
                 "--hot",
                 action = "store_true",
                 help = "Search hot posts."
                 )
CLI.add_argument(
                 "-n",
                 "--new",
                 action = "store_true",
                 help = "Search new posts."
                 )
CLI.add_argument(
                 "-q",
                 "--quiet",
                 action = "store_true",
                 help = "Supress progress reports until jobs are complete."
                 )
CLI.add_argument(
                 "-x",
                 "--nocomments",
                 action = "store_true",
                 help = NO_CMTS_HELP)
CLI.add_argument(
                 "--regex",
                 type = str,
                 required = False,
                 help = REGEX_HELP
)

from .storage_classes import ContentLibrary
import praw
import logging
import datetime as dt
import sys

def time_delta_str(start: dt.datetime, end: dt.datetime) -> str:
    """Simple utility function to create a human-readable time-delta string

    Parameters
    ----------
    start : dt.datetime
        datetime object for startpoint as a string
    end : dt.datetime
        datetime object for endpoint as a string

    Returns
    -------
    [str]
        A human-readable string which takes all units between seconds to years
        > 0 and returns them as [quantity unit, ... and quantity unit]
    """
    time_elapsed = end - start

    time_str = []
    for unit in ('months','weeks','days','hours','minutes','seconds'):
        quantity = getattr(time_elapsed, unit, 0)
        if quantity > 0:
            time_str.append(f'{quantity} {unit}, ')

    if len(time_str) > 1:
        time_str[-1] = time_str[-1].replace(', ', ' and ')
    else:
        time_str[-1] = time_str[-1].replace(', ', '')

    return ''.join(time_str)

class CollectionJob:
    def __init__(self, job_id, auth, sub, domains, sort, limit, num_jobs=None):
        """A class for storing the information relevant to a given search job.
        This supports multi-threading functionality at run-time. A new PRAW 
        instance is generated and performs searches using this object.

        Parameters
        ----------
        job_id : int
            A numerical ID based on the order this job was generated at runtime
        auth : dict
            A dictionary containing the client's authentication information.
        sub : str
            The subreddit to search within.
        domains : list of str
            A list of domains to cross-reference each post with.
        sort : str
            A string identifying what type of posts to search for in the 
            indicated subreddit (hot, new, controversial, or top).
        limit : int
            Maximum number of posts to search (default = 1000; max = 1000).
        num_jobs : int
            Total number of jobs generated.
        """        
        self.auth = auth
        self.job_id = job_id
        self.sub = sub
        self.domains = domains
        self.sort = sort
        self.limit = limit
        self.num_jobs = num_jobs
        self.logger = logging.getLogger(f'JOB_{self.job_id}')
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    @property
    def jobnum(self):
        """Property for determining the order this job was generated.

        Returns
        -------
        str
            formated string "x/y" where, x is the job_id and y is num_jobs
        """
        return f"{self.job_id}/{self.num_jobs}"

    def __str__(self):
        str1 = f'Job {self.jobnum}, searching the '
        str2 = f'posts from '
        str3 = f"/r/{self.sub} for links to"
        str3 += f"{', '.join(i for i in self.domains)}"
        if self.sort == "hot":
            return str1+f'hottest {self.limit} '+str2+str3
        elif self.sort == "new":
            return str1+f'newest {self.limit} '+str2+str3
        elif self.sort == "controversial":
            return str1+f'{self.limit} most controversial '+str2+str3
        else:
            return str1+f'top {self.limit} '+str2+'the past month on '+str3

def collect_links(job: CollectionJob,
                  library: ContentLibrary,
                  verbose = True,
                  incl_cmts = True):
    """
    Basic function to run a job and append its results to the content library.
    
    TODO: Implement an argument for comment recursion level limits
    Search and collect the links associated with a provided job.

    Parameters
    ----------
    job : CollectionJob
        An instance of the CollectionJob class to process.
    library : ContentLibrary
        An instance of the ContentLibrary class to check for membership and
        add new submissions/links to.
    verbose : bool
        Whether to print regular progress updates.
    incl_cmts : bool
        Whether to also search top-level comments responses.
    """
    reddit = praw.Reddit(**job.auth)
    sub = reddit.subreddit(job.sub)
    sort = job.sort
    limit = job.limit

    ### Grab the correct post list.
    if sort == "hot":
        posts = sub.hot(limit=limit)
    elif sort == "new":
        posts = sub.new(limit=limit)
    elif sort == "controversial":
        posts = sub.controversial(limit=limit)
    else:
        posts = sub.top(time_filter=sort, limit=limit)

    # Counts for number of posts checked, and links found + the start time.
    check_cnt = 0
    start = dt.datetime.now()
 
    job.logger.info(f"Started: {job} @ {start.strftime('%Y/%m/%d @ %H:%M:%S')}")

    # Look through posts
    for post in posts:
        check_cnt += 1 # Increment the counter for the # of checks performed.

        if not(post.id in library._checked_post_ids):
            library._checked_post_ids.add(post.id)
            if post.num_comments > 0 and incl_cmts == True:
                post.comments.replace_more(limit=None, threshold=0)
                cmts = post.comments.list()

                for cmt in cmts:
                    new_cmt = not(cmt.id in library._checked_cmt_ids)
                    if new_cmt:
                        library._checked_cmt_ids.add(cmt.id)
                        body = str(cmt.body)
                        domain_present = any([d in body for d in job.domains])
                        if domain_present:
                            library.add(
                                subreddit = sub,
                                targets = job.domains,
                                content = cmt,
                                parent = post)

            if not(post.is_self):
                for domain in job.domains:
                    if domain in post.url:
                        library.add(
                            subreddit = sub,
                            targets = job.domains,
                            content = post)

        if verbose:
            # Check counter and report back.
            for i in (.25, .5, .75, 1):
                if check_cnt == int(limit*i):
                    message = f'{job}\n{i*100:.0f}% completed in '
                    message += f"{time_delta_str(start, dt.datetime.now())}."
                    message += f'\n{check_cnt} threads checked, found '
                    message += f'{len(library.submissions)} link submissions'
                    if incl_cmts:
                        message += '.'
                    else:
                        message += f' and {len(library.comments)} top-level'
                        message += 'comments containing links.'

                    job.logger.info(message)
from typing import Optional, Union, List, Set
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment
from dataclasses import dataclass
import re
from pathlib import Path
import datetime as dt
import pandas as pd

@dataclass
class LinkContent:
    """A dataclass for storing pertinent link content information"""
    link: str
    submission_author: str
    submission_id: str
    submission_title: str
    subreddit: str
    submission_flair: Optional[str] = None
    submission_score: Optional[int] = None
    submission_upvote_ratio: Optional[float ] = None
    submission_date: Optional[dt.datetime] = None
    comment_author: Optional[str] = None
    comment_id: Optional[str] = None
    comment_score: Optional[str] = None
    comment_body: Optional[str] = None
    comment_date: Optional[dt.datetime] = None

class ContentLibrary:
    def __init__(self,
                 submissions: List[LinkContent],
                 comments: List[LinkContent]):
        """A class for keeping track of different submission/post content.

        Parameters
        ----------
        submissions : List[LinkContent]
            A list of submissions (top-level posts)
        comments : List[LinkContent]
            A list of top-level comments (reponses to submissions)
        """
        self.submissions = submissions
        self.comments = comments
        self._checked_post_ids = set([])
        self._checked_cmt_ids = set([])

    def add(self,
            subreddit: str,
            regex: List[str],
            content: Union[Submission, Comment],
            parent: Optional[Union[Submission, Comment]] = None):
        """Add item to the content library.

        Parameters
        ----------
        subreddit : str
            The name of the subbreddit the content was collected from.
        regex : List[str]
            The URLs that were targetted in this search this search
        content : Union[Submission, Comment]
            The praw.models.Submission or praw.models.Comment instanc
        parent : Optional[Union[Submission, Comment]], optional
            A parent for the main content, by default None
        """
        if not content.author:
            author = None
        else:
            author = content.author.name

        if isinstance(content, Submission):
            arguments = {
                'link': content.url,
                'submission_author': author,
                'submission_id': content.id,
                'submission_title': content.title,
                'submission_flair': content.link_flair_text,
                'submission_upvote_ratio': content.upvote_ratio,
                'submission_score': content.score,
                'submission_date': content.created_utc,
                'subreddit': subreddit,
            }

            self.submissions.append(LinkContent(**arguments))

        elif isinstance(content, Comment):
            if parent == None or isinstance(parent, Comment):
                parent = content.submission

            if not parent.author:
                sub_author = None
            else:
                sub_author = parent.author.name

            arguments = {
                    'submission_author': sub_author,
                    'submission_id': parent.id,
                    'submission_title': parent.title,
                    'submission_flair': parent.link_flair_text,
                    'submission_upvote_ratio': parent.upvote_ratio,
                    'submission_score': parent.score,
                    'submission_date': parent.created_utc,
                    'subreddit': subreddit,
                    'comment_id': content.id,
                    'comment_author': author,
                    'comment_score': content.score,
                    'comment_body': str(content.body),
                    'comment_date': content.created_utc
                    }

            links = []
            
            for r in regex:
                links += re.findall(r, arguments['comment_body'])

            if any(links):
                for link in links:
                    arguments['link'] = link
                    self.comments.append(LinkContent(**arguments))
            else:
                arguments['link'] = None
                self.comments.append(LinkContent(**arguments))

    @property
    def unique_submissions(self) -> Set[str]:
        return {[s.submission_id for s in self.submissions]}

    @property
    def unique_comments(self) -> Set[str]:
        return {[c.comment_id for c in self.comments]}

    def __contains__(self, other: Union[Submission, Comment]):
        if isinstance(other, Submission):
            return other.id in self.unique_submissions
        elif isinstance(other, Comment):
            return other.id in self.unique_comments

    def write_results(self, out_path: Path, incl_cmts: bool):
        """Write the contents of the submission and comment libraries to CSV

        Parameters
        ----------
        out_path : Path
            Directory to save output.
        incl_cmts : bool
            Whether comments were included.
        """
        date_str = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        submissions_path = out_path / f'Submissions_{date_str}.csv'
        
        # Save submissions as CSV.
        print(f"Writing submissions to {submissions_path}...")
        submissions_df = pd.DataFrame([i.__dict__ for i in self.submissions])
        submissions_df.to_csv(submissions_path, sep=",")

        # Save comments as CSV, if requested.
        if incl_cmts == True:
            cmts_path = out_path / f'Comments_{date_str}.csv'
            print(f"Writing comments to {cmts_path}")
            cmts_df = pd.DataFrame([i.__dict__ for i in self.comments])
            cmts_df.to_csv(cmts_path, sep=",")
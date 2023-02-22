# Code adapted from https://towardsdatascience.com/scraping-reddit-with-praw-76efc1d1e1d9
from os.path import isfile
import praw
import pandas as pd
from time import sleep
from langdetect import detect

# Get credentials from DEFAULT instance in praw.ini
reddit = praw.Reddit()

class SubredditScraper:

    def __init__(self, sub, q, sort='new', lim=900, mode='w'):
        self.sub = sub
        self.sort = sort
        self.lim = lim
        self.mode = mode
        self.query = q
        print(
            f'SubredditScraper instance created with values '
            f'sub = {sub}, sort = {sort}, lim = {lim}, mode = {mode}, query = {q}')

    def set_sort(self):
        return self.sort, reddit.subreddit(self.sub).search(self.query)

    def get_posts(self):
        """Get unique posts from a specified subreddit."""

        sub_dict = {
            'selftext': [], 'title': [], 'id': []}
        csv = f'{self.sub}_posts.csv'

        # Attempt to specify a sorting method.
        sort, subreddit = self.set_sort()

        # Set csv_loaded to True if csv exists since you can't 
        # evaluate the truth value of a DataFrame.
        df, csv_loaded = (pd.read_csv(csv), 1) if isfile(csv) else ('', 0)

        print(f'csv = {csv}')
        print(f'After set_sort(), sort = {sort} and sub = {self.sub}')
        print(f'csv_loaded = {csv_loaded}')

        print(f'Collecting information from r/{self.sub}.')

        for post in subreddit:
            # Check if the post language is portuguese (can be changed if Reddit implements a language filter like a fucking normal social media platform)
            if detect(post.title) != "pt":
                continue
            # Check if post.id is in df and set to True if df is empty.
            # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique posts to sub_dict.
            if unique_id:
                sub_dict['selftext'].append(post.selftext)
                sub_dict['title'].append(post.title)
                sub_dict['id'].append(post.id)
            sleep(0.1)

            new_df = pd.DataFrame(sub_dict)

            # Add new_df to df if df exists then save it to a csv.
            if 'DataFrame' in str(type(df)) and self.mode == 'w':
                pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)
                print(
                    f'{len(new_df)} new posts collected and added to {csv}')
            elif self.mode == 'w':
                new_df.to_csv(csv, index=False)
                print(f'{len(new_df)} posts collected and saved to {csv}')
            else:
                print(
                    f'{len(new_df)} posts were collected but they were not '
                    f'added to {csv} because mode was set to "{self.mode}"')

if __name__ == '__main__':
    SubredditScraper(
        'naobinarie',
        'amigue OR elu OR amigues OR todes OR ile OR delu',
         lim=10000,
         mode='w',
         sort='hot').get_posts()





from datetime import date
import requests
import json
import pandas
import os


youtube_channel_id = "UC9B_3nunpB-u-1gybsw5DHw"
youtube_key = os.environ["YOUTUBEKEY"]
github_repo = "pyiron/pyiron"
linkedin_id = "20541491"
stackoverflow_tag = "pyiron"
data_download = "http://jan-janssen.com/pyiron-statistics/social.csv"


def get_github_stars(github_repo):
    github_url = "https://api.github.com/repos/" + github_repo
    r = requests.get(github_url)
    content = json.loads(r.text)
    return int(content['stargazers_count'])


def get_youtube_subs(youtube_channel_id, youtube_key):
    youtube_url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + youtube_channel_id + "&key=" + youtube_key
    r = requests.get(youtube_url)
    content = json.loads(r.text)
    return int(content['items'][0]['statistics']['subscriberCount'])


def get_linkedin_followers(linkedin_id):
    linkedin_url = "https://www.linkedin.com/pages-extensions/FollowCompany?id=" + linkedin_id + "&counter=bottom"
    r = requests.get(linkedin_url)
    for l in r.text.split("\n"):
        if "follower-count" in l:
             return int(l.split(">")[1].split('<')[0])


def get_stackoverflow_questions(stackoverflow_tag):
    counts = []
    for site in ["mattermodeling.stackexchange.com", "stackoverflow.com"]:
        stackoverflow_url = "https://api.stackexchange.com/search/advanced?site=" + site + "&q=[" + stackoverflow_tag + "]]"
        r = requests.get(stackoverflow_url)
        content = json.loads(r.text)
        counts.append(len(content["items"]))
    return sum(counts)


def download_existing_data(data_download):
    return pandas.read_csv(data_download, index_col=0)


def update(github_repo, youtube_channel_id, youtube_key, linkedin_id, stackoverflow_tag, data_download):
    df_old = download_existing_data(data_download=data_download)
    return df_old.append(pandas.DataFrame({
        "Date": [date.today().strftime("%Y/%m/%d")], 
        "Github": [get_github_stars(github_repo=github_repo)], 
        "Linkedin": [get_linkedin_followers(linkedin_id=linkedin_id)], 
        "Youtube": [get_youtube_subs(youtube_channel_id=youtube_channel_id, youtube_key=youtube_key)], 
        "Stackoverflow": [get_stackoverflow_questions(stackoverflow_tag=stackoverflow_tag)]
    }), ignore_index=True)
    

df = update(
    github_repo=github_repo, 
    youtube_channel_id=youtube_channel_id, 
    youtube_key=youtube_key, 
    linkedin_id=linkedin_id, 
    stackoverflow_tag=stackoverflow_tag, 
    data_download=data_download
)
df.to_csv("social.csv")

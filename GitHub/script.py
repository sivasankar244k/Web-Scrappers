from github import Github
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import json
import requests
import csv

def login(username, password):
    """
    [Auth Function]

    Arguments:
        username {[str]} -- [GitHub username]
        password {[str]} -- [GitHub password]
    
    Returns:
        [object] -- [Authenticated GitHub object]
    """

    githubInstance = Github(username, password)
    return githubInstance

def getLanguage(repoURL, user):
    languages = []
    repos = user.get_repos()
    for repo in repos:
        if not repo.language:
            pass
        else:
            languages.append(repo.language)
    if len(languages) == 0:
        languages = {}
    else:
        languages = set(languages)
    return languages

def getJSON(APIEndpoint):
    response = requests.get(APIEndpoint)
    content = json.loads(response.text)
    return content

def scrapper(username, password):
    github_instance = login(username,password)
    page = 1
    while page < 11:
        try:
            url = 'https://api.github.com/search/users?q=location:china+followers:<217&type=user&page='+str(page)+'&per_page=100'
            users = getJSON(url)
            with open('ChinaTop1001-2000.csv', 'a', newline='') as outfile:
                headers = ['Name', 'Bio', 'Location', 'Email', 'Site', 'Followers', 'Repos', 'Languages', 'Link']
                writer = csv.DictWriter(outfile, fieldnames=headers)
                # writer.writeheader()
                for item in users['items']:
                    print('Scrapping Page', page, 'User Number', users['items'].index(item)+1, 'of', len(users['items']))            
                    try:
                        user = github_instance.get_user(item['login'])
                        github_name = user.name
                        github_bio = user.bio
                        github_location = user.location
                        github_email = user.email
                        github_site = user.blog
                        github_followers = user.followers
                        github_repo = item['html_url'] + '?tab=repositories'
                        github_link = item['html_url']
                        github_languages = str(getLanguage(item['repos_url'], user)).replace('{','').replace('}','')
                    except Exception as e:
                        print(e)
                        pass
                    finally:
                        writer.writerow({'Name': github_name, 'Bio': github_bio, 'Location':github_location, 'Email': github_email, 'Site': github_site, 'Followers': github_followers, 'Repos': github_repo, 'Languages': github_languages, 'Link': github_link})
                        username = ''
                        github_name = ''
                        github_bio = ''
                        github_location = ''
                        github_email = ''
                        github_site = ''
                        github_followers =  ''
                        github_repo = ''
                        github_languages = ''
                        github_link = ''
        except Exception as e:
            print(e)
            pass
        finally:
            page += 1


if __name__ == '__main__':
    # getUsername()
    # getLanguage('https://api.github.com/users/dorsywang/repos')
    scrapper('brandeddavid', 'marigi@98')
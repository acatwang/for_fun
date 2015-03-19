"""
Inspired by Akshit Khurana

Comment on the birthday posts on your wall

TODO:
The get_posts function fails to retrieve all posts from the wall. 
An explanation of this issue can be found here https://developers.facebook.com/blog/post/478/

"""

import requests
import json
import time


TOKEN = '<Get a token from FB GRAPH API>'

## Type in your birthday here
curr_year = 2015
month = 3
date = 15

d = datetime.date({0},{1},{2}).format(curr_year,month,date)
DATETIME = time.mktime(d.timetuple())

# Or use online converter to get the timestamp
#DATETIME = "1425168000"

def get_posts():
    """Returns dictionary of user_id and messages of on the wall
    between start and end time"""
    
    query = ("SELECT post_id, actor_id, message, created_time, filter_key FROM stream "
            " WHERE filter_key = 'others' AND source_id = me() AND "
            "created_time > %s LIMIT 200 " % DATETIME)
 
    payload = {'q': query, 'access_token': TOKEN}
    r = requests.get('https://graph.facebook.com/fql', params=payload)
    result = json.loads(r.text)
    return result['data']
 
def commentall(wallposts):
    """Comments thank you on all posts"""
    for wallpost in wallposts:      
        url = 'https://graph.facebook.com/%s/comments' % wallpost['post_id']
        r = requests.get('https://graph.facebook.com/{0}?fields=name&access_token={1}'.format(
            wallpost['actor_id'],
            TOKEN))
        print r.text # in order to check error messeage
        
        # return name, id
        user = json.loads(r.text)
        first_name = user['name'].split(' ')[0]
        print "Thanking ", first_name
        
        message = 'Thanks %s :)' % first_name
        payload = {'access_token': TOKEN, 'message': message}
        s = requests.post(url, data=payload)
 
        print "Wall post %s done" % wallpost['post_id']
 
if __name__ == '__main__':
    posts = get_posts()
    print "You got %s messages" % len(posts)
    commentall(posts)
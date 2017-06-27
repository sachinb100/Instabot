#importing requests library to make network requests
import requests
import urllib
#a global variable for the instagram API access token
from key import  ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# a global variable for the base url of all the requests
BASE_URL="https://api.instagram.com/v1/"
#function for defining user own information
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    # a get call to fetch your details.
    user_info = requests.get(request_url).json()
    # checking whether user is successfully searched or not
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "My info is: \n",user_info
            print "My followers: %s \n"%(user_info['data']['counts']['followed_by'])
            print "people I follow:%s \n"%(user_info['data']['counts']['follows'])
            print "No. of posts:%s \n"%(user_info['data']['counts']['media'])
        else:
            print "User does not exist!"
    else:
        print"User code other than 200 recieved"
#function to get the user id of the user
def get_user_id(insta_username):
    request_url=(BASE_URL+"users/search?q=%s&access_token=%s")%(insta_username,ACCESS_TOKEN)
    print 'GET request url:%s'%(request_url)
    user_info=requests.get(request_url).json()
    # checking whether user is successfully searched or not
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return  user_info['data'][0]['id']
        else:
            return None
    else:
        print"User code other than 200 recieved and user cannot be found"
        exit()
#function to get other user's information
def get_user_info(insta_username):
#calling function to get id of the user
    user_id=get_user_id(insta_username)
    if user_id==None:
        print "User does not exist"
        exit()
    request_url=(BASE_URL+'users/%s?access_token=%s')%(user_id,ACCESS_TOKEN)
    print 'GET request url:%s'%(request_url)
    user_info=requests.get(request_url).json()
#checking whether user is successfully searched or not
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'
#function for getting our own post
def get_own_post():
    request_url=(BASE_URL+"users/self/media/recent?access_token=%s")%(ACCESS_TOKEN)
    print"Requesting media for%s"%(request_url)
    recent_post=requests.get(request_url).json()
    # download the most recent post and return it's post ID
    if recent_post['meta']['code'] == 200:
        if len(recent_post['data']):
            return recent_post['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print"Status code other than 200 recieved"

 #function for getting recent post of a user
def get_users_post(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + "users/%s/media/recent?access_token=%s") % (user_id,ACCESS_TOKEN)
    print"Requesting media for%s" % (request_url)
    recent_post=requests.get(request_url).json()
    #download the most recent post and return it's post ID
    if recent_post['meta']['code'] == 200:
        if len(recent_post['data']):
            image_name=recent_post['data'][0]['id']+'.jpeg'
            image_url=recent_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            return recent_post['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print"Status code other than 200 recieved"
    return None



#function for getting post-id of the post
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    request_url = (BASE_URL + "users/%s/media/recent?access_token=%s") % (user_id, ACCESS_TOKEN)
    print"Requesting media for%s" % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            print "Post exist"
            return user_media['data'][0]['id']
        else:
            print "Post does not exist"
    else:
        print"Status code other than 200 recieved"
    return None

#function for getting like made on our post
def get_like_list(insta_username):
    post_id=get_post_id(insta_username)
    request_url=(BASE_URL+"media/%s/likes?access_token=%s")%(post_id,ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    likes_info=requests.get(request_url).json()
    if likes_info['meta']['code']==200:
        if len(likes_info['data']):
            for x in range(0,len(likes_info['data'])):
                print likes_info['data'][x]['username']
        else:
            print "No user liked this post yet!"
    else:
            print"Status code other than 200 received"

#function to like the post of the user
def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    #making a POST call to like a post
    request_url=(BASE_URL+"media/%s/likes")%(media_id)
    payload={"access_token":ACCESS_TOKEN}
    print "Liking the post:%s"%(request_url)
    post_a_like=requests.post(request_url,payload).json()
    if post_a_like['meta']['code']==200:
        print "Like was successful"
    else:
        print"Your like was unsuccessful!Try Again"

#function for getting list of comment on a post
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") % (media_id, ACCESS_TOKEN)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code']==200:
        if len(comment_info['data']):
            for x in range(0,len(comment_info['data'])):
                print "Comment:%s || User:%s"%(comment_info['data'][x]['text'],comment_info['data'][x]['from']['username'])
        else:
            print "There are no comments on this post"
    else:
            print"Status code other than 200 received"

#function to make  a comment on a post
def make_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text=raw_input("Your Comment:")
    payload = {"access_token": ACCESS_TOKEN, "text" :comment_text}
    request_url = (BASE_URL + "media/%s/comments")%(media_id)
    print "Making comment on post:%s"%(request_url)
    make_comment=requests.post(request_url,payload).json()
    if make_comment['meta']['code']==200:
        print "Successfully added a comment"
    else:
        print"Unable to add comment.Try again"





#function for deleting a comment
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments/?access_token=%s") % (media_id, ACCESS_TOKEN)
    print "GET  request url :%s"%(request_url)
    comment_info=requests.get(request_url).json()
    if comment_info['meta']['code']==200:
        if len(comment_info['data']):

          for x in range(0,len(comment_info['data'])):
            comment_id=comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']

            blob=TextBlob(comment_text,analyzer=NaiveBayesAnalyzer())
            if(blob.sentiment.p_neg>blob.sentiment.p_pos):
                print 'Negative Comment%s'%(comment_text)
                delete_url=(BASE_URL+"media/%s/comments/%s/?access_token=%s") % (media_id,comment_id,ACCESS_TOKEN)
                print 'delete REQUEST-URL:%s'%(delete_url)
                delete_info=requests.delete(delete_url).json()
                if delete_info['meta']['code']==200:
                    print "Comment Successfully deleted"
                else:
                    print" 'Unable to delete comment!"
            else:
                print 'Positive comment : %s\n' % (comment_text)



        else:
            print "There are no existing comments on a post!"
    else:
        print "Status code other than 200 received"

#function for getting recent media liked by user
def get_recent_like():
        request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (ACCESS_TOKEN)
        recent_like_post = requests.get(request_url).json()
        if recent_like_post['meta']['code'] == 200:
            print "User like the recent media of:%s" % (recent_like_post['data'][0]['user']['username'])
            print "Media is:%s" % (recent_like_post['data'][0]['images']['thumbnail']['url'])
        else:
            print "Status code other than 200 recieved."

#function for getting minimum numer of likes
def get_creative_post():
            insta_username = raw_input("enter name of user")
            user_id = get_user_id(insta_username)
            request_url = (BASE_URL + "users/%s/media/recent?access_token=%s") % (user_id, ACCESS_TOKEN)
            print"Requesting media for%s" % (request_url)
            post = requests.get(request_url).json()
            l = []
            # download the most recent post and return it's post ID
            if post['meta']['code'] == 200:
                for x in range(0, len(post['data'])):
                    l.append(post['data'][x]['likes']['count'])

                print "Minimum number of likes is:%s" % (min(l))
                minimum_likes = min(l)
                for x in range(0, len(l)):
                    if l[x] == minimum_likes:
                        print"Post with minimum number of likes is:%s" % (
                        post['data'][x]['images']['standard_resolution']['url'])
            else:
                print"Status code other than 200 recieved"
            return None
#function for showing menu options to user
def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Get the recent media liked by user\n"
        print "k.Get the post with minimum number of likes\n"
        print "l.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_users_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           make_a_comment(insta_username)
        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "j":
            get_recent_like()
        elif choice=="k":
            get_creative_post()
        elif choice == "l":
            exit()
        else:
            print "wrong choice"

start_bot()


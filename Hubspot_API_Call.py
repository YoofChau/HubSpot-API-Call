from requests_oauthlib import OAuth2Session  
import os
import pickle
import json
import csv
import pandas as pd
import numpy as np
import os.path
import pygsheets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Replace with your App's Client ID and Secret
CLIENT_ID     = '' #API Key
CLIENT_SECRET = '' #Client Secret Key

# If modifying these scopes, delete the file hstoken.pickle.
SCOPES        = ['contacts','content', 'reports','business-intelligence']

#================================================================
#==== QuickStart Command-line App

def main():
    """
    Connects your app a Hub, then fetches the first Contact in the CRM.
    Note: If you want to change hubs or scopes, delete the `hstoken.pickle` file and rerun.
    """
    app_config = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scopes': SCOPES,
        'auth_uri': 'https://app.hubspot.com/oauth/authorize',
        'token_uri': 'https://api.hubapi.com/oauth/v1/token'
    }

    # The file hstoken.pickle stores the app's access and refresh tokens for the hub you connect to.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('hstoken.pickle'):
        with open('hstoken.pickle','rb') as tokenfile:
            token = pickle.load(tokenfile)
    # If no token file is found, let the user log in (and install the app if needed)
    else:
        token = InstallAppAndCreateToken(app_config)
        # Save the token for future runs
        SaveTokenToFile(token)

    # Create an OAuth session using your app_config and token
    hubspot = OAuth2Session(
        app_config['client_id'], 
        token=token, 
        auto_refresh_url=app_config['token_uri'],
        auto_refresh_kwargs=app_config, 
        token_updater=SaveTokenToFile
    )

    # Call the 'Get all contacts' API endpoint
    response_blog_posts = hubspot.get(
        #'https://api.hubapi.com/content/api/v2/blog-posts?start=20210511&end=20210520&limit=5'
        'https://api.hubapi.com/content/api/v2/blog-posts?start=20210414&end=20211231&limit=500'
        )

    b = response_blog_posts.text #.encode('utf-8')

    created_date_sign = "created_time"
    article_name_sign = '[],"label"'
    url_sign = 'false,"absolute_url"'
    post_id_sign = '"analytics_page_id":"'
    blog_name_sign = '","listing_layout_id'

    blog_name = []
    created_date = []
    article_name = []
    url = []
    posts_id = []
    count = 0
    for i in range (0, len(b) - 21):
        blog_name_total = b[i] + b[i+1] + b[i+2] + b[i+3] + (b[i+4]) + (b[i+5]) + (b[i+6]) + (b[i+7]) + (b[i+8]) + (b[i+9]) + (b[i+10]) + (b[i+11]) + (b[i+12]) + (b[i+13]) + (b[i+14]) + (b[i+15]) + (b[i+16]) + (b[i+17]) + (b[i+18]) + (b[i+19])
        created_date_total = b[i] + b[i+1] + (b[i+2]) + (b[i+3]) + (b[i+4]) + (b[i+5]) + (b[i+6]) + (b[i+7]) + (b[i+8]) + (b[i+9]) + (b[i+10]) + (b[i+11])
        article_name_total = (b[i]) + (b[i+1]) + (b[i+2]) + (b[i+3]) + (b[i+4]) + (b[i+5]) + (b[i+6]) + (b[i+7]) + (b[i+8]) + (b[i+9])
        url_total = (b[i]) + (b[i+1]) + (b[i+2]) + (b[i+3]) + (b[i+4]) + (b[i+5]) + (b[i+6]) + (b[i+7]) + (b[i+8]) + (b[i+9]) + (b[i+10]) + (b[i+11]) + (b[i+12]) + (b[i+13]) + (b[i+14]) + (b[i+15]) + (b[i+16]) + (b[i+17]) + (b[i+18]) + (b[i+19])
        post_id_total = (b[i]) + (b[i+1]) + (b[i+2]) + (b[i+3]) + (b[i+4]) + (b[i+5]) + (b[i+6]) + (b[i+7]) + (b[i+8]) + (b[i+9]) + (b[i+10]) + (b[i+11]) + (b[i+12]) + (b[i+13]) + (b[i+14]) + (b[i+15]) + (b[i+16]) + (b[i+17]) + (b[i+18]) + (b[i+19]) + (b[i+20])

        if blog_name_total == blog_name_sign:
            for j in range(i-1, 0, -1):
                if (b[j]) == '"':
                    entry_point = j+1
                    break

            blog_name_temp = (b[entry_point])
            for j in range(entry_point + 1, i):
                blog_name_temp += (b[j])

            if blog_name_temp == "en-us":
                blog_name.append("Asia Blog")
            elif blog_name_temp == "en-gb":
                blog_name.append("Thailand Blog")
            elif blog_name_temp == "ja":
                blog_name.append("USA Blog")


        if created_date_total == created_date_sign:
            created_date.append(((b[i+14])) + ((b[i+15])) + ((b[i+16])) + ((b[i+17])) + ((b[i+18])) + ((b[i+19])) + ((b[i+20])) + ((b[i+21])) + ((b[i+22])) + ((b[i+23])) + ((b[i+24])) + ((b[i+25])) + ((b[i+26])))

        if article_name_total == article_name_sign:

            article_name_temp = (b[i+12])
            for j in range (i + 13, len(b)):
                if (b[j]) == '"':
                    break

                article_name_temp += (b[j])

            article_name.append(article_name_temp)

        if url_total == url_sign:
            url_temp = (b[i+22])
            for j in range (i + 23, len(b)):
                if (b[j]) == '"':
                    break
                url_temp += (b[j])

            url.append(url_temp)

        if post_id_total == post_id_sign:
            posts_id.append(((b[i+21]) + (b[i+22]) + (b[i+23]) + (b[i+24]) + (b[i+25]) + (b[i+26]) + (b[i+27]) + (b[i+28]) + (b[i+29]) + (b[i+30]) + (b[i+31])))
            count += 1
    
    df_blog_name = pd.DataFrame(blog_name, columns = ["blog_name"])
    df_created_date = pd.DataFrame(created_date, columns = ["created_date"])
    df_article_name = pd.DataFrame(article_name, columns = ["article_name"])
    df_url = pd.DataFrame(url, columns = ["url"])
    df_post_id = pd.DataFrame(posts_id, columns = ["posts_id"])

    df_right = pd.concat([df_blog_name, df_url, df_created_date, df_article_name, df_post_id], axis=1, join='inner')    
        
    column_name = ['posts_id', 'Date', 'breakdown', 'newVisitorRawViews', 'exits', 'pageviewsMinusExits', 'exitsPerPageview', 'rawViews', 'pageBounces', 'pageTime', 'timePerPageview', 'standardViews', 'entrances', 'pageBounceRate']
    lst = []    
    for id in posts_id:
        response = hubspot.get(
                #'https://api.hubapi.com/analytics/v2/reports/blog-posts/' + id + '/sessions/daily?start=20210511&end=20210520' 
                'https://api.hubapi.com/analytics/v2/reports/blog-posts/' + id + '/sources/daily?start=20210414&end=20211231&f=organic&f=direct&f=email&f=referral&f=social'
            )
        dict_train = response.json()

        for key in dict_train.keys():
            for i in range(0, len(dict_train[key])):

                lst_of_lst = []
                lst_of_lst.append(id)
                lst_of_lst.append(key)

                for j in range(2, len(column_name)):

                    n = 0
                    current_length = len(dict_train[key][i].items())

                    for keys_keys, items in dict_train[key][i].items():
                        n += 1   
                        if (keys_keys == column_name[j]):
                            lst_of_lst.append(str(items))
                            break    
                        elif (n == current_length):
                            lst_of_lst.append("")

                lst.append(lst_of_lst)

    df_left = pd.DataFrame(lst, columns = column_name)  
    
    df_final = df_left.merge(df_right, on = 'posts_id', how = 'left')
    print(df_final)
    

def InstallAppAndCreateToken(config, port=3000):
    """
    Creates a simple local web app+server to authorize your app with a HubSpot hub.
    Returns the refresh and access token.
    """  
    from wsgiref import simple_server
    import webbrowser

    local_webapp = SimpleAuthCallbackApp()
    local_webserver = simple_server.make_server(host='localhost', port=port, app=local_webapp)

    redirect_uri = 'http://{}:{}/oauth-callback'.format('localhost', local_webserver.server_port)

    oauth = OAuth2Session(
        client_id=config['client_id'],
        scope=config['scopes'],
        redirect_uri=redirect_uri
    )

    auth_url, _ = oauth.authorization_url(config['auth_uri'])
    
    print('-- Authorizing your app via Browser --')
    print('If your browser does not open automatically, visit this URL:')
    print(auth_url)
    webbrowser.open(auth_url, new=1, autoraise=True)
    local_webserver.handle_request()

    # Https required by requests_oauthlib 
    auth_response = local_webapp.request_uri.replace('http','https')

    token = oauth.fetch_token(
        config['token_uri'],
        authorization_response=auth_response,
        # HubSpot requires you to include the ClientID and ClientSecret
        include_client_id=True,
        client_secret=config['client_secret']
    )
    return token

class SimpleAuthCallbackApp(object):
    """
    Used by our simple server to receive and 
    save the callback data authorization.
    """
    def __init__(self):
        self.request_uri = None
        self._success_message = (
            'All set! Your app is authorized.  ' + 
            'You can close this window now and go back where you started from.'
        )

    def __call__(self, environ, start_response):
        from wsgiref.util import request_uri
        
        start_response('200 OK', [('Content-type', 'text/plain')])
        self.request_uri = request_uri(environ)
        return [self._success_message.encode('utf-8')]

def SaveTokenToFile(token):
    """
    Saves the current token to file for use in future sessions.
    """
    with open('hstoken.pickle', 'wb') as tokenfile:
        pickle.dump(token, tokenfile)
        
if __name__ == '__main__':
    main()

import requests
import json
import sys
from bs4 import BeautifulSoup
import re

def make_playlist(name,auth_token,description=''):
    #makes the playlist and return playlist id
    create_playlist_url='https://api.spotify.com/v1/users/jobin9/playlists'
    playlist_properties=json.dumps({'name':f'{name}','public':'false','description':f'{description}'})
    response=requests.post(create_playlist_url,headers={'Authorization':f'Bearer {auth_token}','Content-Type':'application/json'},data=playlist_properties)
    if not response.status_code==201:
        print('Error',response.status_code)
        sys.exit()
        return str(response.status_code)
    else:
        print('Playlist ',name,' has been created')
        response=response.json()
        return response['id']

def get_songs(auth_token,artist):
    #searches for the songs and returns a list of song uris
    #the code is run for each artist
    #this is basically where the filtering happens
    songs=[]
    search_url='https://api.spotify.com/v1/search?'
    offset=0
    query=f'{search_url}q=artist:{artist}+NOT+year:2018-2020&type=track&offset={offset}&limit=50'
    response=requests.get(query,headers={'Authorization':f'Bearer {auth_token}'})
    response=response.json()
    if response['tracks']['total']<=2000:
        total=response['tracks']['total']
    else:
        total=2000
        print(artist,'CAPPED---------------------------------------')
    print('Total no of songs by ',artist,' is ',total)
    for i in response['tracks']['items']:
        songs.append(i['uri'])
    offset+=50
    while(offset<total):
        query=f'{search_url}q=artist:{artist}+NOT+year:2018-2020&type=track&offset={offset}&limit=50'
        response=requests.get(query,headers={'Authorization':f'Bearer {auth_token}'})
        if response.status_code==200:
            response=response.json()
            for i in response['tracks']['items']:
                songs.append(i['uri'])
            offset+=50
        else:
            print('Error',response.status_code)
            break
    if len(songs)==total:
        print('Songs by ',artist,' have been sucessfully compiled')
    else:
        print('Error in song compilation',artist)
        sys.exit()
    return songs

def add_songs_to_playlist(auth_token,playlist_id,songs):
    #adds the songs to the generated playlist
    #songs is the list of songs by an artist
    add_items_url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?'
    pos=len(songs) if len(songs)<50 else 50
    i=0
    while i < len(songs):
        print('Adding ',pos-i,' songs')
        song_items=json.dumps({"uris":songs[i:pos]})
        pos+=50
        if pos>len(songs):
            pos=len(songs)
        i+=50
        response=requests.post(add_items_url,headers={'Authorization':f'Bearer {auth_token}','Content-Type':'application/json'},data=song_items)
        if not response.status_code==201:
            print('Error',response.status_code)
            sys.exit()
        print('Added ',pos,' songs')
    print('Songs have been added successfully')

def driver():
    #this is the main driver
    #paste authentication token below
    auth_token=''

    artists=['rihanna','katy+perry','flo+rida','onerepublic','lady+gaga','the+black+eyed+peas','beyonce','britney+spears','taylor+swift','p!nk','kelly+clarkson','kesha','jason+derulo','taio+cruz','b.o.b','bruno+mars','usher','pitbull','adele','maroon+5','david+guetta','nicki+minaj','carly+rae+jepsen','justin+timberlake','imagine+dragons','selena+gomez','iggy+azalea','sam+smith','ariana+grande','lorde','pharrell+williams','the+weeknd','ed+sheeran','ellie+goulding','robin+schulz','justin+bieber','twenty+one+pilots','avicii','the+chainsmokers','drake','shawn+mendes','alessia+cara','5+seconds+of+summer','backstreet+boys','bastille','charlie+puth','calvin+harris','coldplay','john+legend','jessie+j','jp+cooper','mumford+&+sons','one+direction','the+script','sia','eminem','alicia+keys','madonna','green+day','michael+jackson','miley+cyrus','shakira','akon','celine dion','jennifer+lopez','50+cent','jay-z','linkin+park','daft-punk','lmfao']

    c=0
    while c+10<=len(artists):
        name=f'Old Songs{c+10}'
        description='Songs that make me feel nostalgic'
        playlist_id=make_playlist(name,auth_token,description)
        i=artists[c:c+10]
        for j in i:
            songs=get_songs(auth_token,j)
            add_songs_to_playlist(auth_token,playlist_id,songs)
        c+=10

    print('Done')


driver()

import requests
import json
import sys

def make_playlist(name,auth_token,description=''):
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

def get_songs(auth_token,year):
    songs=[]
    search_url='https://api.spotify.com/v1/search?'
    offset=0
    query=f'{search_url}q=year:{year}+genre:indie&type=track&offset={offset}&limit=50'
    response=requests.get(query,headers={'Authorization':f'Bearer {auth_token}'})
    response=response.json()
    total=response['tracks']['total'] if response['tracks']['total']<=2000 else 2000
    print('Total no of songs is ',total)
    for i in response['tracks']['items']:
        songs.append(i['uri'])
    offset+=50
    while(offset<total):
        query=f'{search_url}q=year:{year}+genre:indie&type=track&offset={offset}&limit=50'
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
        print('Songs have been sucessfully compiled')
    else:
        print('Error in song compilation')
        sys.exit()
    return songs

def add_songs_to_playlist(auth_token,playlist_id,songs):
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
    for year in [1990,1994,1998,2002,2006,2010,2014,2018]:
        name=f'Indie {year}-{year+3}'
        description=''
        #paste authentication token below
        auth_token=''
        playlist_id=make_playlist(name,auth_token,description)
        for i in range(year,year+4):
            print('adding songs from ',i)
            songs=get_songs(auth_token,str(i))
            add_songs_to_playlist(auth_token,playlist_id,songs)
    print('Done')

driver()

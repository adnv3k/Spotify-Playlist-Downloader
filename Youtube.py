"""
gets class from spotifyconnect.py 
implementing that returns dictionary of tracks in a given playlist from playlistname
#####
calls youtube api
uses search() to query "song title + artist" 
returns youtube links 
"""
import os
os.chdir('D:\\Files\\Documents\\Programming\\Projects\\Spotify Playlist Downloader')
from googleapiclient.discovery import build
from SpotifyWrapper import SpotifyConnect
from pytube import YouTube

#call api get auth
key = os.environ['google']
youtube = build('youtube','v3',developerKey=key)

def search(query, maxResults=10):
    """
    Input: query: str of search items, maxResults: int of number of results to return
    Output: search_response: dict of query results
    """
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=maxResults
        ).execute()
    return search_response

def get_video_links(search_response):
    """
    Input: search_response: dict of query of results
    Output: dict of youtube links {'link': 'title}
    """
    links = {}
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            links['https://www.youtube.com/watch?v=' + search_result['id']['videoId']] = search_result['snippet']['title']
    return links

#region potentially useful formats
# videos = []
# channels = []
# playlists = []
# videoids = []

# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.
# for search_result in search_response.get('items', []):
#     if search_result['id']['kind'] == 'youtube#video':
#         videoids.append(search_result['id']['videoId']) 
        # videos.append('%s (%s)' % (search_result['snippet']['title'],
        #                             search_result['id']['videoId']))
    # elif search_result['id']['kind'] == 'youtube#channel':
    #     channels.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['channelId']))
    # elif search_result['id']['kind'] == 'youtube#playlist':
    #     playlists.append('%s (%s)' % (search_result['snippet']['title'],
    #                                 search_result['id']['playlistId']))

# print ('Videos:\n', '\n'.join(videos), '\n')
# print ('Channels:\n', '\n'.join(channels), '\n')
# print ('Playlists:\n', '\n'.join(playlists), '\n')
#endregion

#generate tracks for default account
account = SpotifyConnect()
tracks = account.get_playlist_tracks()

# example return
# tracks = {"I'm Not Sorry": {'Artist': 'DEAN', 'Date Added': '2021-06-17T23:30:33Z'}, 'Rendezvous': {'Artist': 'Sik-K', 'Date Added': '2021-06-18T00:20:50Z'}}

#get links from youtube api
video_links = {}
for title in [*tracks]:
    #gets dict of maxResults of video links with the search query 'title + artist' 
    video_links[title] = get_video_links(search(title+tracks[title]['Artist'], maxResults=1))

print(video_links)
# for title in [*video_links]:
#     print('videolinkkeys',title)
#     print('TITLE KEYS',[*video_links[title]][0])


#now with dict of videolinks where keys are titles
# download
os.chdir('D:\\Files\\Documents\\Programming\\Projects\\Spotify Playlist Downloader\Downloads')
for title in [*video_links]:
    print('\nDownloading ' + title + ' from ' + [*video_links[title]][0] + '\n')
    download = YouTube([*video_links[title]][0])
    download.streams.all
    download.streams.first().download()
    


# account.close()
youtube.close()





























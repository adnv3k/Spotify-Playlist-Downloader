import spotipy
from spotipy.oauth2 import *
import pandas as pd
import os

class SpotifyConnect(object):
    def __init__(self, id=os.environ['spotify'], 
                        secret = os.environ['openspotify'], 
                        redirect_uri='https://www.google.com/', 
                        scope ='playlist-read-private'):
        super().__init__()
        self.id = id
        self.secret = secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.sp = self.get_auth_token()

    def get_auth_token(self):
        """
        Retrieves an authorization token for API calls. 
        Output: sp: spotipy object
        """
        #calls to api and enables interaction with api that dont require auth
        # sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=self.id, 

        #allows requests that require auth (like getting data about private playlists)
        #include scope to request specific kind of authorization. list of scope arg online
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.id, 
                                                        client_secret=self.secret, 
                                                        redirect_uri=self.redirect_uri,
                                                        scope=self.scope))
        return sp

    def find_playlist_id(self, playlist_name):
        """
        Returns ID of given playlist name. Raises error if playlist not in user list.
        Input: sp: spotipy object, name_of_playlist: str
        Output: name_of_playlist ID: str
        """
        playlists = self.get_playlists()
        #region description
        #returns a dictionary where playlists['items'] = a list of dictionaries of a playlist
        #these dictionaries have the keys 'name' for playlist name and 'id' for playlist id
        #iterate thru the list of dictionaries and store their names and associated id
        #endregion

        for dictionary in playlists['items']:
            if dictionary['name'] == playlist_name:
                return dictionary['id']
        raise "Playlist not in user playlists."

    def get_playlists(self, limit=100):
        """
        Returns all dict of the most recent 100 playlists from current user's playlists
        Input: (optional) limit: int
        Output: playlists: dict {playlistname : {'number of tracks': number of tracks in playlist, 'id' : playlist id}}
        """
        playlists = {}
        user_playlists = self.sp.current_user_playlists(limit=limit)
        for dictionary in user_playlists['items']:
            playlists[dictionary['name']] = {'number of tracks' : dictionary['tracks']['total'], 'id' : dictionary['id']}
        return playlists

    def get_playlist_tracks(self, playlist_name='Download'):
        """
        Returns tracks given playlist name
        Input: sp: spotipy object, playlist_name: str
        Output: tracks: dict of tracks in playlist_id
                tracks = {track title : {'artist': track artist, 'Date Added' : year-month-dayTHH:MM:SS}}
        """

        if playlist_name == 'Download':
            playlist_id = '6CFFSU2aqZvRA9VB7z04Y0'
        else:
            playlists = self.get_playlists()
            try:
                playlist_id = playlists[playlist_name]['id']
            except:
                raise "Playlist not in user playlists."

        self.playlist_tracks = self.sp.playlist_items(playlist_id=playlist_id)
        #region description
        #returns a dictionary where playlist_tracks['items'] = a list of dictionarys of a track
        #these dictionaries includes the entry:
        # 'added_at' : "2021-06-17T23:30:33Z"
        #and playlist_tracks['items']['track'] has a dictionary of track information
        # playlist_tracks['items']['track']['name'] : "I'm Not Sorry"
        # playlist_tracks['items']['track']['artists'] : playlist_tracks['items']['track']['artists'][0]['name'] <== artist name
        #endregion
        
        self.tracks = {}
        self.playlist_tracks = self.playlist_tracks['items']
        for dictionary in self.playlist_tracks:
            self.tracks[dictionary['track']['name']] = {'Artist' : dictionary['track']['artists'][0]['name'], 'Date Added' : dictionary['added_at']}
        return self.tracks
#TODO def get_updated_playlist_tracks():

    def close(self):
        self.sp.close()

# artist_name = ['list of artist names']
# track_name = ['list of track names']
# track_id = ['list of track ids']
# playlist_data = pd.DataFrame({
#         'artist_name' : artist_name,
#         'track_name' : track_name,
#         'track_id' : track_id})
import os
from tqdm import tqdm
import sys
import time
import toml


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from deezer import Client

import mutagen
from mutagen.flac import FLAC

def main():
    # Spotify API Credentials
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    client_id = config['SpotifyAPI']['client_id']
    client_secret = config['SpotifyAPI']['client_secret']

    # Check if client_id and client_secret are provided
    if not client_id or not client_secret:
        print("Error: client_id and/or client_secret not found in config file.")
        input("Press any key to exit...")
        sys.exit()

    # Check if system arguments are provided
    if len(sys.argv) < 2:
        print("Error: Please provide a folder as a command line argument. You can do this by dragging and dropping a folder onto the python file.")
        input("Press any key to exit...")
        sys.exit()
    else:
        folder = sys.argv[1]

    # load in all FLAC files from folder
    flac_files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".flac")]
    if flac_files == []:
        print("No FLAC files found in folder")
        input("Press any key to exit...")
        sys.exit()

    # Setup Spotify API using Spotipy
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))
    dz = Client()

    # Ask for album or track link
    link = input("Enter album or track link (Spotify or Deezer): ")
    
    if "spotify" in link:
        # Retrieve Spotify metadata
        try:
            if 'album' in link:
                album_metadata = sp.album(link)
            if 'track' in link:
                track_metadata = sp.track(link)
        except spotipy.client.SpotifyException as e:
            print(f"Error: {e}")
            input("Press any key to exit...")
            sys.exit()

        if 'album' in link:
            album_metadata = sp.album(link)
            album_name = album_metadata['name']
            tracks_metadata = album_metadata['tracks']['items']
        else:
            track_metadata = sp.track(link)
            album_name = track_metadata['album']['name']
            tracks_metadata = [track_metadata]
        album_artists = [artist['name'] for artist in album_metadata['artists']]
        release_date = album_metadata['release_date']

        print(f"\033[1;32;40mThe following metadata will be applied:\033[0m")
        print(f"\033[1;33;40mAlbum name:  \033[0m {album_name}")
        print(f"\033[1;33;40mAlbum artist:\033[0m {', '.join(album_artists)}")
        print(f"\033[1;33;40mRelease date:\033[0m {release_date}")
    
    elif "deezer" in link:
        # Retrieve Deezer metadata
        if "http" in link:
            album_id = link.split("/")[-1]
        else:
            album_id = link

        album = dz.get_album(album_id)
        album_name = album.title
        album_artists = ', '.join(str(x) for x in list([contributor.name for contributor in album.contributors]))
        release_date = album.release_date
        tracks_metadata = album.get_tracks()
        print(f"\033[1;32;40mThe following metadata will be applied:\033[0m")
        print(f"\033[1;33;40mAlbum name:  \033[0m {album_name}")
        print(f"\033[1;33;40mAlbum artist:\033[0m {album_artists}")
        print(f"\033[1;33;40mRelease date:\033[0m {release_date}")
    else:
        print("Invalid link. Please provide a valid Spotify or Deezer link.")
        input("Press any key to exit...")
        sys.exit()
            # Check config file if user should be asked for confirmation
    if config['Options']['alwaysAskForConformation']:
        confirmation = input("Do you want to continue? (Y/n)\n") or "y"
    else:
        confirmation = "y"
    start_time = time.time()
    if confirmation.lower() == "y":
        if "spotify" in link:
            for track_metadata, flac_file in tqdm(zip(tracks_metadata, flac_files), total=len(tracks_metadata), desc="Processing files"):
                audio = mutagen.flac.FLAC(flac_file)
                audio['album'] = album_name
                audio["ARTIST"] = [artist['name'] for artist in track_metadata['artists']]
                audio['title'] = track_metadata['name']
                audio["ALBUMARTIST"] = album_artists
                audio['date'] = release_date
                audio.save()
                
        elif "deezer" in link:
            for track, flac_file in tqdm(zip(tracks_metadata, flac_files), total=len(tracks_metadata), desc="Processing files"):
                audio = mutagen.flac.FLAC(flac_file)
                audio['album'] = album_name
                audio["ARTIST"] = [contributor.name for contributor in track.contributors]
                audio['title'] = track.title
                audio["ALBUMARTIST"] = album_artists
                audio['date'] = str(release_date)
                audio.save()
    end_time = time.time()
    print(f"Metadata successfully applied!\nTotal time taken: {end_time - start_time:.2f} seconds")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
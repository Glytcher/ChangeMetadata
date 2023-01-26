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
    
    clientId = config['SpotifyAPI']['clientId']
    clientSecret = config['SpotifyAPI']['clientSecret']

    # Check if system arguments are provided
    if len(sys.argv) < 2:
        print("Error: Please provide a folder as a command line argument. You can do this by dragging and dropping a folder onto the python file.")
        input("Press Enter key to exit...")
        sys.exit()
    else:
        folder = sys.argv[1]

    # Load in all FLAC files from folder
    flacFiles = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".flac")]
    if flacFiles == []:
        print("No FLAC files found in folder")
        input("Press Enter key to exit...")
        sys.exit()

    # Setup Spotify API using Spotipy and Deezer API client using Deezer-Python
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(clientId, clientSecret))
    dz = Client()

    # Ask for album or track link
    link = input("Enter album or track link (Spotify or Deezer): ")
    
    # Check if link is valid and check for Spotify or Deezer
    if "spotify" in link:
        # Check if clientId and clientSecret are provided
        if not clientId or not clientSecret:
            print("Error: Spotify clientId and/or clientSecret empty")
            input("Press Enter key to exit...")
            sys.exit()

        # Retrieve Spotify metadata
        try:
            if 'album' in link:
                albumMetadata = sp.album(link)
            if 'track' in link:
                trackMetadata = sp.track(link)
        except spotipy.client.SpotifyException as e:
            print(f"Error: {e}")
            input("Press any key to exit...")
            sys.exit()
        
        if 'album' in link:
            albumMetadata = sp.album(link)
            albumName = albumMetadata['name']
            tracksMetadata = albumMetadata['tracks']['items']
        else:
            trackMetadata = sp.track(link)
            albumMetadata = sp.album(trackMetadata['album']['id'])
            albumName = trackMetadata['album']['name']
            tracksMetadata = [trackMetadata]
        
        totalTracks = str(albumMetadata['total_tracks'])
        albumArtists = [artist['name'] for artist in albumMetadata['artists']]
        releaseDate = albumMetadata['release_date']
        
        print(f"\033[1;32;40mThe following metadata will be applied:\033[0m")
        print(f"\033[1;33;40mAlbum name:  \033[0m {albumName}")
        print(f"\033[1;33;40mAlbum artist(s):\033[0m {', '.join(albumArtists)}")
        print(f"\033[1;33;40mRelease date:\033[0m {releaseDate}")
    
    elif "deezer" in link:
        # Get Deezer album ID
        if "http" in link:
            albumId = link.split("/")[-1]
        else:
            albumId = link

        album = dz.get_album(albumId)
        albumName = album.title
        albumArtists = ', '.join(str(x) for x in list([contributor.name for contributor in album.contributors]))
        totalTracks = str(album.nb_tracks)
        releaseDate = str(album.release_date)
        tracksMetadata = album.get_tracks()

        print(f"\033[1;32;40mThe following metadata will be applied:\033[0m")
        print(f"\033[1;33;40mAlbum name:  \033[0m {albumName}")
        print(f"\033[1;33;40mAlbum artist(s):\033[0m {albumArtists}")
        print(f"\033[1;33;40mRelease date:\033[0m {releaseDate}")
    else:
        print("Invalid link. Please provide a valid Spotify or Deezer link.")
        input("Press Enter to exit...")
        sys.exit()

    # Check total tracks and FLAC files in folder to check if they match
    if len(tracksMetadata) != len(flacFiles):
        print(f"\033[91mNote:\033[0m         Total tracks in given album ({len(tracksMetadata)}) does not match total FLAC files in folder ({len(flacFiles)})")

    # Check config file if user should be asked for confirmation
    if config['Options']['alwaysAskForConformation']:
        confirmation = input("Do you want to continue? (Y/n)\n") or "y"
    else:
        confirmation = "y"

    # Start timer for processing time
    startTime = time.time()
    
    if confirmation.lower() == "y":
        if "spotify" in link:
            for trackMetadata, flac_file in tqdm(zip(tracksMetadata, flacFiles), total=len(tracksMetadata), desc="Processing files"):
                audio = mutagen.flac.FLAC(flac_file)
                audio['album'] = albumName
                audio["ARTIST"] = [artist['name'] for artist in trackMetadata['artists']]
                audio['title'] = trackMetadata['name']
                audio["ALBUMARTIST"] = albumArtists
                audio['date'] = releaseDate
                audio['tracktotal'] = totalTracks
                audio['discnumber'] = str(trackMetadata['disc_number'])
                audio['tracknumber'] = str(trackMetadata['track_number'])
                audio.save()
        elif "deezer" in link:
            for track, flac_file in tqdm(zip(tracksMetadata, flacFiles), total=len(tracksMetadata), desc="Processing files"):
                audio = mutagen.flac.FLAC(flac_file)
                audio['album'] = albumName
                audio["ARTIST"] = [contributor.name for contributor in track.contributors]
                audio['title'] = track.title
                audio["ALBUMARTIST"] = albumArtists
                audio['date'] = releaseDate
                audio['tracktotal'] = totalTracks
                audio['discnumber'] = str(track.disk_number)
                audio['tracknumber'] = str(track.track_position)
                audio.save()
    else:
        print("Aborted")
        input("Press Enter to exit...")
        sys.exit()
        
    # End timer for processing time
    endTime = time.time()
    
    print(f"Metadata successfully applied!\nTotal time taken: {endTime - startTime:.2f} seconds")
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
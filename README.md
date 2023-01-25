# Apply Spotify or Deezer metadata to FLAC files

This script allows you to add Spotify or Deezer metadata to your FLAC files using Spotify/Deezer API. Useful for when you use both a local music player and Spotify or Deezer and want to keep your metadata consistent for use with Last.fm scrobbling (E.g. with Foobar2000 and [foo_scrobble](https://github.com/gix/foo_scrobble)). Using the metadata from Spotify or Deezer would fix annoying issues like the track artist or song title being different in Spotify or Deezer and your local music player, resulting in inaccurate scrobbles on Last.fm.

This script will add the following metadata to the FLAC files taken from Spotify or Deezer:

- Album & track artist(s)
- Album title
- Track title
- Release date
- Total number of tracks
- Track number
- Disc number

## Requirements

- Python 3.9+
- [Spotipy](https://pypi.org/project/spotipy/)
- [toml](https://pypi.org/project/toml/)
- [tqdm](https://pypi.org/project/tqdm/)
- [Deezer-python](https://pypi.org/project/deezer-python/)
- [Mutagen](https://pypi.org/project/mutagen/)

**Optional:**

- If you want to use Spotify, you need Spotify API credentials (client ID and client secret, see [here](https://developer.spotify.com/dashboard/applications) for more information)

## Installation and usage

1. Clone or download the repository and navigate to the folder using the command line
2. Install the dependencies by running `pip install -r requirements.txt`
3. Create a `config.toml` file in the same folder as the `ChangeMetadata.py` file and add your Spotify API credentials to it if needed. See the Configuration section below for more information.
4. Run the script by dragging a folder containing FLAC files onto the script file or by providing the folder as a command line argument, e.g. `python ChangeMetadata.py "path/to/folder"`.
5. Provide the Spotify or Deezer link/ID of the album or track when prompted
6. The script will display a summary of the metadata that will be added and prompt for confirmation before applying.

## Configuration

### config.toml template

```toml
[SpotifyAPI]
client_id = ""      # Your client ID taken form the Spotify Developer Dashboard
client_secret = ""  # Your client secret taken from the Spotify Developer Dashboard

[Options]
alwaysAskForConformation = true # If set to true, the program will always ask for confirmation before applying the metadata changes
```

You can configure the script by editing the `config.toml` file. The following options are available:

- `alwaysAskForConfirmation`: If set to true, the script will always prompt for confirmation before applying the metadata. If set to false, the script will apply the metadata without prompting for confirmation.

## Notes

- Only tested on Windows with Python 3.9.5

## Todo

- [x] Add support for Deezer
- [x] Add disc metadata
- [ ] Make the config file optional, since you dont need credentials for Deezer
- [ ] Handle extended/alternative versions of albums not available on Spotify or Deezer

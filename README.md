# Apply Spotify/Deezer metadata to FLAC files

This script allows you to add Spotify/Deezer metadata to your FLAC files using Spotify/Deezer API. Useful for when you use both Foobar2000 and Spotify/Deezer and want to keep your metadata consistent for use with last.fm scrobbling. The script will add the following metadata to the FLAC files taken from Spotify/Deezer:

- Album & track artist(s)
- Album title
- Track title
- Release date
- Total tracks
- Track number
- Disc number

## Requirements

- Python 3.9+
- [Spotipy](https://pypi.org/project/spotipy/)
- [Deezer-python](https://pypi.org/project/deezer-python/)
- [Mutagen](https://pypi.org/project/mutagen/)
- Spotify API credentials (client ID and client secret, see [here](https://developer.spotify.com/dashboard/applications) for more information)

## Usage

1. Clone the repository and navigate to the folder
2. Install the dependencies by running `pip install -r requirements.txt`
3. Create a `config.toml` file next to the main .py file and add your Spotify API credentials to it. See the Configuration section below for more information.
4. Run the script by providing the folder containing the FLAC files as a command line argument, e.g. `python ChangeMetadata.py "path/to/folder"`. This can also be done by dragging the folder onto the script file.
5. Provide the Spotify link of the album when prompted
6. The script will display the metadata that will be added and prompt for confirmation before applying

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
- [ ] Handle extended/alternative versions of albums not available on Spotify/Deezer

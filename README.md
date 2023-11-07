# moreloja-mpd-scrobbler

This program connects to mpd and queries the currentsong every second.
When the song changes the data about the played song is saved in a mongodb document in a format that [Moreloja](https://github.com/Moreloja/Moreloja) can use.

## Usage

### Optional venv

Use venv if you want:

``` bash
python -m venv venv
source venv/bin/activate
```

### Requirements

Install requirements.

``` bash
pip install -r requirements.txt
```

### Configuration

``` bash
export MONGO_HOST=localhost
export MONGO_PORT=27017
export MONGO_DB_NAME=moreloja
```

### Start

``` bash
python ./src/main.py
```

## Example document

``` json
{
    _id: ObjectId('653bbdb70c0dce126422b181'),
    Artist: 'Aimer',
    artistsort: 'Aimer',
    albumartist: 'Aimer',
    albumartistsort: 'Aimer',
    timestamp: ISODate('2023-10-27T13:37:54.500Z'),
    timestamp_end: ISODate('2023-10-27T13:40:07.670Z'),
    Album: 'SPARK‐AGAIN',
    Name: 'SPARK‐AGAIN',
    label: 'SME Records',
    Provider_musicbrainzalbum: '8d07bd90-4985-42c6-9600-f176962e972a',
    Provider_musicbrainzalbumartist: '9388cee2-7d57-4598-905f-106019b267d3',
    Provider_musicbrainzartist: '9388cee2-7d57-4598-905f-106019b267d3',
    Provider_musicbrainzreleasegroup: '082e4943-6ebf-4abe-ae97-018518555055',
    Provider_musicbrainztrack: 'f5e75761-bbc3-4aa7-86b5-4a69f9ed9b4e',
    musicbrainz_workid: 'aab77019-7f5b-4ecc-9e6f-f6753ee7ac08',
    ServerVersion: '0.23.5',
    date: '2020-07-04',
    originaldate: '2020-07-04',
    Year: 2020,
    disc: [
        '1',
        '1'
    ],
    track: [
        '1',
        '1'
    ],
    genre: 'J-Pop',
    playback_position_seconds: 243.994,
    run_time: 244.160,
    playback_info_schema_version: 2
}
```

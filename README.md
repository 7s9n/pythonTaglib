# **pytag**

pytag is a [Python](http://www.python.org) audio tagging library. It is cross-platform, and is very simple to use yet fully featured:

- [supports more than a dozen file formats](http://taglib.github.io) including mp3, flac, ogg, wma, and mp4,
- support arbitrary, non-standard tag names,

pytag is a very thin wrapper (≈366 lines of [code](pytag/__init__.py)) around the fast and rock-solid [TagLib](http://taglib.github.io) C++ library.

## Usage

```python
import pytag
>>> song = pytag.File('/path/to/my/file.mp3')
>>> tag = song.tags
>>> tag.title
Hussein Sarea
>>> tag.title = 'New title'
>>> tag.title
New title
>>> song.save()
>>> song.close()
```

## Another example

```python
import pytag
path = Path('/path/to/my/file.mp3')

with pytag.File(path) as tfile:
    tags = tfile[0]
    properties = tfile[1]
    
    # delete a specific tag
    del tags.title

    # edit a tag
    tags.artist = 'new artist'

    # you can also get audio properties information
    print(properties.length)
    print(properties.minutes)
    print(properties.seconds)
    print(properties.bitrate)
    print(properties.samplerate)
    print(properties.channels)
```

### Manual Compilation: General

You can download or checkout the sources and compile manually:

```python
    python setup.py build
    python setup.py test  # optional, run unit tests
    python setup.py install
```

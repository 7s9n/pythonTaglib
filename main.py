from pathlib import Path
import pytag

path = Path(__file__).parent.parent / 'Desktop' / 'music' / 'chilly.mp3'

with pytag.File(path) as tfile:
    tags = tfile[0]
    properties = tfile[1]
    
    # delete a specific tag

    del tags.title
# with pytag.File(path, pytag.FileType.MPEG) as tag:
#     print(tag.album)
# tags = pytag.File(path, pytag.FileType.MPEG).tags
# del tags.title
# print(tags.comment)
# tags.save()
# del file.tags['ALBUM']

# file.save()


# print(tags.artist)

# tags = file.tags
# file.close()

# properties = file.audio_properties

# print(properties.minutes)
# print(properties.seconds)
# print(properties.bitrate)
# print(properties.samplerate)
# print(properties.channels)
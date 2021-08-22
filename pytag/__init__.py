from ctypes import (
    cdll,
    c_bool,
    c_int,
    c_char_p,
    c_uint,
)
from sys import platform
from pathlib import Path
from enum import IntEnum
from typing import Optional, Tuple, Union
from ._utils import (
    to_byte_str,
    to_python_str,
    to_int,
    wrap_function,
    _FilePtr,
    _TagPtr,
    _AudioPropertiesPtr,
)

__lib_files = {
    'linux':'libtag_c.so',
    'win32':'libtag_c.dll',
}
__lib = __lib_files.get(platform)
__file_path = Path(__file__).parent / 'lib'
__main_path = Path(__file__).parent.parent

if (__file_path / __lib).exists():
    TAGLIB_PATH = __file_path / __lib
elif (__main_path  / __lib).exists():
    TAGLIB_PATH = __main_path / __lib
elif (__main_path / 'lib' / __lib).exists():
    TAGLIB_PATH = __main_path / 'lib' / __lib
else:
    raise FileNotFoundError(
        """Cannot find "{}" in this search path: __file__ folder: {}"""
        .format(__lib, str(__file_path))
    )

_tl = cdll.LoadLibrary(str(TAGLIB_PATH))

class FileType(IntEnum):
    MPEG = 0
    OggVorbis = 1
    FLAC = 2
    MPC = 3
    OggFlac = 4
    WavPack = 5
    Speex = 6
    TrueAudio = 7
    MP4 = 8
    ASF = 9

class ID3v2Encoding(IntEnum):
    Latin1 = 0
    UTF16 = 1
    UTF16BE = 2
    UTF8 = 3

class AudioProperties:
    """TagLib::AudioProperties wrapper"""
    __length = wrap_function(_tl,'taglib_audioproperties_length', [_AudioPropertiesPtr], c_int)
    __bitrate = wrap_function(_tl,'taglib_audioproperties_bitrate', [_AudioPropertiesPtr], c_int)
    __samplerate = wrap_function(_tl, 'taglib_audioproperties_samplerate', [_AudioPropertiesPtr], c_int)
    __channels = wrap_function(_tl, 'taglib_audioproperties_channels', [_AudioPropertiesPtr], c_int)

    def __init__(self, file: 'File') -> None:
        if isinstance(file, File):
            if not file._file:
                raise ValueError('You cannot get audio properties from closed file.')
            self._audio_properties = wrap_function(_tl,'taglib_file_audioproperties', [_FilePtr],_AudioPropertiesPtr)(file._file)
        else:
            raise TypeError("{} must be an instance of File not {}".format(file, file.__class__.__qualname__))

    @property
    def seconds(self)-> int:
        return self.__length(self._audio_properties) % 60
    
    @property
    def minutes(self)-> int:
        return (self.__length(self._audio_properties) - self.seconds) // 60
    
    @property
    def length(self)-> int:
        """
        Returns the length of the file in seconds.
        """
        return self.__length(self._audio_properties)
    
    @property
    def bitrate(self)-> int:
        """
        Returns the bitrate of the file in kb/s.
        """
        return self.__bitrate(self._audio_properties)

    @property
    def samplerate(self)-> int:
        """
        Returns the sample rate of the file in Hz.
        """
        return self.__samplerate(self._audio_properties)

    @property
    def channels(self)-> int:
        """
        Returns the number of channels in the audio stream.
        """
        return self.__channels(self._audio_properties)

class Tag:
    """TagLib::Tag wrapper"""
    __title = wrap_function(_tl, 'taglib_tag_title', [_TagPtr], c_char_p)
    __artist = wrap_function(_tl, 'taglib_tag_artist', [_TagPtr], c_char_p)
    __album = wrap_function(_tl, 'taglib_tag_album', [_TagPtr], c_char_p)
    __comment = wrap_function(_tl, 'taglib_tag_comment', [_TagPtr], c_char_p)
    __genre = wrap_function(_tl, 'taglib_tag_genre', [_TagPtr], c_char_p)
    __year = wrap_function(_tl, 'taglib_tag_year', [_TagPtr], c_uint)
    __track = wrap_function(_tl, 'taglib_tag_track', [_TagPtr], c_uint)
    __stitle = wrap_function(_tl, 'taglib_tag_set_title', [_TagPtr, c_char_p])
    __sartist = wrap_function(_tl, 'taglib_tag_set_artist', [_TagPtr, c_char_p])
    __salbum = wrap_function(_tl, 'taglib_tag_set_album', [_TagPtr, c_char_p])
    __scomment = wrap_function(_tl, 'taglib_tag_set_comment', [_TagPtr, c_char_p])
    __sgenre = wrap_function(_tl, 'taglib_tag_set_genre', [_TagPtr, c_char_p])
    __syear = wrap_function(_tl, 'taglib_tag_set_year', [_TagPtr, c_uint])
    __strack = wrap_function(_tl, 'taglib_tag_set_track', [_TagPtr, c_uint])

    def __init__(self, file: 'File')-> None:
        if isinstance(file, File):
            if not file._file:
                raise ValueError('You cannot get tags from closed file.')
            self._tag = wrap_function(_tl, 'taglib_file_tag', [_FilePtr], _TagPtr)(file._file)
            self.__file = file
        else:
            raise TypeError("{} must be an instance of File not {}".format(file, file.__class__.__qualname__))

    @property
    def title(self)-> str:
        """
        Returns a string with this tag's title.
        By default this string should be UTF8 encoded
        """
        return to_python_str(self.__title(self._tag))
    
    @title.setter
    def title(self, value: str)-> None:
        """
        Sets the tag's title.
        NOTE: By default this string should be UTF8 encoded.
        """
        self.__stitle(self._tag, to_byte_str(value))

    @title.deleter
    def title(self):
        self.title = ''

    @property
    def artist(self)-> str:
        """
        Returns a string with this tag's artist.
        By default this string should be UTF8 encoded
        """
        return to_python_str(self.__artist(self._tag))

    @artist.setter
    def artist(self, value: str)-> None:
        """
        Sets the tag's artist.
        NOTE: By default this string should be UTF8 encoded.
        """
        self.__sartist(self._tag, to_byte_str(value))
    
    @artist.deleter
    def artist(self):
        self.artist = ''

    @property
    def album(self)-> str:
        """
        Returns a string with this tag's album name.
        By default this string should be UTF8 encoded
        """
        return to_python_str(self.__album(self._tag))

    @album.setter
    def album(self, value: str)-> None:
        """
        Sets the tag's album.
        NOTE: By default this string should be UTF8 encoded.
        """
        self.__salbum(self._tag, to_byte_str(value))

    @album.deleter
    def album(self):
        self.album = ''
    
    @property
    def comment(self)-> str:
        """
        Returns a string with this tag's comment.
        By default this string should be UTF8 encoded
        """
        return to_python_str(self.__comment(self._tag))
    
    @comment.setter
    def comment(self, value: str)-> None:
        """
        Sets the tag's comment.
        NOTE: By default this string should be UTF8 encoded.
        """
        self.__scomment(self._tag, to_byte_str(value))

    @comment.deleter
    def comment(self):
        self.comment = ''

    @property
    def genre(self)-> str:
        """
        Returns a string with this tag's genre.
        By default this string should be UTF8 encoded
        """
        return to_python_str(self.__genre(self._tag))
    
    @genre.setter
    def genre(self, value: int)-> None:
        """
        Sets the tag's genre.
        NOTE: By default this string should be UTF8 encoded.
        """
        self.__sgenre(self._tag, to_byte_str(value))

    @genre.deleter
    def genre(self):
        self.genre = ''

    @property
    def year(self)-> int:
        """
        Returns the tag's year or 0 if year is not set.
        """
        return self.__year(self._tag)

    @year.setter
    def year(self, value: int)-> None:
        """
        Sets the tag's year.  0 indicates that this field should be cleared.
        """
        self.__syear(self._tag, to_int(value))

    @year.deleter
    def year(self):
        self.year = 0

    @property
    def track(self)-> int:
        """
        Returns the tag's track number or 0 if track number is not set.
        """
        return self.__track(self._tag)

    @track.setter
    def track(self, value: int)-> None:
        """
        Sets the tag's track number.  0 indicates that this field should be cleared.
        """
        self.__strack(self._tag, to_int(value))
    
    @track.deleter
    def track(self):
        self.track = 0

    def save(self)-> None:
        self.__file.save()
    
class File:
    """TagLib::File wrapper"""
    __is_valid = wrap_function(_tl, 'taglib_file_is_valid', [_FilePtr], c_bool)
    __save = wrap_function(_tl, 'taglib_file_save', [_FilePtr], c_bool)
    __close = wrap_function(_tl,'taglib_file_free', [_FilePtr])

    def __init__(self, filename: Union[str, Path], filetype: Optional[FileType]= None) -> None:
        """
        Creates a TagLib file based on filename.
        TagLib will try to guess the file type if it's not provided,
        but if filetype is set Rather than attempting to guess the type, 
        it will use the one specified by filetype.
        raises OSError if the file type cannot be determined or the file cannot be opened.
        """
        if filetype:
            self._file = wrap_function('taglib_file_new_type', [c_char_p, c_int], _FilePtr)(
                to_byte_str(str(filename)),
                to_int(filetype),
            )
        else:
            self._file = wrap_function(_tl, 'taglib_file_new', [c_char_p], _FilePtr)(
                to_byte_str(str(filename)),
            )
        
        if not self._file or not self.__is_valid(self._file):
            raise OSError("Problem occurred while opening the file: {}".format(filename))

    def is_valid(self)-> bool:
        """
        Returns true if the file is open and readable and valid information for
        the Tag and / or AudioProperties was found.
        """
        if not self._file:
            return False
        return File.__is_valid(self._file)

    @property
    def tags(self)-> Tag:
        """
        Returns an instance to the Tag associated with this file. This will be freed
        automatically when the file is freed.
        """
        return Tag(self)

    @property
    def audio_properties(self)-> AudioProperties:
        """
        Returns an instance to the audio properties associated with this file. This
        will be freed automatically when the file is freed.
        """
        return AudioProperties(self)

    def close(self)-> None:
        """Frees and closes the file."""
        if self._file:
            self.__close(self._file)
            self._file = None

    def save(self)-> bool:
        """
        Saves the file to disk.
        raises a ValueError if file has been closed
        returns True if file saved successfully false otherwise
        """
        if not self._file:
            raise ValueError('I/O operation on closed file.')
        
        success = self.__save(self._file)
        
        return success
    
    def __enter__(self)-> Tuple[Tag, AudioProperties]:
        return (Tag(self), AudioProperties(self))

    def __exit__(self, *args)-> None:
        self.save()
        self.close()

    def __del__(self)-> None:
        """Frees and closes the file."""
        self.close()

# Special convenience ID3v2 functions

wrap_function(_tl, 'taglib_id3v2_set_default_text_encoding', [c_int])
def set_default_text_encoding(encoding: Union[ID3v2Encoding, int])-> None:
    """
    This sets the default encoding for ID3v2 frames that are written to tags.
    """
    _tl.taglib_id3v2_set_default_text_encoding(to_int(encoding))

wrap_function(_tl,'taglib_set_strings_unicode', [c_bool])
def set_strings_unicode(flag: bool)-> None:
    _tl.taglib_set_strings_unicode(flag)
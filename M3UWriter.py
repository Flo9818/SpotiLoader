import logging

import eyed3

logger = logging.getLogger(__name__)


class M3UWriter():
    def __init__(self, version=3):
        self.end_playlist = True
        self.playlist_entries = []
        self.version = version
        self.sequence = 0
        self.duration = self.duration()

    def addItem(self, pFile):
        entry = {'name': pFile, 'duration': eyed3.load('Music/' + pFile).info.time_secs}
        self.playlist_entries.append(entry)

    def writeM3U(self, pFilename='playlist.m3u'):
        print ("")
        print ("Writing Playlist: " + pFilename)
        playlist = self._generate()
        f = open('Music/' + pFilename, 'w')
        f.write(playlist)
        f.close()

    def _generate_playlist(self):
        playlist = "{}\n{}".format(self._m3u8_header_template(), self._generate_playlist_entries())
        return playlist

    def _generate_playlist_entries(self):
        playlist = ""
        for entry in self.playlist_entries:
            playlist += "#EXTINF:{duration}\n{media}\n".format(duration=float(entry['duration']), media=(entry['name']))
        return playlist

    def _generate(self):
        return self._generate_playlist()

    def _m3u8_header_template(self):
        header = "#EXTM3U\n#EXT-X-VERSION:{version}\n#EXT-X-MEDIA-SEQUENCE:{sequence}\n#EXT-X-TARGETDURATION:{duration}".format(
            version=self.version, sequence=self.sequence, duration=self.duration).strip()

        if self.end_playlist:
            return "{}\n#EXT-X-ENDLIST".format(header)
        else:
            return header

    def duration(self):
        duration_total = 0
        for entry in self.playlist_entries:
            if 'duration' in entry:
                try:
                    duration_total += float(entry['duration'])
                except Exception as e:
                    logger.exception(e)

        return duration_total

    def generate(self):
        """ This is a proxy for _generate makes it
        difficult to edit the real method for future."""
        return self._generate()

import subprocess
from torrentsort.folder_actions import *
from torrentsort.log import *


logging.basicConfig(level=logging.DEBUG)


class TorrentCheck:
    def __init__(self, path_to_watch, final):
        self.path_to_watch = path_to_watch
        self.final = final

    def get_audio_codec_channels(self, file):
        """
        Takes a video file and returns the their frame count
        Uses MediaInfo CLI to read
        """
        response = subprocess.check_output('MediaInfo "' + file + '" --Output="Audio;%Format%|%Channels%"', shell=True)\
            .decode("utf-8")
        response = response.rstrip()
        response = response.split('|')
        return response

    def video_pt_audio_transcode(self, i, o, options):
        if os.path.exists(o):
            logging.error('Output File exists! Not overwriting!')
        else:
            subprocess.call('ffmpeg -y -i "{0}" -vcodec copy -acodec ac3 {2} "{1}"'.format(i, o, options), shell=True)

    def codec_channels_algo(self, i, o, audio_codec, channels):
        if int(channels) > 6:
            logging.debug('Too many audio channels ({0}) for given spec, reducing to 5.1 audio'.format(channels))
            self.video_pt_audio_transcode(i, o, '-ac 6')
        else:
            if audio_codec != 'AAC' and audio_codec != 'AC-3':
                logging.debug('{0} is not supported in this playback environment...Transcoding to Dolby'.format(audio_codec))
                self.video_pt_audio_transcode(i, o, '')
            else:
                logging.debug('File matches required media specs')
                logging.debug('Audio codec detected as ' + audio_codec)
                logging.debug('Number of audio channels = ' + channels)

    def transcode_watch(self):
        """
        Main watch folder fucntion
        Starts a thread for every folder moved to watch
        """
        log_tracking('Initializing subprocess')
        before = dict([(f, None) for f in os.listdir(self.path_to_watch)])
        while True:
            time.sleep(5)
            after = dict([(f, None) for f in os.listdir(self.path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]
            if added:
                logging.info('Added: {0}'.format(', '.join(added)))
                for asset in added:
                    if os.path.isdir(os.path.join(self.path_to_watch, asset)):
                        file_asset = find_files_with_ext(os.path.join(self.path_to_watch, asset))
                        logging.debug('Input is ' + file_asset)
                        out_path = os.path.join(self.path_to_watch, asset, asset + '.AC-3.mkv')
                        self.codec_channels_algo(file_asset, out_path, self.get_audio_codec_channels(file_asset)[0],
                                            self.get_audio_codec_channels(file_asset)[1])
                    else:
                        file_asset = os.path.join(self.path_to_watch, asset)
                        out_path = os.path.join(self.final, asset[:-4] + '.AC-3.mkv')
                        self.codec_channels_algo(file_asset, out_path, self.get_audio_codec_channels(file_asset)[0], self.get_audio_codec_channels(file_asset)[1])
            if removed:
                logging.info("Removed: {0}".format(", ".join(removed)))
            before = after

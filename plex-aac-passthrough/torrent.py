import re


class TorrentAsset:
    def __init__(self, asset):
        self.asset = asset

    def get_season_and_episode(self):
        """
        :param asset:
        :return index 0 is season, index 1 is episode:
        """
        return (re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})", self.asset, re.I))[0]

    def get_season(self):
        return self.get_season_and_episode()[0]

    def get_episode(self):
        return self.get_season_and_episode()[1]

    def get_show_name(self):
        splitter = self.get_season()
        return self.asset.split('S' + splitter)[0].replace('.', ' ').strip(' ')



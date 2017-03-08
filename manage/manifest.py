import yaml
from datetime import datetime


MANIFEST_FILE = './manifest.yml'


class Containers(dict):
    @staticmethod
    def _version_ordering(version_str):
        scores = {
            'stable': 100,
            'beta': 101,
            'nightly': 102,
        }
        parts = version_str.split('.')
        if '-' in parts[-1]:
            last, extra = parts[-1].split('-', 1)
            parts = parts[:-1]
            parts.append(last)
        else:
            extra = ''

        parts = list(map(lambda v: scores[v] if v in scores.keys() else v, parts))
        parts = list(map(int, parts))
        parts.append(extra)
        return parts

    def add(self, path, version, archive, channel, extra_tags, onbuild):
        tags = Manifest._make_tags(version, channel, extra_tags, onbuild)
        self[tags[0]] = {
            'path': path,
            'archive': archive,
            'channel': channel,
            'onbuild': onbuild,
            'rustc': None,
            'image': None,
            'pushed': None,
            'updated': datetime.now(),
            'tags': tags
        }

    def update(self, main_tag, **kwargs):
        self[main_tag].update(kwargs)


    def items(self):
        for key in sorted(self.keys(), key=self._version_ordering):
            yield key, self[key]


class Manifest(object):
    def __init__(self):
        self.dockerhub_repo = None
        self.github_repo = None
        self.containers = Containers()
        self.created = datetime.now()
        self.updated = datetime.now()

    @staticmethod
    def load():
        try:
            yml_stream = open(MANIFEST_FILE, 'r')
        except IOError:
            return Manifest()
        return yaml.load(yml_stream)

    @staticmethod
    def _make_tags(version, channel, extra_tags, onbuild):
        if onbuild:
            transform = lambda tag: "{}-onbuild".format(tag)
        else:
            transform = lambda tag: str(tag)

        tags = []
        if channel:
            tags.append(transform(channel))
        tags.append(transform(version))
        if extra_tags:
            tags += map(transform, extra_tags)
        return tags

    def store(self):
        self.updated = datetime.now()
        yaml.dump(self, open(MANIFEST_FILE, 'w'), default_flow_style=False)

import datetime
from cnr.exception import ChannelNotFound, ChannelAlreadyExists
import cnr.semver as semver


class ChannelBase(object):
    def __init__(self, name, package):
        self.package = package
        self.name = name
        self._iscreated = None

    def exists(self):
        return self._exists()

    def _exists(self):
        """ Check if the channel is saved already """
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @classmethod
    def all_channels(cls, package):
        """ Returns all available channels for a package """
        channel_names = cls.all(package)
        result = {}
        for channel_name in channel_names:
            channel = cls(channel_name, package)
            releases = channel.releases()
            result[str(channel)] = {"releases": releases,
                                    "name": channel_name,
                                    "current": channel.current_release(releases)}
        return result

    @classmethod
    def all(cls, package):
        raise NotImplementedError

    def releases(self):
        """ Returns the list of versions """
        raise NotImplementedError

    def _add_release(self, version):
        # etcdctl put /{self.package/channels/{self.name}/version
        raise NotImplementedError

    def _remove_release(self, version):
        # etcdctl put /{self.package/channels/{self.name}/version
        raise NotImplementedError

    def current_release(self, releases=None):
        if releases is None:
            releases = self.releases()
        if not releases:
            return None
        ordered_versions = [str(x) for x in sorted(semver.versions(releases, False),
                                                   reverse=True)]
        return ordered_versions[0]

    def add_release(self, version, package_class):
        if self._check_release(version, package_class) is False:
            raise ValueError("Release %s doesn't exist for package %s" % (version, self.package))
        if not self.exists():
            self.save()
        return self._add_release(version)

    def remove_release(self, version):
        if not self.exists():
            self.save()
        return self._remove_release(version)

    def _check_release(self, release_name, package_class):
        version = package_class.get_version(self.package, release_name)
        if version is None or str(version) != release_name:
            return False
        else:
            return True

    def _new_chan_release(self, version):
        data = {'release': version,
                'created_at': datetime.datetime.utcnow().isoformat()}
        return data

    @classmethod
    def _raise_not_found(cls, package, channel=None, version=None):
        if channel is None:
            raise ChannelNotFound("No channel found for package '%s'" % (package),
                                  {'package': package})
        else:
            raise ChannelNotFound("Channel '%s' doesn't exist for package '%s'" % (channel, package),
                                  {'channel': channel, 'package': package, 'version': version})

    @classmethod
    def _raise_already_exists(cls, channel, package, version=None):
        if version is None:
            raise ChannelAlreadyExists("Channel '%s' exists already for package '%s'" % (channel, package),
                                       {'package': package, 'channel': channel})
        else:
            raise ChannelAlreadyExists("Realease '%s' exists already in channel '%s'" % (version, channel),
                                       {'package': package, 'channel': channel, 'version': version})

    def to_dict(self):
        releases = self.releases()
        return ({"releases": releases,
                 "name": self.name,
                 "current": self.current_release(releases)})

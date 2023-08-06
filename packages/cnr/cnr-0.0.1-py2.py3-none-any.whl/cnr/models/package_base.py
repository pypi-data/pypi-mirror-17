import datetime
import semantic_version
import cnr.packager as packager
from cnr.semver import last_version, select_version
from cnr.exception import (InvalidVersion,
                           PackageAlreadyExists,
                           ChannelNotFound,
                           PackageVersionNotFound,
                           PackageNotFound)


class PackageBase(object):
    def __init__(self, package_name, version=None, blob=None, data=None):
        self.package = package_name
        self.namespace, self.name = package_name.split("/")
        self.version = version
        self._data = data
        self.created_at = None
        self.packager = None
        self.blob = blob

    def channels(self, channel_class):
        """ Returns all available channels for a package """
        channel_names = channel_class.all(self.package)
        result = []
        for channel in channel_names:
            c = channel_class(channel, self.package)
            releases = c.releases()
            if self.version in releases:
                result.append(channel)
        return result

    @property
    def blob(self):
        return self.packager.b64blob

    @property
    def digest(self):
        return self.packager.digest

    @blob.setter
    def blob(self, value):
        if value is not None:
            self.packager = packager.Package(value)

    @property
    def data(self):
        if self._data is None:
            self._data = {'created_at': datetime.datetime.utcnow().isoformat()}
        d = {"package": self.package,
             "release": self.version,
             "blob": self.blob,
             "digest": self.packager.digest}

        self._data.update(d)
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.blob = data['blob']
        self.created_at = data['created_at']
        self.version = data['release']

    @classmethod
    def check_version(self, version):
        try:
            semantic_version.Version(version)
        except ValueError as e:
            raise InvalidVersion(e.message, {"version": version})
        return None

    @classmethod
    def get(self, package, version='default'):
        """
        package: string following "namespace/package_name" format
        version: version query. If None return latest version

        returns: (package blob(targz) encoded in base64, version)
        """
        p = self(package, version)
        p.pull(version)
        return p

    @classmethod
    def get_version(self, package, version_query, stable=False):
        versions = self.all_versions(package)
        if not versions:
            self._raise_not_found(package)
        if version_query is None or version_query == 'default':
            return last_version(versions, stable)
        else:
            try:
                return select_version(versions, str(version_query), stable)
            except ValueError as e:
                raise InvalidVersion(e.message, {"version": version_query})

    def pull(self, version_query=None):
        if version_query is None:
            version_query = self.version
        package = self.package
        version = self.get_version(package, version_query)
        if version is None:
            raise PackageVersionNotFound("No version match '%s' for package '%s'" % (version_query, package),
                                         {"package": package, "version_query": version_query})

        self.data = self._fetch(package, version)
        return self

    @classmethod
    def isdeleted_release(self, package, version):
        raise NotImplementedError

    @classmethod
    def search_index(self):
        pass

    @classmethod
    def add_index(self, name):
        pass

    @classmethod
    def remove_index(self, name):
        pass

    @classmethod
    def write_index(self, index):
        pass

    @classmethod
    def reindex(self):
        r = set()
        for package in self.all():
            r.add(package['name'])
        self.write_index(r)

    def save(self, force=False):
        self.check_version(self.version)
        if self.isdeleted_release(self.package, self.version) and not force:
            raise PackageAlreadyExists("Package release %s existed" % self.package,
                                       {"package": self.package, "version": self.version})
        self._save(force)
        self.add_index(self.package)

    def versions(self):
        return self.all_versions(self.package)

    @classmethod
    def _raise_not_found(self, package, version=None):
        raise PackageNotFound("package %s doesn't exist" % package,
                              {'package': package, 'version': version})

    @classmethod
    def all(self, namespace=None):
        raise NotImplementedError

    @classmethod
    def _fetch(self, package, version):
        raise NotImplementedError

    def _save(self, force=False):
        raise NotImplementedError

    @classmethod
    def _delete(self, package, version):
        raise NotImplementedError

    @classmethod
    def _delete_from_channels(self, package, version, channel_class):
        p = self(package, version)
        for channel in p.channels(channel_class):
            c = channel_class(channel, package)
            try:
                c.remove_release(version)
            except ChannelNotFound:
                pass

    @classmethod
    def delete(self, package, version, channel_class):
        self._delete_from_channels(package, version, channel_class)
        self._delete(package, version)
        if not self.all_versions(package):
            self.remove_index(package)

    @classmethod
    def all_versions(self, package):
        raise NotImplementedError

    @classmethod
    def search(self, query):
        raise NotImplementedError

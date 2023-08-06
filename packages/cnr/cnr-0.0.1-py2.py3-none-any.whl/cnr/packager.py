import base64
import gzip
import hashlib
import logging
import tarfile
import io
import os


logger = logging.getLogger(__name__)


def authorized_files():
    files = []
    for root, _, filenames in os.walk('.'):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def pack_app(app):
    tar = tarfile.open(app, "w:gz")
    for f in authorized_files():
        tar.add(f)
    tar.close()


def unpack_app(app, dest="."):
    tar = tarfile.open(app, "r:gz")
    tar.extractall(dest)
    tar.close()


class Package(object):
    def __init__(self, blob=None, b64_encoded=True):
        self.files = {}
        self.tar = None
        self.blob = None
        self.io_file = None
        self._digest = None
        self.b64blob = None
        if blob is not None:
            self.load(blob, b64_encoded)

    def _load_blob(self, blob, b64_encoded):
        if b64_encoded:
            self.b64blob = blob
            self.blob = base64.b64decode(blob)
        else:
            self.b64blob = base64.b64encode(blob)
            self.blob = blob

    def load(self, blob, b64_encoded=True):
        self._digest = None
        self._load_blob(blob, b64_encoded)
        self.io_file = io.BytesIO(self.blob)
        self.tar = tarfile.open(fileobj=self.io_file, mode='r:gz')
        for m in self.tar.getmembers():
            tf = self.tar.extractfile(m)
            if tf is not None:
                self.files[tf.name] = tf.read()

    def extract(self, dest):
        self.tar.extractall(dest)

    def pack(self, dest):
        f = open(dest, "wb")
        f.write(self.blob)
        f.close()

    def tree(self, directory=None):
        files = self.files.keys()
        files.sort()
        if directory is not None:
            filtered = [x for x in files if x.startswith(directory)]
        else:
            filtered = files
        return filtered

    def file(self, filename):
        return self.files[filename]

    @property
    def digest(self):
        if self._digest is None:
            self.io_file.seek(0)
            gunzip = gzip.GzipFile(fileobj=self.io_file, mode='r').read()
            self._digest = hashlib.sha256(gunzip).hexdigest()
        return self._digest

import os
import shutil
import tempfile


class TempDirectory(object):
    """
    Helper class that creates and cleans up a temporary directory, can
    be used as a context manager.
    >>> with TempDirectory() as tempdir:
    >>>     print(os.path.isdir(tempdir))
    """

    def __init__(
        self,
        cleanup=True,
        prefix="temp",
        debug_mode=False,
    ):

        self._cleanup = cleanup
        self._prefix = prefix
        self._debug_mode = debug_mode
        self.path = None

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.path)

    def __enter__(self):
        self.create()
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._debug_mode:
            self.move_to_curdir()

        if self._cleanup:
            self.cleanup()

    def create(self):
        if self.path is not None:
            return self.path

        tempdir = tempfile.mkdtemp(prefix="bentoctl-{}-".format(self._prefix))
        self.path = os.path.realpath(tempdir)

    def cleanup(self, ignore_errors=False):
        """
        Remove the temporary directory created
        """
        if self.path is not None and os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=ignore_errors)
        self.path = None

    def move_to_curdir(self):
        deployable_path = os.path.join(os.curdir, "bentoctl_deployable")
        if os.path.exists(deployable_path):
            shutil.rmtree(deployable_path)

        shutil.copytree(os.path.join(self.path, "bentoctl_deployable"), deployable_path)

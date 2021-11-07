import sys


class Platform:
    @staticmethod
    def fetch_platform():
        return sys.platform

    @staticmethod
    def is_windows_platform():
        return Platform.fetch_platform() == "win32"

    @staticmethod
    def is_unix_platform():
        if Platform.fetch_platform() == "aix" or Platform.fetch_platform() == "linux":
            return True
        else:
            return False

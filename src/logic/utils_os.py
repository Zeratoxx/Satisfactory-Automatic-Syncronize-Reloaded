import platform

from logic.OSType import OSType


def detect_os() -> OSType:
    system = platform.system().lower()
    if "windows" in system:
        return OSType.WINDOWS
    elif "linux" in system:
        return OSType.LINUX
    elif "darwin" in system:  # macOS
        return OSType.MAC
    else:
        return OSType.UNKNOWN

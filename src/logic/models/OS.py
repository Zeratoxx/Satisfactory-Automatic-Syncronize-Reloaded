import enum
import platform


class OS:
    class OSType(enum.Enum):
        WINDOWS = "Windows"
        LINUX = "Linux"
        MAC = "Mac"
        UNKNOWN = "Unknown"

    def detect_os(self) -> OSType:
        system = platform.system().lower()
        if "windows" in system:
            return self.OSType.WINDOWS
        elif "linux" in system:
            return self.OSType.LINUX
        elif "darwin" in system:  # macOS
            return self.OSType.MAC
        else:
            return self.OSType.UNKNOWN

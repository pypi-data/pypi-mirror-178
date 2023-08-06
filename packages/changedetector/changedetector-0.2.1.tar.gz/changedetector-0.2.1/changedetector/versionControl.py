import subprocess
from colors import Colors
import requests

class VersionControl:
    """
    check if there is not more recent package of changedetector
    """

    def __init__(self):
        self.venvinit_version = subprocess.check_output(
            ["pip", "show", "changedetector"]).decode("utf-8").split("Version: ")[1].split(" ")[0]
        self.venvint_version_split = self.venvinit_version.split(".")
        self.major = int(self.venvint_version_split[0])
        self.minor = int(self.venvint_version_split[1])
        self.patch = int(self.venvint_version_split[2].split("\n")[0])
        self.version = f"{self.major}.{self.minor}.{self.patch}"

    def upgradeMessage(self):
        print(Colors.clr(
            "There is a newer version of changedetector available", Colors.YELLOW))
        print(Colors.clr("Current version: ", Colors.GRAY) +
              Colors.clr(f"{self.venvinit_version}", Colors.WHITE))
        print(Colors.clr("Latest version: ", Colors.GRAY) +
              Colors.clr(f"{self.latest_version}", Colors.WHITE))
        print(Colors.clr("Run ", Colors.GRAY) + Colors.clr("pip install --upgrade changedetector",
                                                           Colors.WHITE) + Colors.clr(" to upgrade", Colors.GRAY))

    def getVersion(self):
        return self.version

    def check(self):

        try:
            self.latest_version: str = requests.get("https://pypi.org/pypi/changedetector/json").json()["info"]["version"]
            self.latest_version_split = self.latest_version.split(".")
            self.last_major = int(self.latest_version_split[0])
            self.last_minor = int(self.latest_version_split[1])
            self.last_patch = int(self.latest_version_split[2])

            if self.last_major == self.major:
                if self.last_minor == self.minor and self.last_patch == self.patch:
                    print(Colors.clr("changedetector is up to date", Colors.GREEN))
                elif self.last_minor == self.minor and self.last_patch > self.patch or self.last_minor != self.minor and self.last_minor > self.minor:
                    self.upgradeMessage()
            elif self.last_major > self.major:
                self.upgradeMessage()

        except requests.exceptions.ConnectionError:
            print(Colors.clr("Failed to check for updates", Colors.RED))

    def main(self):
        print("Changedetector")
        print(f"v{self.getVersion()}")
        print("Checking for updates...\r", end="")
        self.check()

if __name__ == "__main__":
    VersionControl().main()

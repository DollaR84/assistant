import os


class GitStatus:
    """`git status` parser"""
    __readme__ = ["startswith", "A", "D", "M", "R", "untracked"]
    out = None

    def __init__(self, out=None):
        if not out:
            raise ValueError("Out result after git status absent")

        self.out = out

    def _startswith(self, string):
        """return a list of files startswith string"""
        lines = []
        for line in self.out.splitlines():
            if line.find(string) == 0:
                lines.append(line.split(":")[1].strip())
        return lines

    @property
    def A(self):
        """return a list of added files"""
        return self._startswith("\tA")

    @property
    def D(self):
        """return a list of deleted files"""
        return self._startswith("\tD")

    @property
    def M(self):
        """return a list of modified files"""
        return self._startswith("\tm")

    @property
    def R(self):
        """return a list of renamed files"""
        return self._startswith("\tR")

    @property
    def untracked(self):
        """return a list of untracked files"""
        lines = []
        begin = False
        for line in self.out.splitlines():
            if "Untracked" in line:
                begin = True
                continue
            if not begin:
                continue

            if line.find("\t") == 0:
                lines.append(line.replace("\t", ""))
        return lines

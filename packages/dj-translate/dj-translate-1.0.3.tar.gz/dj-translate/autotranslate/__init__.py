VERSION = (1, 0, 3)


def get_version(svn=False, limit=3):
    """Return the version as a human-format string."""
    return '.'.join([str(i) for i in VERSION[:limit]])

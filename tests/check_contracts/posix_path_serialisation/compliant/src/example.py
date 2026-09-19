def serialise(path, root):
    return path.relative_to(root).as_posix()

def serialise(path, root):
    return str(path.relative_to(root))

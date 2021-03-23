def compare_dict(d1, d2, exclude: list = ["id"]) -> bool:
    assert len(d1.keys()) == len(d2.keys())

    for key in d1.keys():
        if key not in exclude and d1[key] != d2[key]:
            return False

    return True

def compare_dict(d1, d2, exclude: list) -> bool:
    exclude = exclude or ["id"]
    d1 = {k: v for k, v in d1.items() if k not in exclude}
    d2 = {k: v for k, v in d2.items() if k not in exclude}
    return d1 == d2

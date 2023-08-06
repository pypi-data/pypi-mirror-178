def convert_list_to_dist(x):
    from collections import Counter
    counts = Counter(x)
    z = sum(counts.values())
    dist = {k: v/z for k, v in counts.items()}
    return dist


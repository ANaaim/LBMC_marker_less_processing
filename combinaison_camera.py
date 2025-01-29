import itertools

def generate(with_group_unique=False):
    group = {"A": ["M11463"], "B": ["M11141", "M11458"], "C": ["M11139", "M11459"],
             "D": ["M11461", "M11140"], "E": ["M11462"]}
    new_dict = {}
    keys = list(group.keys())
    # Include combinations of 1 group where the value has at least a size of 2
    if with_group_unique:
        for key in keys:
            if len(group[key]) >= 2:
                new_dict[key] = sorted(group[key])

    # Generate combinations of 2, 3, 4, and 5 elements
    for r in range(2, 6):
        for combo in itertools.combinations(keys, r):
            new_key = ''.join(combo)
            new_value = []
            for key in combo:
                new_value.extend(group[key])
            new_dict[new_key] = sorted(new_value)  # Sort the new_value list

    return new_dict


if __name__ == "__main__":
    toto = generate()
    print(toto)
    # calculate dictionary siz
    print(len(toto))
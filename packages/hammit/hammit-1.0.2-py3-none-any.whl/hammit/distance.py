def distance(s1: str, s2: str) -> int:
    """
    Calculates the hamming distance between two equal length strings.

    s1: string - the first string to test
    s2: string - the second string to test

    returns: int representing hamming distance between s1 and s2
    """
    # Invalid input, return -1 indicating incomputable 
    if len(s2) != len(s1):
        return -1

    distance = 0
    for i in range(len(s1)):
        distance += 1 if s1[i] != s2[i] else 0

    return distance


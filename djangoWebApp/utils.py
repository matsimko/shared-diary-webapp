
def chunks(lst, n):
    """Yields successive n-sized chunks from lst."""
    for i in range(0, len(lst), n): #increment by n
        yield lst[i:i + n]

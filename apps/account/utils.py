from django.conf import settings

DATA_NO_PER_PAGE = 10


def slicer(data, page_i, limit=DATA_NO_PER_PAGE):
    limit = int(limit)
    start_idx = (page_i - 1) * limit
    end_idx = start_idx + limit
    return data[start_idx:end_idx]



 
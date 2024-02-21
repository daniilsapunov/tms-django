def paginate(lst, page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    max_page = int(len(lst) / page_size) + 1

    paginated_list = lst[start:end]

    if page_size > len(lst) and page > 1:
        print('ValueError')
        exit()

        'Не успел придумать не костыль, позже исправлю'

    result = {
        "count": len(lst),
        "next": f"?page={page + 1}&page_size={page_size}" if page < max_page else None,
        "previous": f"?page={page - 1}&page_size={page_size}" if page > 1 else None,
        "results": paginated_list
    }
    return result


print(paginate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], page=2, page_size=2))
print(paginate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], page=3, page_size=3))
print(paginate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], page=4, page_size=3))
print(paginate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], page=1, page_size=100))
print(paginate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], page=2, page_size=100))
# {'count': 10, 'next': '?page=3&page_size=2', 'previous': '?page=1&page_size=2', 'results': [3, 4]}
# {'count': 10, 'next': '?page=4&page_size=3', 'previous': '?page=2&page_size=3', 'results': [7, 8, 9]}
# {'count': 10, 'next': None, 'previous': '?page=3&page_size=3', 'results': [10]}
# {'count': 10, 'next': None, 'previous': None, 'results': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
# ValueError

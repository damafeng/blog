class Pagination:
    def __init__(self, page, max_page):
        self.start = 1
        self.page = page
        self.max_page = max_page

    @staticmethod
    def get_pagination(page, count):
        if count == 1:
            pagination = None
        else:
            pagination = Pagination(page, count)
        return pagination

    def has_prev(self):
        return self.page > self.start

    def has_next(self):
        return self.page < self.max_page

    def iter_pages(self):
        r = []
        if self.page - 3 <= self.start:
            r += [i for i in range(self.start, self.page + 1)]
        else:
            r += [1, None]
            r += [i for i in range(self.page - 2, self.page + 1)]
        if self.page + 3 >= self.max_page:
            r += [i for i in range(self.page + 1, self.max_page + 1)]
        else:
            r += [i for i in range(self.page + 1, self.page + 3)]
            r += [None, self.max_page]
        return r

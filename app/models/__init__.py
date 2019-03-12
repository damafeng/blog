import time
from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient()
db_name = 'db'
db = client[db_name]


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1,
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # data_id中存储各类型数据的下一序号
    # 找到返回序号并将表中序号+1
    d = db.data_id
    new_id = d.find_and_modify(**kwargs).get('seq')
    return new_id


class Model:
    __fields__ = [
        '_id',  # type ObjectId
        # 字段名， 属性， 默认值
        ('id', int, -1),
        ('type', str, ''),
        ('ct', int, 0),
        ('ut', int, 0),
        ('delete', bool, False),
    ]

    @classmethod
    def set_by_form(cls, form):
        m = cls()
        # 只处理预先设定的字段
        fields = cls.__fields__.copy()
        fields.remove('_id')
        if form is None:
            form = {}

        for field in fields:
            # k: 字段名, t: 类型， v： 默认值
            k, t, v = field
            if k in form:
                # 从form中取值
                setattr(m, k, t(form[k]))
            else:
                # 设为预设的默认值
                setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        insert model
        :param form:
        :param kwargs:
        :return: model
        """
        name = cls.__name__
        m = cls.set_by_form(form)

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 为id, ct, ut赋值
        m.id = next_id(name)
        t = int(time.time())
        m.ct = t
        m.ut = t
        m.type = name.lower()
        m._insert_one()
        return m

    def _insert_one(self):
        """增"""
        name = self.__class__.__name__
        db[name].insert_one(self.__dict__)

    @classmethod
    def _new_with_bson(cls, bson):
        """从数据库中查找数据后恢复数据为model对象"""
        m = cls.set_by_form(bson)
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def find_by(cls, all_data=False, **kwargs):
        if not all_data:
            kwargs['delete'] = False
        return cls._find_one(**kwargs)

    @classmethod
    def find_all(cls, sort=None, order='asc',
                 page_size=0, page_no=0, all_data=False, **kwargs):
        if order == 'des':
            order = DESCENDING
        else:
            order = ASCENDING
        kwargs['__sort'] = sort
        kwargs['__order'] = order
        kwargs['__page_size'] = page_size
        kwargs['__page_no'] = page_no
        if not all_data:
            kwargs['delete'] = False
        return cls._find(**kwargs)

    @classmethod
    def all(cls, sort=None, order='asc'):
        return cls.find_all(sort=sort, order=order)

    @classmethod
    def _find_one(cls, **kwargs):
        name = cls.__name__
        d = db[name].find_one(kwargs)
        if d is not None:
            return cls._new_with_bson(d)
        else:
            return None

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        flag_order = '__order'
        flag_page_size = '__page_size'
        flag_page_no = '__page_no'
        sort = kwargs.pop(flag_sort, None)
        order = kwargs.pop(flag_order, None)
        page_size = kwargs.pop(flag_page_size, 0)
        page_no = kwargs.pop(flag_page_no, 0)
        ds = db[name].find(kwargs)
        if sort is not None:
            if order is not None:
                ds.sort(sort, order)
            else:
                ds.sort(sort)
        if page_size != 0:
            skip = page_size * (page_no - 1)
            ds.limit(page_size).skip(skip)
        data_list = [cls._new_with_bson(d) for d in ds]
        return data_list

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        m = cls.find_by(**query_form)
        if m is None:
            query_form.update(update_form)
            m = cls.new(query_form)
        else:
            m.update(update_form, hard)
        return m

    def update(self, update_form, hard=False):
        update_form['ut'] = int(time.time())
        query = {
            'id': self.id,
        }
        for k, v in update_form.items():
            if not hasattr(self, k) and not hard:
                raise KeyError
        else:
            name = self.__class__.__name__
            update_form = {
                '$set': update_form,
            }
            return db[name].update_one(query, update_form)

    def save(self):
        form = self.__dict__.copy()
        form.pop('_id')
        return self.update(form)

    def remove(self):
        value = {
            'delete': True,
        }
        self.update(value)

    @staticmethod
    def blacklist():
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    def data_count(self, cls):
        name = cls.__name__
        i = '{}_id'.format(self.type)
        query = {
            'delete': False,
            i: self.id,
        }
        count = db[name].count_documents(query)
        return count

    @classmethod
    def count(cls, **kwargs):
        name = cls.__name__
        query = {
            'delete': False,
        }
        query.update(kwargs)
        count = db[name].count_documents(query)
        return count

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}={}'.format(k, v) for k, v in self.__dict__.items())
        return '<{}: \n {}\n>'.format(name, '\n '.join(properties))

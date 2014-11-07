import uuid
import types


class ModelConverter(object):

    def _to_model(self, obj):
        return obj

    def _from_model(self, obj):
        return obj

    def to_model(self, param):
        if param is None:
            yield param

        elif isinstance(param, list):
            for item in param:
                yield self._to_model(item)
        else:
            yield self._to_model(param)

    def from_model(self, param):
        if param is None:
            yield param

        elif isinstance(param, types.GeneratorType):
            for item in param:
                yield self._from_model(item)
        else:
            yield self._from_model(param)


class CRUDRepository(object):

    def __init__(self):
        self.converter = ModelConverter()

    def count(self):
        print 'count'

    def exists(self, id):
        print 'exists'

    def _save_one(self, obj):
        print '_save_one'

    def _save_list(self, objs):
        print '_save_list'

    def _find_one(self, id):
        print '_find_one'

    def _find_list(self, ids=None):
        print '_find_list'

    def _delete_by_id(self, obj):
        print '_delete_by_id'

    def _delete_one(self, obj):
        print '_delete_one'

    def _delete_list(self, objs):
        print '_delete_list'

    def _delete_all(self):
        print '_delete_all'

    def save(self, obj):
        if isinstance(obj, list):
            self._save_list(self.converter.to_model(obj))
        else:
            self._save_one(self.converter.to_model(obj).next())

    def find(self, param=None):
        if param:
            if isinstance(param, list):
                return self.converter.from_model(self._find_list(param))
            else:
                return self.converter.from_model(self._find_one(param)).next()
        else:
            return self.converter.from_model(self._find_list())

    def delete(self, param=None):
        if param:
            if isinstance(param, list):
                self._delete_list(self.converter.to_model(param))
            if isinstance(param, str):
                self._delete_by_id(param)
            else:
                self._delete_one(self.converter.to_model(param).next())
        else:
            return self._delete_all()


class SimpleCRUDRepository(CRUDRepository):

    def __init__(self):
        self.data = {}
        self.converter = ModelConverter()

    def count(self):
        return len(self.data)

    def exists(self, id):
        return id in self.data

    def _save_one(self, obj):
        id = obj.get('id', None)
        if id is None:
            obj['id'] = uuid.uuid4().hex

        self.data[id] = obj

    def _save_list(self, objs):
        for obj in objs:
            self._save_one(obj)

    def _find_one(self, id):
        return self.data.get(id, None)

    def _find_list(self, ids=None):
        if ids:
            for id in ids:
                yield self._find_one(id)
        else:
            for value in self.data.values():
                yield value

    def _delete_by_id(self, id):
        self.data.pop(id, None)

    def _delete_one(self, obj):
        id = obj['id']
        self._delete_by_id(id)

    def _delete_list(self, objs):
        for obj in objs:
            self._delete_one(obj)

    def _delete_all(self):
        self.data.clear()



repo = SimpleCRUDRepository()

one = {'id':'id', 'hello':'world'}

two = {'id':'id2', 'hello':'world'}
three = {'id':'id3', 'hello':'world'}
data = [two, three]

repo.save(one)
repo.save(data)

print repo.find('id')
print ''

for obj in repo.find(['id2', 'id3']):
    print obj

print ''
for obj in repo.find():
    print obj

repo.delete('id')
repo.delete(one)
repo.delete([one, two])

print 'After delete'
print ''
for obj in repo.find():
    print obj

repo.delete()

print 'End'
for obj in repo.find():
    print obj


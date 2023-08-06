import logging

from .restriction import Q
from .services import IdOnly, AllProperties

log = logging.getLogger(__name__)


class MultipleObjectsReturned(Exception):
    pass


class DoesNotExist(Exception):
    pass


class QuerySet:
    """
    A Django QuerySet-like class for querying items. Defers queries until the QuerySet is consumed. Supports chaining to
    build up complex queries.

    Django QuerySet documentation: https://docs.djangoproject.com/en/dev/ref/models/querysets/
    """
    VALUES = 'values'
    VALUES_LIST = 'values_list'
    FLAT = 'flat'
    NONE = 'none'
    RETURN_TYPES = (VALUES, VALUES_LIST, FLAT, NONE)

    def __init__(self, folder):
        self.folder = folder
        self.q = Q()
        self.only_fields = None
        self.order_fields = None
        self.reversed = False
        self.return_format = self.NONE

        self._cache = None

    def copy(self):
        new_qs = self.__class__(self.folder)
        new_qs.q = self.q
        new_qs.only_fields = self.only_fields
        new_qs.order_fields = self.order_fields
        new_qs.reversed = self.reversed
        new_qs.return_format = self.return_format
        new_qs._cache = self._cache
        return new_qs

    def _check_fields(self, field_names):
        allowed_field_names = set(self.folder.item_model.fieldnames()) | {'item_id', 'changekey'}
        for f in field_names:
            if f not in allowed_field_names:
                raise ValueError("Unknown fieldname '%s'" % f)

    def _query(self):
        if self.only_fields is None:
            # The list of fields was not restricted. Get all fields we support
            additional_fields = self.folder.item_model.fieldnames()
        else:
            # Remove ItemId and ChangeKey. We get them unconditionally
            additional_fields = tuple(f for f in self.only_fields if f not in {'item_id', 'changekey'})
        complex_fields_requested = bool(set(additional_fields) & set(self.folder.item_model.complex_fields()))
        if self.order_fields:
            for f in self.order_fields:
                if f not in additional_fields:
                    # TODO: Also fetch the order_by fields but remove them afterwards if they are not in additional_fields
                    raise ValueError("order_by field '%s' must be one of the fields to fetch (%s)" % (f, additional_fields))
        if not additional_fields and not self.order_fields:
            # We requested no additional fields and we need to do no sorting, so we can take a shortcut by setting
            # additional_fields=None. Thi tells find_items() to do less work
            assert not complex_fields_requested
            return self.folder.find_items(self.q, additional_fields=None, shape=IdOnly)
        if complex_fields_requested:
            # The FindItems service does not support complex field types. Fallback to getting ids and calling GetItems
            ids = self.folder.find_items(self.q, additional_fields=None, shape=IdOnly)
            items = self.folder.fetch(ids=ids, only_fields=additional_fields)
        else:
            items = self.folder.find_items(self.q, additional_fields=additional_fields, shape=IdOnly)
        if self.order_fields:
            items = sorted(items, key=lambda i: tuple(getattr(i, f) for f in self.order_fields))
        if self.reversed:
            items = reversed(items)
        return items

    def __iter__(self):
        # Fill cache if this is the first iteration. Return an iterator over the cached results.
        if self._cache is None:
            log.debug('Filling cache')
            if self.q is None:
                self._cache = []
            else:
                # TODO: This is still eager processing
                self._cache = list(self._query())
        cache_iter = iter(self._cache)
        if self.return_format == self.VALUES:
            return self.as_values(cache_iter)
        if self.return_format == self.VALUES_LIST:
            return self.as_values_list(cache_iter)
        if self.return_format == self.FLAT:
            return self.as_flat_values_list(cache_iter)
        assert self.return_format == self.NONE
        return cache_iter

    def __len__(self):
        self.__iter__()  # Make sure cache is full
        return len(self._cache)

    def __getitem__(self, key):
        self.__iter__()  # Make sure cache is full
        return self._cache[key]

    def as_values(self, iterable):
        if len(self.only_fields) == 0:
            raise ValueError('values() requires at least one field name')
        additional_fields = tuple(f for f in self.only_fields if f not in {'item_id', 'changekey'})
        if not additional_fields and not self.order_fields:
            # _query() will return an iterator of (item_id, changekey) tuples
            if 'changekey' not in self.only_fields:
                for item_id, changekey in iterable:
                    yield {'item_id': item_id}
            elif 'item_id' not in self.only_fields:
                for item_id, changekey in iterable:
                    yield {'changekey': changekey}
            else:
                for item_id, changekey in iterable:
                    yield {'item_id': item_id, 'changekey': changekey}
            return
        for i in iterable:
            yield {k: getattr(i, k) for k in self.only_fields}

    def as_values_list(self, iterable):
        if len(self.only_fields) == 0:
            raise ValueError('values_list() requires at least one field name')
        additional_fields = tuple(f for f in self.only_fields if f not in {'item_id', 'changekey'})

        if not additional_fields and not self.order_fields:
            # _query() will return an iterator of (item_id, changekey) tuples
            if 'changekey' not in self.only_fields:
                for item_id, changekey in iterable:
                    yield (item_id,)
            elif 'item_id' not in self.only_fields:
                for item_id, changekey in iterable:
                    yield (changekey,)
            else:
                for item_id, changekey in iterable:
                    yield (item_id, changekey)
            return
        for i in iterable:
            yield tuple(getattr(i, f) for f in self.only_fields)

    def as_flat_values_list(self, iterable):
        if len(self.only_fields) != 1:
            raise ValueError('flat=True requires exactly one field name')
        additional_fields = tuple(f for f in self.only_fields if f not in {'item_id', 'changekey'})

        if not additional_fields and not self.order_fields:
            # _query() will return an iterator of (item_id, changekey) tuples
            if 'item_id' in self.only_fields:
                for item_id, changekey in iterable:
                    yield item_id
            elif 'changekey' in self.only_fields:
                for item_id, changekey in iterable:
                    yield changekey
            else:
                assert False
            return
        for i in iterable:
            yield getattr(i, self.only_fields[0])

    ###############################
    #
    # Methods that support chaining
    #
    ###############################
    # Return copies of self, so this works as expected:
    #
    # foo_qs = my_folder.filter(...)
    # foo_qs.filter(foo='bar')
    # foo_qs.filter(foo='baz')  # Should not be affected by the previous statement
    #
    def all(self):
        # Invalidate cache and return all objects
        new_qs = self.copy()
        new_qs._cache = None
        return new_qs

    def none(self):
        new_qs = self.copy()
        new_qs._cache = None
        new_qs.q = None
        return new_qs

    def filter(self, *args, **kwargs):
        new_qs = self.copy()
        q = Q.from_filter_args(self.folder.item_model, *args, **kwargs) or Q()
        new_qs.q = q if new_qs.q is None else new_qs.q & q
        return new_qs

    def exclude(self, *args, **kwargs):
        new_qs = self.copy()
        q = ~Q.from_filter_args(self.folder.item_model, *args, **kwargs) or Q()
        new_qs.q = q if new_qs.q is None else new_qs.q & q
        return new_qs

    def only(self, *args):
        try:
            self._check_fields(args)
        except ValueError as e:
            raise ValueError("%s in only()" % e.args[0])
        new_qs = self.copy()
        new_qs.only_fields = args
        return new_qs

    def order_by(self, *args):
        # TODO: support '-my_field' for reverse sort
        try:
            self._check_fields(args)
        except ValueError as e:
            raise ValueError("%s in order_by()" % e.args[0])
        new_qs = self.copy()
        new_qs.order_fields = args
        return new_qs

    def reverse(self):
        new_qs = self.copy()
        if not self.order_fields:
            raise ValueError('Reversing only makes sense if there are order_by fields')
        new_qs.reversed = not self.reversed
        return new_qs

    def values(self, *args):
        try:
            self._check_fields(args)
        except ValueError as e:
            raise ValueError("%s in values()" % e.args[0])
        new_qs = self.copy()
        new_qs.only_fields = args
        new_qs.return_format = self.VALUES
        return new_qs

    def values_list(self, *args, flat=False):
        try:
            self._check_fields(args)
        except ValueError as e:
            raise ValueError("%s in values_list()" % e.args[0])
        new_qs = self.copy()
        new_qs.only_fields = args
        new_qs.return_format = self.FLAT if flat else self.VALUES_LIST
        return new_qs

    ###########################
    #
    # Methods that end chaining
    #
    ###########################
    def iterator(self):
        # Return an iterator that doesn't bother with caching
        return self._query()

    def get(self, *args, **kwargs):
        new_qs = self.filter(*args, **kwargs)
        items = list(new_qs)
        if len(items) == 0:
            raise DoesNotExist()
        if len(items) != 1:
            raise MultipleObjectsReturned()
        return items[0]

    def count(self):
        # Get the item count with as little effort as possible
        new_qs = self.copy()
        new_qs.only_fields = tuple()
        new_qs.order_fields = None
        new_qs.reverse = False
        return len(list(new_qs))

    def exists(self):
        return self.count() > 0

    def delete(self):
        # Delete the items with as little effort as possible
        new_qs = self.copy()
        new_qs.only_fields = tuple()
        new_qs.order_fields = None
        new_qs.reverse = False
        from .folders import ALL_OCCURRENCIES
        return self.folder.bulk_delete(ids=new_qs, affected_task_occurrences=ALL_OCCURRENCIES)

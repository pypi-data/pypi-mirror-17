from weakref import WeakValueDictionary
from collections import deque
import math

from pysistency.utilities.std_clone import inherit_docstrings
from pysistency.utilities.constants import NOTSET
from pysistency.backend.base_store import BaseBucketStore, BucketNotFound


class ListBucket(list):
    """Subclass of :py:class:`list` allowing for weak references"""
    pass


@inherit_docstrings(inherit_from=list)
class PersistentList(object):
    """
    Sequence object that is persistently stored

    :param store_uri: URI for storing buckets; see :py:class:`~BaseBucketStore`
    :type store_uri: :py:class:`str`

    :param bucket_length: number of items to store per bucket
    :type bucket_length: :py:class:`int`

    :param cache_size: number of buckets to LRU-cache in memory
    :type cache_size: :py:class:`int`
    """
    persistent_defaults = {
        'bucket_length': 32,
    }

    def __init__(self, store_uri, bucket_length=NOTSET, cache_size=3):
        self._bucket_store = BaseBucketStore.from_uri(store_uri=store_uri, default_scheme='file')
        # set empty fields
        self._bucket_length = None
        self._bucket_count = 0
        self._len = 0
        self._bucket_cache = None
        self._cache_size = None
        self.bucket_key_fmt = None
        # load current settings
        try:
            for attr, value in self._bucket_store.fetch_head().items():
                setattr(self, attr, value)
        except BucketNotFound:
            pass
        # apply new settings
        self.bucket_length = bucket_length
        # LRU store for objects fetched from disk
        self.cache_size = cache_size
        # weakref store for objects still in use
        self._active_buckets = WeakValueDictionary()
        self._active_items = WeakValueDictionary()
        # calcualate metadata
        self._length = self._fetch_length()
        # store new settings
        self._store_head()

    # Settings
    def _store_head(self):
        """
        Store the meta-information of the dict
        """
        self._bucket_store.store_head({
            attr: getattr(self, attr) for attr in
            ('bucket_length', '_bucket_count')
        })

    def _fetch_length(self):
        """Calculate the length of the list from the persistent store"""
        if self._bucket_count == 0:
            return 0
        last_bucket = self._fetch_bucket(self.bucket_key_fmt % (self._bucket_count - 1))
        return (self._bucket_count - 1) * self._bucket_length + len(last_bucket)

    def _update_bucket_key_fmt(self):
        # key: count, salt, index
        self.bucket_key_fmt = "dlistbkt_%(bucket_length)xs%%x" % {
            'bucket_length': self.bucket_length,
        }

    @property
    def _length(self):
        return self._len

    @_length.setter
    def _length(self, value):
        # detect change of bucket count
        if self._bucket_count != value // self._bucket_length:
            self._bucket_count = value // self._bucket_length
            self._store_head()
        self._len = value

    # exposed settings
    @property
    def cache_size(self):
        return self._cache_size

    @cache_size.setter
    def cache_size(self, value):
        self._cache_size = int(value or 1)
        self._bucket_cache = deque(maxlen=self.cache_size)

    @property
    def bucket_length(self):
        """
        Get/Set the ``bucket_length`` of the persistent mapping

        :note: Setting ``bucket_length`` causes **all** buckets storing data to be
               recreated. Until the new buckets have been created, changes to the
               mapping content may be silently dropped.
        """
        return self._bucket_length

    @bucket_length.setter
    def bucket_length(self, value):
        # default if unset
        if value == NOTSET:
            if self._bucket_length is not None:
                return
            self._bucket_length = self.persistent_defaults['bucket_length']
        else:
            value = int(value)
            if value < 1:
                raise ValueError('At least one item per bucket must be used')
            # no change
            elif self._bucket_length == value:
                return
            # uninitialized, we don't have content yet
            elif self._bucket_length is None:
                self._bucket_length = value
            # TODO: allow resizing backend
            else:
                raise NotImplementedError('Changing bucket count not implemented yet')
        # apply secondary settings
        self._update_bucket_key_fmt()

    # bucket management
    @property
    def _bucket_keys(self):
        """List of used bucket keys"""
        return [self._bucket_key(idx) for idx in range(0, self._length, self._bucket_length)]

    def _bucket_key(self, index):
        """
        Create the bucket identifier for a given key

        :param index: key to the content in-memory
        :return: key to the bucket stored persistently
        :rtype: str
        """
        if index < 0:
            index += self._length
        return self.bucket_key_fmt % (index // self._bucket_length)

    def _fetch_bucket(self, bucket_key):
        """
        Return a bucket from disk or create a new one

        :param bucket_key: key for the bucket
        :return: bucket for ``bucket_key``
        :rtype: :py:class:`~DictBucket`
        """
        try:
            bucket = self._bucket_store.fetch_bucket(bucket_key=bucket_key)
        except BucketNotFound:
            self._store_head()
            bucket = ListBucket()
        self._active_buckets[bucket_key] = bucket
        self._bucket_cache.appendleft(bucket)
        return bucket

    def _get_bucket(self, bucket_key):
        """
        Return the appropriate bucket

        May return the cached bucket if available.

        :param bucket_key: key for the bucket
        :return: bucket for ``bucket_key``
        :rtype: :py:class:`~DictBucket`
        """
        try:
            return self._active_buckets[bucket_key]
        except KeyError:
            return self._fetch_bucket(bucket_key)

    def _store_bucket(self, bucket_key, bucket=None):
        """
        Store a bucket on disk

        :param bucket_key: key for the entire bucket
        """
        if bucket is None:
            try:
                bucket = self._active_buckets[bucket_key]
            except KeyError:
                return
        if bucket:
            self._bucket_store.store_bucket(bucket_key=bucket_key, bucket=bucket)
        # free empty buckets
        else:
            self._bucket_store.free_bucket(bucket_key)

    # cache management
    # Item cache
    def _set_cached_item(self, key, item):
        """Cache reference to existing item"""
        try:
            self._active_items[key] = item
        except TypeError:
            pass

    def _get_cached_item(self, key):
        """Get reference to existing item; raises KeyError if item cannot be fetched"""
        try:
            return self._active_items[key]
        except TypeError:
            raise KeyError

    def _del_cached_item(self, key):
        """Release reference to existing item"""
        try:
            del self._active_items[key]
        except (TypeError, KeyError):
            pass

    # paths and files
    def flush(self):
        """
        Commit all outstanding changes to persistent store
        """
        for bucket_key, bucket in self._active_buckets.values():
            self._store_bucket(bucket_key, bucket)

    # sequence interface
    def __getitem__(self, pos):
        if isinstance(pos, slice):
            return self._get_slice(pos)
        return self._get_item(pos)

    def _get_item(self, index):
        # - use cached reference to existing item
        # - fetch item from cached reference to existing bucket
        # - fetch item from fetched bucket
        try:
            return self._get_cached_item(index)
        except KeyError:
            bucket = self._get_bucket(self._bucket_key(index))
            item = bucket[index % self._bucket_length]
        self._set_cached_item(index, item)
        return item

    def _get_slice(self, positions):
        start_idx, stop_idx, stride = positions.indices(self._length)
        list_slice = []
        # fetch sub-slice from each bucket
        while start_idx < stop_idx:
            bucket = self._get_bucket(self._bucket_key(start_idx))
            # stop_idx in next bucket
            if stop_idx // self._bucket_length > start_idx // self._bucket_length:
                list_slice.extend(bucket[start_idx % self._bucket_length::stride])
                slice_length = math.ceil((self._bucket_length - (start_idx % self._bucket_length)) / stride)
            # stop_idx in this bucket
            else:
                list_slice.extend(bucket[start_idx % self._bucket_length:stop_idx % self._bucket_length:stride])
                slice_length = math.ceil(((stop_idx - start_idx) % self._bucket_length) / stride)
            # advance to next bucket
            start_idx += slice_length * stride
        return list_slice

    def __setitem__(self, pos, value):
        if isinstance(pos, slice):
            self._set_slice(pos, value)
        else:
            self._set_item(pos, value)

    def _set_slice(self, positions, sequence):
        start_idx, stop_idx, stride = positions.indices(self._length)
        sequence = list(sequence)
        # fetch sub-slice from each bucket
        while start_idx < stop_idx:
            bucket_key = self._bucket_key(start_idx)
            bucket = self._get_bucket(bucket_key)
            # stop_idx in next bucket
            if stop_idx // self._bucket_length > start_idx // self._bucket_length:
                slice_length = math.ceil((self._bucket_length - (start_idx % self._bucket_length)) / stride)
                bucket[start_idx % self._bucket_length::stride] = sequence[:slice_length]
            # stop_idx in this bucket
            else:
                slice_length = math.ceil(((stop_idx - start_idx) % self._bucket_length) / stride)
                bucket[start_idx % self._bucket_length:stop_idx % self._bucket_length:stride] = sequence[:slice_length]
            self._store_bucket(bucket_key, bucket)
            # advance to next bucket
            start_idx += slice_length * stride
            sequence[:] = sequence[slice_length:]

    def _set_item(self, index, value):
        bucket_key = self._bucket_key(index)
        bucket = self._get_bucket(bucket_key)
        bucket[index % self._bucket_length] = value
        self._store_bucket(bucket_key, bucket)
        # update item cache
        self._set_cached_item(index, value)

    def __delitem__(self, index):
        if isinstance(index, slice):
            self._del_slice(index)
        else:
            self._del_item(index)

    def _del_slice(self, positions):
        start_idx, stop_idx, stride = positions.indices(self._length)
        print(start_idx, stop_idx, stride)
        if start_idx == stop_idx:
            return
        # TODO: make this work on sequences
        for idx in range(start_idx, stop_idx, stride):
            self._del_item(idx)
        # consecutive sequence
        #if stride == 1:
        #    pass

    def _del_item(self, pos):
        self._del_cached_item(pos)
        # delete first element, append first element with next bucket
        this_bucket_key = self._bucket_key(pos)
        this_bucket = self._get_bucket(this_bucket_key)
        # remaining elements move one forward
        del this_bucket[pos % self._bucket_length]  # if this fails, IndexError for entire collection
        # index of first element of next bucket
        pos = (pos // self._bucket_length + 1) * self._bucket_length
        # fill missing last element with first of next bucket
        while pos < self._length - 1:
            next_bucket_key = self._bucket_key(pos)
            next_bucket = self._get_bucket(next_bucket_key)
            this_bucket.append(next_bucket.pop(0))
            self._store_bucket(this_bucket_key, this_bucket)
            this_bucket_key = next_bucket_key
            this_bucket = next_bucket
            pos += self._bucket_length
        # store last bucket
        self._store_bucket(this_bucket_key, this_bucket)
        self._length -= 1

    # container protocol
    def __len__(self):
        return self._length

    # list methods
    def append(self, item):
        bucket_key = self._bucket_key(self._length)
        bucket = self._get_bucket(bucket_key)
        bucket.append(item)
        self._store_bucket(bucket_key, bucket)
        # update item cache
        self._set_cached_item(self._length, item)
        self._length += 1

    def extend(self, sequence):
        # split sequence into chunks to fill each bucket
        while sequence:
            bucket_key = self._bucket_key(self._length)
            bucket = self._get_bucket(bucket_key)
            bucket_sequence, sequence = \
                sequence[:self._bucket_length - len(bucket)], sequence[self._bucket_length - len(bucket):]
            bucket.extend(bucket_sequence)
            self._store_bucket(bucket_key, bucket)
            # update item cache
            for idx, item in enumerate(bucket_sequence):
                self._set_cached_item(self._length + idx, item)
            self._length += len(bucket_sequence)

    def clear(self):
        # clear persistent storage
        for bucket_key in self._bucket_keys:
            self._bucket_store.free_bucket(bucket_key=bucket_key)
        self._length = 0
        self._bucket_count = 0
        self._store_head()
        # reset caches
        self._bucket_cache = deque(maxlen=self.cache_size)
        self._active_buckets = type(self._active_buckets)()
        #self._active_items = type(self._active_items)()

    def insert(self, index, value):
        raise NotImplementedError

    def pop(self, index=None):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def reverse(self, value):
        raise NotImplementedError

    def __str__(self):
        return '[<%s>]' % ('>, <'.join(
            str(self._get_bucket(bucket_key))[1:-1] for bucket_key in self._bucket_keys
        ))

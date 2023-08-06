from abc import ABC, abstractmethod
from functools import cached_property
from io import BytesIO
from itertools import chain
from math import ceil
from operator import itemgetter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import MutableSequence, Callable, MutableMapping, Protocol, Iterator
from wave import Wave_write

from dol import appendable, Files, wrap_kvs
from mongodol.tracking_methods import (
    track_method_calls,
    track_calls_without_executing,
    TrackableMixin,
)
from recode import (
    encode_pcm_bytes,
    decode_wav_bytes,
)


class BulkStore(Protocol):
    """Mutable Mapping with Append Method"""

    def append(self, item):
        pass

    def __setitem__(self, __k, __v) -> None:
        pass

    def __delitem__(self, __v) -> None:
        pass

    def __getitem__(self, __k):
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> Iterator:
        pass


class AbstractBulkAppend(TrackableMixin, ABC):
    bulk_factory: Callable[[], MutableSequence] = list

    @cached_property
    def _bulk(self) -> MutableSequence:
        """Sequence of items.

        :return:
        """
        return self.bulk_factory()

    def _execute_tracks(self):
        for func, args, kwargs in self._tracks:
            if kv := self._bulk_append(*args, **kwargs):
                func(self, kv)
        if len(self._bulk) > 0:
            kv = self._bulk_kv(self._bulk)
            func(self, kv)

    def _bulk_append(self, item):
        """Append item to bulk and return None, or combine bulk and return the resulting item.

        :param item:
        :return:
        """
        if len(self._bulk) > 0:
            if self._should_bulk(item):
                self._bulk.append(item)
            else:
                rv = self._bulk_kv(self._bulk)
                self._bulk.clear()
                self._bulk.append(item)
                return rv
        else:
            self._bulk.append(item)
        return None

    @abstractmethod
    def _should_bulk(self, item) -> bool:
        """Check if next item triggers the condition to bulk all the items into a single item

        :param item:
        :return:
        """
        pass

    @abstractmethod
    def _bulk_kv(self, bulk):
        """Takes the sequence of items and combines into a single item

        :param bulk:
        :return:
        """
        pass


audio_slab_kv = itemgetter('timestamp', 'wf')


N_TO_BULK = 10


def should_bulk_if_bt_within_n(self, item, n=N_TO_BULK):
    bulk_ts, _ = audio_slab_kv(self._bulk[0])
    item_ts, _ = audio_slab_kv(item)
    return item_ts - bulk_ts < n


def join_ts_wf(self, bulk):
    """Merge bulk and return key and joined value

    :param bulk:
    :return:
    """
    ts = bulk[0]['timestamp']
    joined_wf = list(chain.from_iterable(map(itemgetter('wf'), bulk)))
    return {'timestamp': ts, 'wf': joined_wf}


def bulk_append(
    should_bulk=should_bulk_if_bt_within_n,
    bulk_kv=join_ts_wf,
    bulk_factory_callable=AbstractBulkAppend.bulk_factory,
):
    class BulkAppend(AbstractBulkAppend):
        bulk_factory = bulk_factory_callable

        def _should_bulk(self, item) -> bool:
            return should_bulk(self, item)

        def _bulk_kv(self, bulk):
            return bulk_kv(self, bulk)

    return BulkAppend


def ts_to_filename(ts, ext='.wav'):
    return f'{ts}{ext}'


def filename_to_ts(name, ext='.wav'):
    return int(name[: -len(ext)])


def wf_to_wav(
    wf, sr: int = 44100, width_bytes: int = 2, *, n_channels: int = 1
) -> bytes:
    bio = BytesIO()
    with Wave_write(bio) as obj:
        obj.setparams((n_channels, width_bytes, sr, 0, 'NONE', 'not compressed'))
        wf_bytes = encode_pcm_bytes(wf, width=width_bytes * 8, n_channels=n_channels)
        obj.writeframes(wf_bytes)
        bio.seek(0)
    return bio.read()


def wav_to_wf(wav):
    wf, sr = decode_wav_bytes(wav)
    return wf


@track_method_calls(
    tracked_methods='append',
    tracking_mixin=bulk_append(),
    calls_tracker=track_calls_without_executing,
)
@appendable(item2kv=audio_slab_kv)
@wrap_kvs(
    key_of_id=filename_to_ts,
    id_of_key=ts_to_filename,
    obj_of_data=wav_to_wf,
    data_of_obj=wf_to_wav,
)
class WavFileStore(Files, BulkStore):
    pass


@track_method_calls(
    tracked_methods='append',
    tracking_mixin=bulk_append(),
    calls_tracker=track_calls_without_executing,
)
@appendable(item2kv=audio_slab_kv)
class DictStore(dict, BulkStore):
    pass


def _test_dict_store():
    _test_store(DictStore())


def _test_files_store():
    with TemporaryDirectory() as tmpdirname:
        audio_store = WavFileStore(rootdir=tmpdirname)
        _test_store(audio_store)
        print(f'{len(list(Path(tmpdirname).iterdir()))=} == {len(audio_store)=}')
        assert len(list(Path(tmpdirname).iterdir())) == len(audio_store)


def _test_store(store_instance: MutableMapping, *, n=22, chk_size=2, log=print):
    """Test append, tracking, input, and output

    :param store_instance:
    :param n: number of chunks
    :param chk_size: samples per chunk
    :param log: print
    :return:
    """
    with store_instance as a:
        for i in range(n):
            a.append({'timestamp': i, 'wf': [i] * chk_size})
            log('print#2', f'{i=}', f'{len(a._tracks)=}', a)
            assert (
                len(a._tracks) == (i + 1) % N_TO_BULK
            ), 'Tracking should auto flush when size limit is reached'
            log('print#3', f'{len(a) == 0=}')
            assert len(a) == 0, list(a)
        log('print#4', f'{len(a._tracks) == n=}')
        assert len(a._tracks) == n
        log('print#5', a, len(a._tracks))

    log('print#6', len(a._tracks), a)
    assert len(a._tracks) == 0
    assert len(a) == ceil(n / N_TO_BULK), f'{len(a)=} == {ceil(n / N_TO_BULK)=}'
    for i, (k, v) in enumerate(sorted(a.items())):
        log('print#7', f'{(k, v)=}')
        assert k == i * N_TO_BULK
        if k + N_TO_BULK > n:
            assert (
                len(v) / chk_size == n - k
            ), f'{i=}, {k=}, {len(v) / chk_size=}, {n - k=}'
        else:
            assert (
                len(v) / chk_size == N_TO_BULK
            ), f'{i=}, {k=}, {len(v) / chk_size=}, {N_TO_BULK=}'
        v_iter = iter(v)
        for j in range(i * N_TO_BULK, min((i + 1) * N_TO_BULK, n)):
            for _ in range(chk_size):
                assert (
                    next(v_iter) == j
                ), f'{i=}, {j=}, {k=}, {i * N_TO_BULK=}, {min((i + 1) * N_TO_BULK, n)=}'

    print(f'Test passed with params: {store_instance=}, {n=}, {chk_size=}, {log=}')


if __name__ == '__main__':
    _test_dict_store()
    _test_files_store()

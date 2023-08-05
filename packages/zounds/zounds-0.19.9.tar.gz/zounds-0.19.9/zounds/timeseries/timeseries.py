from featureflow import \
    NumpyEncoder, NumpyMetaData, Feature, BaseNumpyDecoder
import numpy as np
from duration import Picoseconds
from samplerate import SampleRate
import re


class TimeSlice(object):
    def __init__(self, duration=None, start=None):
        super(TimeSlice, self).__init__()

        if duration is not None and not isinstance(duration, np.timedelta64):
            raise ValueError('duration must be of type {t} but was {t2}'.format(
                    t=np.timedelta64, t2=duration.__class__))

        if start is not None and not isinstance(start, np.timedelta64):
            raise ValueError('start must be of type {t} but was {t2}'.format(
                    t=np.timedelta64, t2=start.__class__))

        self.duration = duration
        self.start = start or Picoseconds(0)

    def __add__(self, other):
        return TimeSlice(self.duration, start=self.start + other)

    def __radd__(self, other):
        return self.__add__(other)

    @property
    def end(self):
        return self.start + self.duration

    def __lt__(self, other):
        try:
            return self.start.__lt__(other.start)
        except AttributeError:
            return self.start.__lt__(other)

    def __gt__(self, other):
        try:
            return self.start.__gt__(other.start)
        except AttributeError:
            return self.start.__get__(other)

    def __le__(self, other):
        try:
            return self.start.__le__(other.start)
        except AttributeError:
            return self.start.__le__(other)

    def __ge__(self, other):
        try:
            return self.start.__ge__(other.start)
        except AttributeError:
            return self.start.__ge__(other)

    def __and__(self, other):
        delta = max(
                Picoseconds(0),
                min(self.end, other.end) - max(self.start, other.start))
        return TimeSlice(delta)

    def __contains__(self, other):
        print other
        if isinstance(other, np.timedelta64):
            return self.start < other < self.end
        if isinstance(other, TimeSlice):
            return other.start > self.start and other.end < self.end
        raise ValueError

    def __eq__(self, other):
        return self.start == other.start and self.duration == other.duration

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{cls}(duration = {duration}, start = {start})'.format(
                cls=self.__class__.__name__,
                duration=str(self.duration),
                start=str(self.start))

    def __str__(self):
        return self.__repr__()


class ConstantRateTimeSeriesMetadata(NumpyMetaData):
    DTYPE_RE = re.compile(r'\[(?P<dtype>[^\]]+)\]')

    def __init__(
            self,
            dtype=None,
            shape=None,
            frequency=None,
            duration=None):
        super(ConstantRateTimeSeriesMetadata, self).__init__(
                dtype=dtype, shape=shape)
        self.frequency = self._decode_timedelta(frequency)
        self.duration = self._decode_timedelta(duration)

    @staticmethod
    def from_timeseries(timeseries):
        return ConstantRateTimeSeriesMetadata(
                dtype=timeseries.dtype,
                shape=timeseries.shape[1:],
                frequency=timeseries.frequency,
                duration=timeseries.duration)

    def _encode_timedelta(self, td):
        dtype = self.DTYPE_RE.search(str(td.dtype)).groupdict()['dtype']
        return td.astype(np.uint64).tostring(), dtype

    def _decode_timedelta(self, t):
        if isinstance(t, np.timedelta64):
            return t

        v = np.fromstring(t[0], dtype=np.uint64)[0]
        s = t[1]
        return np.timedelta64(long(v), s)

    def __repr__(self):
        return repr((
            str(np.dtype(self.dtype)),
            self.shape,
            self._encode_timedelta(self.frequency),
            self._encode_timedelta(self.duration)
        ))


class BaseConstantRateTimeSeriesEncoder(NumpyEncoder):
    def __init__(self, needs=None):
        super(BaseConstantRateTimeSeriesEncoder, self).__init__(needs=needs)

    def _prepare_data(self, data):
        raise NotImplementedError()

    def _prepare_metadata(self, data):
        return ConstantRateTimeSeriesMetadata.from_timeseries(data)


class ConstantRateTimeSeriesEncoder(BaseConstantRateTimeSeriesEncoder):
    def __init__(self, needs=None):
        super(ConstantRateTimeSeriesEncoder, self).__init__(needs=needs)

    def _prepare_data(self, data):
        return data


class PackedConstantRateTimeSeriesEncoder(BaseConstantRateTimeSeriesEncoder):
    def __init__(self, needs=None, axis=1):
        super(PackedConstantRateTimeSeriesEncoder, self).__init__(needs=needs)
        self.axis = axis

    def _prepare_data(self, data):
        packedbits = np.packbits(data.astype(np.uint8), axis=self.axis)

        return ConstantRateTimeSeries(
                packedbits,
                frequency=data.frequency,
                duration=data.duration)


class GreedyConstantRateTimeSeriesDecoder(BaseNumpyDecoder):
    def __init__(self):
        super(GreedyConstantRateTimeSeriesDecoder, self).__init__()

    def _unpack_metadata(self, flo):
        return ConstantRateTimeSeriesMetadata.unpack(flo)

    def _wrap_array(self, raw, metadata):
        return ConstantRateTimeSeries(
                raw, metadata.frequency, metadata.duration)


class ConstantRateTimeSeriesFeature(Feature):
    def __init__(
            self,
            extractor,
            needs=None,
            store=False,
            key=None,
            encoder=ConstantRateTimeSeriesEncoder,
            decoder=GreedyConstantRateTimeSeriesDecoder(),
            **extractor_args):
        super(ConstantRateTimeSeriesFeature, self).__init__(
                extractor,
                needs=needs,
                store=store,
                encoder=encoder,
                decoder=decoder,
                key=key,
                **extractor_args)


class ConstantRateTimeSeries(np.ndarray):
    """
    A TimeSeries implementation with samples of a constant duration and
    frequency.
    """

    def __new__(cls, input_array, frequency=None, duration=None):
        if not isinstance(frequency, np.timedelta64):
            raise ValueError('duration must be of type {t} but was {t2}'.format(
                    t=np.timedelta64, t2=frequency.__class__))

        if duration is not None and not isinstance(duration, np.timedelta64):
            raise ValueError('start must be of type {t} but was {t2}'.format(
                    t=np.timedelta64, t2=duration.__class__))

        obj = np.asarray(input_array).view(cls)
        obj.frequency = frequency
        obj.duration = duration or frequency
        return obj

    def kwargs(self, **kwargs):
        return dict(frequency=self.frequency, duration=self.duration, **kwargs)

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.frequency = getattr(obj, 'frequency', None)
        self.duration = getattr(obj, 'duration', None)

    @classmethod
    def from_example(cls, arr, example):
        return cls(arr, frequency=example.frequency, duration=example.duration)

    def concatenate(self, other):
        if self.frequency == other.frequency and self.duration == other.duration:
            return self.from_example(np.concatenate([self, other]), self)
        raise ValueError(
                'self and other must have the same sample frequency and sample duration')

    @classmethod
    def concat(cls, arrs, axis=0):
        freqs = set(x.frequency for x in arrs)
        if len(freqs) > 1:
            raise ValueError('all timeseries must have same frequency')

        durations = set(x.duration for x in arrs)
        if len(durations) > 1:
            raise ValueError('all timeseries must have same duration')

        return cls.from_example(np.concatenate(arrs, axis=axis), arrs[0])

    @property
    def samples_per_second(self):
        return int(Picoseconds(int(1e12)) / self.frequency)

    @property
    def duration_in_seconds(self):
        return self.duration / Picoseconds(int(1e12))

    @property
    def samplerate(self):
        return SampleRate(self.frequency, self.duration)

    @property
    def overlap(self):
        return self.samplerate.overlap

    @property
    def span(self):
        overlap = self.duration - self.frequency
        return TimeSlice((len(self) * self.frequency) + overlap)

    @property
    def end(self):
        return self.span.end

    def _ts_to_integer_indices(self, ts):
        if not isinstance(ts, TimeSlice):
            return ts

        diff = self.duration - self.frequency
        start_index = \
            max(0, np.floor((ts.start - diff) / self.frequency))
        end = self.end if ts.duration is None else ts.end
        stop_index = np.ceil(end / self.frequency)
        return slice(start_index, stop_index)

    def __getitem__(self, index):
        try:
            slices = map(self._ts_to_integer_indices, index)
        except TypeError:
            slices = (self._ts_to_integer_indices(index),)

        return super(ConstantRateTimeSeries, self).__getitem__(slices)

# @Time    : 2022/9/18 23:07
# @Author  : tk
# @FileName: simple_record.py
import json
import pickle
import typing
import numpy as np
import data_serialize
from tfrecords import TFRecordOptions,TFRecordCompressionType,TFRecordWriter,RECORD

__all__ = [
    "data_serialize",
    'pickle',
    'json',
    'RECORD',
    "DataType",
    "TFRecordOptions",
    "TFRecordCompressionType",
    "TFRecordWriter",
    "WriterObject",
    "StringWriter",
    "BytesWriter",
    "PickleWriter",
    "FeatureWriter",
    "NumpyWriter",
]

class DataType:
    int64_list = 0
    float_list = 1
    bytes_list = 2


class WriterObject:
    def __init__(self, filename, options=TFRecordOptions(compression_type='GZIP')):
        self.filename = filename
        self.options = options
        self.file_writer = TFRecordWriter(filename, options=options)

    def __del__(self):
        self.close()

    @property
    def get_writer(self):
        return self.file_writer

    def close(self):
        if self.file_writer is not None:
            self.file_writer.close()

    def write(self, data, *args, **kwargs):
        return self.file_writer.write(data)

    def write_batch(self,data, *args, **kwargs):
        return self.file_writer.write_batch(data)

    def flush(self):
        return self.file_writer.flush()

    def __enter__(self):
        if  self.file_writer is None:
            self.file_writer = TFRecordWriter(self.filename, options=self.options)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def write_index_for_RandomDataset(self,display=-1):
        from fastdatasets.record import load_dataset as Loader
        datasets = Loader.RandomDataset(self.filename,options=self.options)
        if display > 0:
            for i in range(len(datasets)):
                if (i + 1) % display == 0:
                    print(i, datasets[i])

class StringWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        return super(StringWriter, self).write(data)

    def write_batch(self, data,*args, **kwargs):
        return super(StringWriter, self).write_batch(data)

class BytesWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        return super(BytesWriter, self).write(data)

    def write_batch(self, data, *args, **kwargs):
        return super(BytesWriter, self).write_batch(data)

class PickleWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        return super(PickleWriter, self).write(pickle.dumps(data,*args,**kwargs))

    def write_batch(self, data, *args, **kwargs):
        return super(PickleWriter, self).write_batch([pickle.dumps(d,*args,**kwargs) for d in data])

class JsonWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        super(JsonWriter, self).write(json.dumps(data,*args,**kwargs))

    def write_batch(self, data, *args, **kwargs):
        return super(JsonWriter, self).write_batch([json.dumps(d,*args,**kwargs) for d in data])

class FeatureWriter(WriterObject):
    def write(self,data : typing.Dict,*args, **kwargs):
        assert data is not None
        dict_data = {}
        for k,v in data.items():
            val = v['data']
            if v['dtype'] == DataType.int64_list:
                dict_data[k] = data_serialize.Feature(int64_list=data_serialize.Int64List(value=val))
            elif v['dtype'] == DataType.float_list:
                dict_data[k] = data_serialize.Feature(float_list=data_serialize.FloatList(value=val))
            elif v['dtype'] == DataType.bytes_list:
                dict_data[k] = data_serialize.Feature(bytes_list=data_serialize.BytesList(value=val))
            else:
                raise Exception('bad dtype')

        feature = data_serialize.Features(feature=dict_data)
        example = data_serialize.Example(features=feature)
        return super(FeatureWriter, self).write(example.SerializeToString())

    def write_batch(self, data, *args, **kwargs):
        data_output = []
        for feature in data:
            dict_data = {}
            for k, v in feature.items():
                val = v['data']
                if v['dtype'] == DataType.int64_list:
                    dict_data[k] = data_serialize.Feature(int64_list=data_serialize.Int64List(value=val))
                elif v['dtype'] == DataType.float_list:
                    dict_data[k] = data_serialize.Feature(float_list=data_serialize.FloatList(value=val))
                elif v['dtype'] == DataType.bytes_list:
                    dict_data[k] = data_serialize.Feature(bytes_list=data_serialize.BytesList(value=val))
                else:
                    raise Exception('bad dtype')
            feature = data_serialize.Features(feature=dict_data)
            example = data_serialize.Example(features=feature)
            data_output.append(example.SerializeToString())
        return super(FeatureWriter, self).write_batch(data_output)



class NumpyWriter(WriterObject):
    def write(self,data : typing.Dict,*args, **kwargs):
        assert data is not None
        dict_data = {}
        for k, v in data.items():
            assert isinstance(v, np.ndarray) , 'assert error in {}'.format(k)
            if v.dtype.kind == 'i':
                value_key = 'int64'
                val = v.reshape((-1,)).tolist()
            elif v.dtype == np.float32:
                value_key = 'float32'
                val = v.reshape((-1,)).tolist()
            elif v.dtype == np.float or v.dtype == np.float64:
                value_key = 'float64'
                val = v.reshape((-1,)).tolist()
            elif v.dtype.kind == 'S':
                value_key = 'bytes'
                val = v.tobytes()
            else:
                raise Exception('bad dtype', k, v.dtype)
            kwargs_data = {
                "header": '',
                "dtype": str(v.dtype),
                "shape": list(v.shape),
                value_key: val,
            }
            dict_data[k] = data_serialize.NumpyObject(**kwargs_data)

        example = data_serialize.NumpyObjectMap(numpyobjects=dict_data)
        return super(NumpyWriter, self).write(example.SerializeToString())

    def write_batch(self, data: typing.List[dict], *args, **kwargs):
        data_output = []
        for feature in data:
            dict_data = {}
            for k, v in feature.items():
                assert isinstance(v, np.ndarray) , 'assert error in {}'.format(k)
                if v.dtype.kind == 'i':
                    value_key = 'int64'
                    val = v.reshape((-1,)).tolist()
                elif v.dtype == np.float32:
                    value_key = 'float32'
                    val = v.reshape((-1,)).tolist()
                elif v.dtype == np.float or v.dtype == np.float64:
                    value_key = 'float64'
                    val = v.reshape((-1,)).tolist()
                elif v.dtype.kind == 'S':
                    value_key = 'bytes'
                    val = v.tobytes()
                else:
                    raise Exception('bad dtype', k, v.dtype)
                kwargs_data = {
                    "header": '',
                    "dtype": str(v.dtype),
                    "shape": list(v.shape),
                    value_key: val,
                }
                dict_data[k] = data_serialize.NumpyObject(**kwargs_data)
            example = data_serialize.NumpyObjectMap(numpyobjects=dict_data)
            data_output.append(example.SerializeToString())
        return super(NumpyWriter, self).write_batch(data_output)




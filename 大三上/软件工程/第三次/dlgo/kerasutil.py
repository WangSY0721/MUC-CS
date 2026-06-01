from __future__ import absolute_import
import tempfile
import os

import h5py
import keras
import numpy as np
from keras.models import load_model, save_model


def save_model_to_hdf5_group(model, f):
    # 使用项目目录下的临时目录
    temp_dir = "temp_model_dir"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    tempfname = os.path.join(temp_dir, 'temp_model.h5')  # 指定文件路径

    # 保存模型到临时文件
    save_model(model, tempfname)

    # 将临时文件的二进制内容读入 numpy 数组
    with open(tempfname, 'rb') as tempf:
        model_data = np.frombuffer(tempf.read(), dtype='uint8')

    # 将模型数据保存到 HDF5 文件中
    f.create_dataset('model', data=model_data)

    # 删除临时文件和目录
    os.remove(tempfname)
    os.rmdir(temp_dir)


def load_model_from_hdf5_group(f, custom_objects=None):
    """
    Load a model from an HDF5 group or dataset, handling both cases.
    """
    tempfd, tempfname = tempfile.mkstemp(prefix='tmp-kerasmodel', suffix='.h5')
    try:
        os.close(tempfd)

        # 如果 f 是一个数据集（Dataset），直接保存到临时文件
        if isinstance(f, h5py.Dataset):
            with open(tempfname, 'wb') as tempf:
                tempf.write(f[()])  # 写入数据到文件
        # 如果 f 是一个组（Group），遍历其内容并写入到临时文件
        elif isinstance(f, h5py.Group):
            with h5py.File(tempfname, 'w') as serialized_model:
                for attr_name, attr_value in f.attrs.items():
                    serialized_model.attrs[attr_name] = attr_value
                for k in f.keys():
                    f.copy(k, serialized_model, k)
        else:
            raise TypeError(f"Unsupported HDF5 object type: {type(f)}")

        # 从临时文件加载模型
        return load_model(tempfname, custom_objects=custom_objects)
    finally:
        # 删除临时文件
        try:
            os.unlink(tempfname)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {tempfname}: {e}")



def set_gpu_memory_target(frac):
    """Configure Tensorflow to use a fraction of available GPU memory.

    Use this for evaluating models in parallel. By default, Tensorflow
    will try to map all available GPU memory in advance. You can
    configure to use just a fraction so that multiple processes can run
    in parallel. For example, if you want to use 2 works, set the
    memory fraction to 0.5.

    If you are using Python multiprocessing, you must call this function
    from the *worker* process (not from the parent).

    This function does nothing if Keras is using a backend other than
    Tensorflow.
    """
    if keras.backend.backend() != 'tensorflow':
        return
    # Do the import here, not at the top, in case Tensorflow is not
    # installed at all.
    import tensorflow as tf
    from keras.backend.tensorflow_backend import set_session
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = frac
    set_session(tf.Session(config=config))

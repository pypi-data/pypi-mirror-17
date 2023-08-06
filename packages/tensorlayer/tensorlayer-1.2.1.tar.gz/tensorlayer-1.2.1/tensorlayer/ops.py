#! /usr/bin/python
# -*- coding: utf8 -*-




import tensorflow as tf
import os
from sys import platform as _platform
from .layers import set_keep


def exit_tf(sess=None):
    """Close tensorboard and nvidia-process if available

    Parameters
    ----------
    sess : a session instance of TensorFlow
        TensorFlow session
    """
    text = "Close tensorboard and nvidia-process if available"
    sess.close()
    # import time
    # time.sleep(2)
    if _platform == "linux" or _platform == "linux2":
        print('linux: %s' % text)
        os.system('nvidia-smi')
        os.system('fuser 6006/tcp -k')  # kill tensorboard 6006
        os.system("nvidia-smi | grep python |awk '{print $3}'|xargs kill") # kill all nvidia-smi python process
    elif _platform == "darwin":
        print('OS X: %s' % text)
        os.system("lsof -i tcp:6006 | grep -v PID | awk '{print $2}' | xargs kill") # kill tensorboard 6006
    elif _platform == "win32":
        print('Windows: %s' % text)
    else:
        print(_platform)
    exit()

def clear_all(printable=True):
    """Clears all the placeholder variables of keep prob,
    including keeping probabilities of all dropout, denoising, dropconnect etc.

    Parameters
    ----------
    printable : boolean
        If True, print all deleted variables.
    """
    print('clear all .....................................')
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue
        if 'class' in str(globals()[var]): continue

        if printable:
            print(" clear_all ------- %s" % str(globals()[var]))

        del globals()[var]

# def clear_all2(vars, printable=True):
#     """
#     The :function:`clear_all()` Clears all the placeholder variables of keep prob,
#     including keeping probabilities of all dropout, denoising, dropconnect
#     Parameters
#     ----------
#     printable : if True, print all deleted variables.
#     """
#     print('clear all .....................................')
#     for var in vars:
#         if var[0] == '_': continue
#         if 'func' in str(var): continue
#         if 'module' in str(var): continue
#         if 'class' in str(var): continue
#
#         if printable:
#             print(" clear_all ------- %s" % str(var))
#
#         del var

def set_gpu_fraction(sess=None, gpu_fraction=0.3):
    """Set the GPU memory fraction for the application.

    Parameters
    ----------
    sess : a session instance of TensorFlow
        TensorFlow session
    gpu_fraction : a float
        Fraction of GPU memory, (0 ~ 1]

    References
    ----------
    `TensorFlow using GPU <https://www.tensorflow.org/versions/r0.9/how_tos/using_gpu/index.html>`_
    """
    print("  tensorlayer: GPU MEM Fraction %f" % gpu_fraction)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)
    sess = tf.Session(config = tf.ConfigProto(gpu_options = gpu_options))
    return sess











#

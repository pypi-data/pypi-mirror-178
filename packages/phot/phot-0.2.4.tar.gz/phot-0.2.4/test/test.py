import numpy as np
from numba import njit, prange
import jax
import jax.numpy as jnp
import torch

def loop_body(prev_i):
    a = jnp.array([1, 2, 3])
    a = jnp.fft.fft(a)
    return prev_i + 1, a


def g_inner_jitted(x, n):
    i = 0
    while i < n:
        i, a = loop_body(i)
    return x + i


@jax.jit
def test2():
    for i in range(1000):
        a = jnp.array([1, 2, 3, 4, 5, 6, 7, 10, 8, 8, 9, 9, 9, 342])
        a = jnp.fft.fft(a)

import os
import re
import subprocess
import sys
from pathlib import Path

if __name__ == '__main__':
    # print(g_inner_jitted(3, 1))
    # test2()
    # print('finished')
    print(os.fspath(Path("phot/csrc").resolve()))

#!/usr/bin/env python
"""
Based on https://github.com/danyaal/mandelbrot
Edited by jpdeleon on 2020-05-24 to include jit and argparse
See also https://rosettacode.org/wiki/Mandelbrot_set#Python
"""
import sys
import argparse
import time
import numpy as np
from numba import jit
import matplotlib.pyplot as plt

# counts the number of iterations until the function diverges or
# returns the iteration threshold that we check until
@jit
def countIterationsUntilDivergent(c, threshold):
    z = complex(0, 0)
    for iteration in range(threshold):
        z = (z*z) + c

        if abs(z) > 4:
            break
            pass
        pass
    return iteration

# takes the iteration limit before declaring function as convergent and
# takes the density of the atlas
# create atlas, plot mandelbrot set, display set
def mandelbrot(threshold, density, rlim=None, ilim=None, cmap='RdBu'):
    # location and size of the atlas rectangle
    if rlim is None:
        rlim=(-2.25, 0.75)
    if ilim is None:
        ilim=(-1.5, 1.5)
    #assert isinstance(rlim, tuple)
    #assert isinstance(ilim, tuple)
    realAxis = np.linspace(*rlim, density)
    imaginaryAxis = np.linspace(*ilim, density)
    realAxisLen = len(realAxis)
    imaginaryAxisLen = len(imaginaryAxis)

    # 2-D array to represent mandelbrot atlas
    atlas = np.empty((realAxisLen, imaginaryAxisLen))

    tic = time.perf_counter()

    # color each point in the atlas depending on the iteration count
    for ix in range(realAxisLen):
        for iy in range(imaginaryAxisLen):
            cx = realAxis[ix]
            cy = imaginaryAxis[iy]
            c = complex(cx, cy)

            atlas[ix, iy] = countIterationsUntilDivergent(c, threshold)
            pass
        pass
    toc = time.perf_counter()
    print(f"Runtime: {toc - tic:0.4f} sec")

    # plot and display mandelbrot set
    fig = plt.subplots(constrained_layout=True)
    plt.imshow(atlas.T, interpolation="nearest", cmap=cmap)
    plt.axis("off")
    plt.show()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="plot mandelbrot set")
    parser.add_argument("-t", "--threshold", type=int, help="threshold", default=100)
    parser.add_argument("-d", "--density", type=int, help="density", default=1000)
    parser.add_argument("-c", "--cmap", type=str, help="color map", default="RdBu")
    parser.add_argument("-z", "--zoom", action="store_true", help="zoom-in", default=False)
    parser.add_argument("-rlim", nargs=2, type=float, help="real axis limits", default=None)
    parser.add_argument("-ilim", nargs=2, type=float, help="imaginary axis limits", default=None)
    args = parser.parse_args()#(None if sys.argv[1:] else ["-h"])
    if args.zoom:
        rlim=(-0.22, -0.219)
        ilim=(-0.70, -0.699)
    else:
        rlim, ilim = None, None
    mandelbrot(args.threshold, args.density, cmap=args.cmap, rlim=rlim, ilim=ilim)

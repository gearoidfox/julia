# -*- coding: utf8 -*-
#
# Copyright 2017 Gearóid Fox
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
Plot the filled Julia set for given c
"""

from __future__ import division
from __future__ import print_function

import argparse
import math
import sys
import colorsys

import numpy
import scipy.misc
import scipy.ndimage



def f(z, c):
    """function to iterate
    
    f(z) = z^2 + c
    """
    return z*z + c;



def checkz(z, c, r, max_iter):
    """
    Check that function f(z) does not go to infinity within a set number
    of iterations, for a given starting value of z

    args:
        z (complex): inital value for z
        c (complex): iterate z^2 + c
        r (float):   cutoff absolute value for points that go in infinity
        max_iter (int) : maximum iterations to check

    returns:
        0 if z does f(z) does not go to infinity within max_iters iterations
         or
        n, the number of iterations at which |f^n(z)| > r
    """
    n = 1
    while n <= max_iter:
        z = f(z, c)
        if abs(z) > r: # goes to infinity
            return n
        n+= 1
    # doesn't go to infinity
    return 0



def main():
    # handle command line arguments
    description='Plot a filled Julia set.'
    epilog="""c must be specified as a Python complex variable, in the form
    x+yJ, e.g. 0+1J, 0.25-.5J, 1.
    \n
    If the real component is negative, quote c, and place a space character
    between the opening quote and the minus sign, e.g. ' -1+1J', to avoid 
    conflicts with command line argument parsing.

    \n

    The output image format is detected automatically from the file extension.
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('c', type=complex, help='complex constant')
    parser.add_argument('-i', '--iters', type=int, default=512,
            help='maximum number of iterations of f(z) for any z')
    parser.add_argument('-r', '--resolution', help='generate r*r bitmap',
            default=1000, type=int)
    parser.add_argument('-o', '--out', default='julia.png',
            help='output filename (default:julia.png')
    parser.add_argument('--colour', action='store_true', default='false',
            help='make a colour image')
    parser.add_argument('--offset', help='hue offset [0-1]', default=0.67,
            type=float)
    parser.add_argument('--smooth', help='apply smoothing to final image',
            action='store_true', default=False)
    args = parser.parse_args()


    # picture size:
    x_res = args.resolution
    y_res = args.resolution

    # plot boundaries: 
    (x0, x1, y0, y1) = (-2, 2, -2, 2)

    # max iterations of f(z) to check
    max_iter = args.iters

    c = args.c
    r = (1 + math.sqrt(1 + 4 * abs(c))) / 2

    # image array (rgb):
    pixels = numpy.zeros((y_res, x_res))

    for xpixel in range(x_res):
        for ypixel in range(y_res): 
            # calculate current initial z value:
            x = x0 + (x1 - x0) * xpixel / x_res
            y = y0 + (y1 - y0) * ypixel / y_res
            if y < 0:
                continue
            z = x + 1j * y
            pix = checkz(z, c, r, max_iter)
            pixels[ypixel, xpixel] = pix
            pixels[-ypixel, -xpixel] = pix
    

    # color image
    if args.colour is True:
        hue_offset = args.offset
        pixels = numpy.divide(pixels, numpy.amax(pixels))
        colour_pixels = numpy.zeros((y_res, x_res, 3))
        for xpixel in range(x_res):
            for ypixel in range(y_res): 
                if pixels[ypixel, xpixel] == 0:
                    colour_pixels[ypixel, xpixel] = [0, 0, 0]
                else:
                    hue = pixels[ypixel, xpixel] + hue_offset
                    if hue > 1:
                        hue -= 1
                    col = colorsys.hsv_to_rgb(hue, 1, 0.5)
                    colour_pixels[ypixel, xpixel] = col
        pixels = colour_pixels

    # smooth image
    if args.smooth is True:
        pixels = scipy.ndimage.filters.gaussian_filter(pixels, 1)

    # write image
    pixels = numpy.flipud(pixels)
    scipy.misc.imsave(args.out, pixels)

if __name__=="__main__":
    sys.exit(main())

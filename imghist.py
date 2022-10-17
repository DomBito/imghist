#!/usr/bin/python3
import sys
import numpy as np
import cv2
import os.path
import argparse
import warnings

def plot_hist(hist):
    import matplotlib.pyplot as plt
    r,g,b = hist[1]
    plt.fill_between(np.arange(256),r,facecolor="#d53d36")
    plt.fill_between(np.arange(256),g,facecolor="#008b00")
    plt.fill_between(np.arange(256),b,facecolor="#6e69e9")
    plt.fill_between(np.arange(256),np.minimum(r,g),facecolor="#3d3d1c")
    plt.fill_between(np.arange(256),np.minimum(b,g),facecolor="#004343")
    plt.fill_between(np.arange(256),np.minimum(b,r),facecolor="#4d324d")
    plt.fill_between(np.arange(256),np.minimum(np.minimum(r,g),b),facecolor="#212121")
    plt.show()

def add2hist(img=None,hist=None):
    if hist is None:
        hist = [0,np.zeros([3,256])]
    if img is None:
        img = [[[np.inf,np.inf,np.inf]]]
        imglen = 0
    else:
        imglen = np.size(img)/3
    blue,green,red = np.moveaxis(img,-1,0)
    r,rbins = np.histogram(red  ,np.arange(257)-0.5)
    g,gbins = np.histogram(green,np.arange(257)-0.5)
    b,bbins = np.histogram(blue ,np.arange(257)-0.5)
    total = imglen + hist[0]
    w0 = hist[0]/total
    w1 = imglen/total
    hist[1] = hist[1]*w0 + np.asarray([r,g,b])*w1
    hist[0] = total
    return hist

def makeimg(hist,size):
    if hist[0] == 0:
        sys.exit("\nYou must have a non-empty histogram to make an image.\n")
    else:
        freq = hist[1]
        n = size*size
        m = np.sum(freq,1)
        freq[0] = np.rint(freq[0]*(n/m[0]))
        freq[1] = np.rint(freq[1]*(n/m[1]))
        freq[2] = np.rint(freq[2]*(n/m[2]))
        m = np.sum(freq,1)
        diff = (n - m).astype(int)
        order = np.argsort(freq)
        if np.abs(diff[0]) > 0:
            freq[0][order[0,-np.abs(diff[0]):]] += np.sign(diff[0])*np.ones(np.abs(diff[0]))
        if np.abs(diff[1]) > 0:
            freq[1][order[1,-np.abs(diff[1]):]] += np.sign(diff[1])*np.ones(np.abs(diff[1]))
        if np.abs(diff[2]) > 0:
            freq[2][order[2,-np.abs(diff[2]):]] += np.sign(diff[2])*np.ones(np.abs(diff[2]))
        freq = freq.astype(int)
        img = [[],[],[]]
        for i in range(256):
            for j in range(3):
                img[j] = img[j] + (i*np.ones(freq[2-j,i])).tolist()
        img = np.reshape(np.moveaxis(img,0,-1),(size,size,3))
        cv2.imwrite("histimg.png", img)


parser = argparse.ArgumentParser(description="Make histograms of images.")
parser.add_argument('-i','--input',
                    dest='imgfile',default="",
                    type=str,
                    help='Image input file.')
parser.add_argument('-o', '--output',
                    dest='histfile', default="hist.npz",
                    type=str,
                    help='Histogram output file. If a histogram file already exists, it will add information to said histogram.')
parser.add_argument('-p', '--plot',
                    dest='plot', default=False, const=True,
                    action='store_const',
                    help='Plot the histogram.')
parser.add_argument('-d', '--draw_image',
                    dest='draw', default=False, const=True,
                    action='store_const',
                    help='Make an image whose histogram matches your histogram file (accuracy depends on the size of the image).')
parser.add_argument('-q', '--quiet',
                    dest='isquiet', default=False, const=True,
                    action='store_const',
                    help="Don't print messages.")
parser.add_argument('-s', '--size',
                    dest='size', default=600,
                    type=int,
                    help='Size of the image when the option -d is set.')
args = parser.parse_args()

if args.histfile[-4:] == ".npz":
    histfile = args.histfile
else:
    histfile = args.histfile + ".npz"

if os.path.isfile(histfile):
    if os.path.isfile(args.imgfile) and not args.isquiet:
        print("Adding information to the pre-existing histogram!")
    hist = np.load(histfile)
    hist = [hist['arr_0'],hist['arr_1']]
else:
    hist = [0,np.zeros([3,256])]

if not args.imgfile:
    img = None
else:
    img = cv2.imread(args.imgfile)
    hist = add2hist(img,hist)
    np.savez(histfile,hist[0],hist[1])

if args.draw:
    makeimg(hist,args.size)

if args.plot:
    plot_hist(hist)

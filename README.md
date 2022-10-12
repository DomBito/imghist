# imghist
Tool for creating and plotting histograms of images.

```
usage: imghist.py [-h] [-i IMGFILE] [-o HISTFILE] [-p] [-d] [-s SIZE]

Make histograms of images.

options:
  -h, --help            show this help message and exit
  -i IMGFILE, --input IMGFILE
                        Image input file.
  -o HISTFILE, --output HISTFILE
                        Histogram output file. If a histogram file already exists, it will add
                        information to said histogram.
  -p, --plot            Plot the histogram.
  -d, --draw_image      Make an image whose histogram matches your histogram file (accuracy depends
                        on the size of the image).
  -s SIZE, --size SIZE  Size of the image when the option -d is set.
```

**TIP**: The `-d` flag is useful if you want to do a histogram-based image manipulation to affect a whole video clip or multiple images. If you have, say, a part of a movie for which you want to change its global histogram, then you can export multiple frames of it and get one single histogram for them.

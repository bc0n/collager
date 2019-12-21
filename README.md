# collager
collager.py stacks images found in the given directory into a slideshow.

## Usage:
```
python collager.py directory   width height secPerFrame pictureSizeFactor
python collager.py ./pictures/ 500   500    1           0.3
```
See collager.avi for a small sample.
[![collager sample video]({framesnap.png})]({collager.avi} "collager.avi")

Images under ./pictures/ are CC BY-NC 2.0 from SpaceX's CRS-5 mission https://www.flickr.com/photos/spacex/albums/72157650676154467/with/16511916838/

## Requirements:
* cv2
* glob
* numpy
* sys
* re



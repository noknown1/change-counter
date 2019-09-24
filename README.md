# Change Counter

 Change Counter is a fast way count up all of your loose change. Powered by Open-CV for Python. 

### How to Use

To use the program, you'll first need to take an picture of your loose change. This must be done in a specific way if you want accurate results:
- Arrange all of your coins so they lay flat on some level surface (no coins are allowed to overlap, and for best results, they should not touch either.
- A photo should be taken from directly above, ideally capturing only the coins and nothing else (i.e. the frame of the image should be entirely filled with coins).
- The image taken needs to be to be completely parallel to the plane the coins rest on. The image should be directly 'head-on', meaning the coins should have clear circular shapes, not ovoid ones. 
- Finally, for best results place the coins on a surface that gives good contrast against them. 

Once you have a picture uploaded to your computer, simply run the program and load it in by pressing "***File/Load Image***" in the menu bar. You should see the image you took in the program's preview box. Next, press run to process the image. The program should do this quickly and show you the output image (a grey-scale version of your image with overlays circling the coins that were found), as well as the total and individual coin counts.

### Dependencies

- Open-CV
- PIL/Pillow
- Numpy

### Accuracy

There are many factors that will effect the accuracy of the program. 
1) Lighting: Dark coins on a dark background will be hard to detect. The background should have a high contrast to all the coins.
2) Photo Angle: Ideally, the shape of each coin in the image should be a perfect circle. If an image is taken of the coins at any sort of angle, it will cause the coin shapes to become ovals, which will cause trouble for the Hough-Circle's algorithm.

### Advanced Settings

Advanced settings are available in the drop down menu.

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

Advanced settings are available in the drop down menu, these include:

Two threshold paramters passed into Open-CV's HoughCircle function (see https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_circle/hough_circle.html for more details):
- edge detection threshold: Larger values will be more strict on whether or not an edge is an edge.
- circle threshold: This value

Two error acceptance percentages used to figure out what type of coin a circle is:
- small error acceptance: Used to differentiate between small coins, i.e. dimes and pennies.
- large error acceptance: Used to differentiate between larger coins, i.e. quarters and nickles.

One overall performance parameter:
- resize percentage: this is the percentage the image will be scaled down to in order to get better performance. Using the program on very large images may make it run very slow. It's recommended to keep this value around 30% for pictures from modern smartphones. For smaller images, it is okay to use a high percentage.

### Getting Good Results

For some images, the program will work perfectly with default values. Sometimes, you will need to edit the advanced parameters and click run agian to get good results. Below is a list of tips/steps to take to get an accurate reading. In the future this should all be automated, but for now you will need to do some manual edits to some values.
1) Coins no being circled: If the image shows zero circles detected, you need to decrease the edge threshold. Do this until all coins in the images have circles around them (it's okay if the coin type is undetected at this point).
2) Incorrect, non existiant circles showing up: Usually, lowering the threshold to detect all circles results in many false readings, often times many very extreme sized circles compaired to the coins. At this point, you should increase the circle threshold. Eventully, the program will stop these false circles.
3) Coin types are wrong: If the coin types are incorrect, or there are blue 'unknown' circles around some coins, you need to edit the error acceptance percentages. Making these larger will increase the error that's allowed between the detected coins and the coins actual known size. Decreasing it makes the error smaller. To get rid of blue 'unknown' circles, increasing the percentages give the circle a better change to be placed in a category. The small error value controls the acceptance error for pennies and dimes, while the large error value controls it for quarters and nickels. Look at the image and see what coins are being detected incorrectly, and use that to decide which one to change.
4) Program still gives incorrect results for some reason: If you need the program to be very accurate, I recommend taking multiple images of same set of coins. The coins in the image should stay the same, but rearrange them each image. This way, you are much more likely to get a configuration of coins that just happens to work well with the program. It will also allow you to get a better general idea of what the real value should be around, or give you the chance to average all results into one value.





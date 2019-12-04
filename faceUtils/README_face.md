
## Usage and Library Requirements

The command works as follows:

!face link_to_an_image

!face can detect multiple faces in an image.

For testing purposes, the following libraries are required (Python3):

- OpenCV
	- pip install opencv-python
	- imported as cv2
- NumPy
	- pip install numpy
	

## Known Bugs/Issues:	

- Age predicition isn't consistently accurate
- Identity prediciton is very innacurate. Most often, a face linked will be identified as Becky_Bayless

## Neural Network Model Data Used

I want to note that due to the nature of the command, having to use neural network libraries, there is a folder named faceUtils that contains files needed for the NN/face.py to do its job.

The files contain models that have been trained to detect human faces:

- age_net.caffemodel
- deploy_age.prototxt
- deploy_gender.prototxt
- gender_net.caffemodel
- haarcascade_frontalface_alt2.xml
- identity_meta.csv
- senet50_256.prototxt
- senet50_256.caffemodel

Two of these files (the .caffemodel files):

- age_net.caffemodel
- gender_net.caffemodel

are very large in size, each nearly 50mb in size. These files are used to help detect age and gender.

The age and gender files can be obtained from here:

- https://github.com/GilLevi/AgeGenderDeepLearning
or
- https://talhassner.github.io/home/publication/2015_CVPR

A third .caffemodel file

- senet50_256.caffemodel

the one used for guessing identity, has been omitted because it is >100 mb, above the limit github allows to be uploaded.

senet50_256.caffemodel can be obtained at:

- https://github.com/ox-vgg/vgg_face2
- search for "SE-ResNet-50-256D" and click on the Caffe model link
- add it to the faceUtils directory

---

VGGFace2 Citation:

Q. Cao, L. Shen, W. Xie, O. M. Parkhi, A. Zisserman  
VGGFace2: A dataset for recognising face across pose and age  
International Conference on Automatic Face and Gesture Recognition, 2018.
Bibtex | Abstract | [PDF](http://www.robots.ox.ac.uk/~vgg/publications/2018/Cao18/cao18.pdf)
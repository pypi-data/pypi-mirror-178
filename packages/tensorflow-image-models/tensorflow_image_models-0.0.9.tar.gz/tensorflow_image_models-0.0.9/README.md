Install<br />

pip install tensorflow_image_models==0.0.9

----------------------------------------------

Usage<br />

from tensorflow_image_models import list_models<br />

list_models()<br />

models list:<br />
DPN92<br />
DPN98<br />
DPN131<br />
DPN107<br />
EfficientNetB0<br />
EfficientNetB1<br />
.....<br />
.....<br />
VGG16<br />
VGG19<br />

Create Model<br />

from tensorflow_image_models import EfficientNet<br />
model = EfficientNet.EfficientNetB0(classes=10)<br />
model.summary()


from tensorflow_image_models import Inception<br />
model = Inception.InceptionV4(classes=3, input_shape=(299,299,3)<br />
model.summary()

----------------------------------------------

Here is a list of input shape expected for each model

EfficientNetB0-----(224, 224, 3)<br />
EfficientNetB1-----(240, 240, 3)<br />
EfficientNetB2-----(260, 260, 3)<br />
EfficientNetB3-----(300, 300, 3)<br />
EfficientNetB4-----(380, 380, 3)<br />
EfficientNetB5-----(456, 456, 3)<br />
EfficientNetB6-----(528, 528, 3)<br />
EfficientNetB7-----(600, 600, 3)<br />
AlexNet------------(224, 224, 3)<br />
InceptionResNetV2--(299, 299, 3)<br />
InceptionV3--------(299, 299, 3)<br />
LeNet--------------(32,  32,  1)<br />
MobileNetV2--------(224, 224, 3)<br />
ResNet18-----------(224, 224, 3)<br />
ResNet34-----------(224, 224, 3)<br />
VoVNet27-----------(224, 224, 3)<br />
VoVNet39-----------(224, 224, 3)<br />
VoVNet57-----------(224, 224, 3)<br />


The rest of the models receive any shape, and the default shape is (128,128,3)

----------------------------------------------

License<br />
This project is licensed under the MIT License

----------------------------------------------

Author<br />
DEEPOLOGY LAB

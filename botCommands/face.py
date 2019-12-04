import discord
from discord.ext import commands
import cv2
import csv
import numpy as np
from urllib.request import urlopen


def url_to_image(self):
    # download the linked image, convert it to a NumPy array,
    # and then read it into OpenCV format
    resp = urlopen(self)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


class Face(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='face')
    async def face(self, ctx, *, link=None):
        if link is None:
            await ctx.send('Please provide a linked image: !face <link>')
        else:
            print('Loading models...\n')
            await ctx.send('Calculating...\n')

            # Pre trained Convolutional Neural Network (CNN) models
            # obtained from Gil Levi and Tal Hassner (age, gender)
            # and from VGGFace2 (identity)
            age_net = cv2.dnn.readNetFromCaffe(
                'faceUtils/deploy_age.prototxt',
                'faceUtils/age_net.caffemodel')
            gender_net = cv2.dnn.readNetFromCaffe(
                'faceUtils/deploy_gender.prototxt',
                'faceUtils/gender_net.caffemodel')
            identity_net = cv2.dnn.readNetFromCaffe(
                'faceUtils/senet50_256.prototxt',
                'faceUtils/senet50_256.caffemodel')

            # mean values for age and gender obtained from sources named above
            MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

            # mean values for identity
            MODEL_MEAN_VALUES_2 = (91.4953, 103.8827, 131.0912)

            # labels
            age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
            gender_list = ['Male', 'Female']

            # from identity_meta.csv
            Class_ID = []
            Name = []
            Sample_Num = []
            Flag = []
            Gender = []
            # read identity_meta.csv into an array, obtain celeb names
            with open('faceUtils/identity_meta.csv', encoding="utf8") as csvDataFile:
                data = csv.reader(csvDataFile)
                data_list = [Class_ID, Name, Sample_Num, Flag, Gender]
                for row in data:
                    Class_ID.append(row[0])
                    Name.append(row[1])
                    Sample_Num.append(row[2])
                    Flag.append(row[3])
                    Gender.append(row[4])
                identity_list = data_list[1]

            # Trained Haar classifier cascade used to identify human faces
            face_cascade = cv2.CascadeClassifier('faceUtils/haarcascade_frontalface_alt2.xml')

            # read the image from the link
            img = url_to_image(link)

            # convert and read the image as a gray-scale image
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # detect the number of faces
            faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=8)
            print("Number of faces detected: {}\n".format(len(faces)))
            await ctx.send('Number of faces detected: {}'.format(len(faces)))
            if len(faces) == 0:
                await ctx.send('No face detected, please try a different picture')

            for x, y, w, h in faces:
                # create rectangular box around each face detected
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                face_img = img[y:y + h, x:x + w].copy()

                # pass the mean values to the image to pre-process the image
                # so it can be passed to the model for prediction
                blobAgeGender = cv2.dnn.blobFromImage(face_img, 1, (227, 227), swapRB=False)
                blobIdentity = cv2.dnn.blobFromImage(face_img, 1, (227, 227), swapRB=False)

                # Predict age
                age_net.setInput(blobAgeGender)
                age_predictions = age_net.forward()
                print("Age Prediction: {}".format(age_predictions))
                age = age_list[age_predictions[0].argmax()]
                print("Age Range: {}".format(age))
                # await ctx.send('Age Range: {}'.format(age))

                # Predict gender
                gender_net.setInput(blobAgeGender)
                gender_predictions = gender_net.forward()
                print("Gender Prediction: {}".format(gender_predictions))
                gender = gender_list[gender_predictions[0].argmax()]
                print("Gender: {}".format(gender))
                # await ctx.send('Gender: {}'.format(gender))

                # Predict identity/look-alike
                identity_net.setInput(blobIdentity)
                identity_predictions = identity_net.forward()
                identity = identity_list[identity_predictions[0].argmax()]
                print("Identity or Celebrity Look Alike: {}".format(identity))
                # await ctx.send('Identity or Celebrity Look Alike: {}'.format(identity))

                # create embeded card for each face detected for easier information reading
                embed = discord.Embed(colour=0x9c0101, description=f"Age: {age}\n"
                                                                   f"Gender: {gender}\n"
                                                                   f"Identity or Celebrity Look Alike: {identity}")
                embed.set_author(icon_url=ctx.me.avatar_url_as(format='png'), name="Estimated Face Information")
                await ctx.send(embed=embed)
                await ctx.send("...\n")


def setup(bot):
    bot.add_cog(Face(bot))

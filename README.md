# Reconstruction-of-Satellite-Images

Good Evening Sir, I am Vaishali Chauhan both are trying to explain the working of our project through github medium.

## Whenever user opens the application below is the interface which would be the first preview for a person

![Screenshot from 2020-06-25 15-11-00](https://user-images.githubusercontent.com/39858354/100092756-983eb180-2e7c-11eb-8e90-ec300c9de5e9.png)

## Now after clicking on the browse button user would upload his/her distorted Image.
After clicking on the start processing button first the Image would be changed to 256\*256\*3 size and **model** at the backend will be invoked and processing would get start.

## Now as the processing part is done there would come a pop-up to save the Image which would be our Final Image.
![Screenshot from 2020-06-22 16-26-52](https://user-images.githubusercontent.com/39858354/100093375-73970980-2e7d-11eb-9ce0-6d0096b0214f.png)

Now above explaination is all about what will happen at **the end of user perspective**.

# Now what is happening in backend??

## Below is the Low level Data Flow Diagram which is representing the basic architecture..
![Project_Report_UE178010_UE1731141](https://user-images.githubusercontent.com/39858354/100094197-a55ca000-2e7e-11eb-9f40-e498a1c8e555.jpg)

![naveen](https://user-images.githubusercontent.com/39858354/100094591-44819780-2e7f-11eb-9188-1c5ed14d6227.jpg)

### Above Image is showing the how the whole project works when it is connected with the frontend as well.

1. We have prepared the data by downloading some of the sample Images from the Internet and prepared Its masks by using the photoshop..

Below are samples of the Data
Input Image                |   Created Mask           
:-------------------------:|:-------------------------:
![a6](https://user-images.githubusercontent.com/39858354/100095155-151f5a80-2e80-11eb-8cc8-2b3bf7e8e5e0.jpg) | ![a6_3GT](https://user-images.githubusercontent.com/39858354/100095174-1b153b80-2e80-11eb-9fc7-d82e1a0e1e2b.png)
Input Image                |   Created Mask           
:-------------------------:|:-------------------------:
![a14](https://user-images.githubusercontent.com/39858354/100095202-223c4980-2e80-11eb-8127-bcd6d03dd321.jpg) | ![a14_3GT](https://user-images.githubusercontent.com/39858354/100095217-28cac100-2e80-11eb-9b05-76f3b8cf303a.png)
Input Image                |   Created Mask           
:-------------------------:|:-------------------------:
![B5](https://user-images.githubusercontent.com/39858354/100095241-33855600-2e80-11eb-86ca-89cfe4193a3d.jpg) | ![B5_3GT](https://user-images.githubusercontent.com/39858354/100095259-397b3700-2e80-11eb-935b-10bd932df250.png)

Whole data is uploaded in the **app folder** in the repository.

Now model is trained over the 53 pages of the above type for which UNet Model is used to generate predict the masked Image of the Input Image.
Now one thing is why we are interested in the geneartion of mask then answer of this question is that there is the Image Inpainting algorithm which is being provided by the OpenCv library which is widely used algorithm in the reconstruction of Images.
This algorithm takes three arguments as Input **a)** Distorted Image, **b)** Masked Image (White area represents the distorted pixels), **c)** Location at which we have to save the Image.

Our **UNet Model would do this work for the generation of masked Images from the Input Images (Distorted Images)**.

Below is the **Architecture of UNet we are using the five layers in this (5 for down and 5 for up)**
![Project_Report_UE178010_UE173114](https://user-images.githubusercontent.com/39858354/100097436-852ee000-2e82-11eb-99b6-a14f9bfa4d1f.jpg)

## Now after this our Mask Image would be generated and we will pass this masked Image as well as Input Image to the Inpainting Algorithm and It would return us the Processed Image.

#Results which we are getting after doing this
Input Image                |  Predicted Mask           | Processing GIF           | Output Image
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
![t11](https://user-images.githubusercontent.com/39858354/89610240-a5b53900-d897-11ea-96f6-a180734735c8.jpg) | ![mask_t11](https://user-images.githubusercontent.com/39858354/89610250-a9e15680-d897-11ea-96fd-713aae266cf3.jpg) | ![t11](https://user-images.githubusercontent.com/39858354/89610146-70105000-d897-11ea-88ea-1b8649ca85db.gif) | ![t12](https://user-images.githubusercontent.com/39858354/89610317-ce3d3300-d897-11ea-9b8a-19ce9f90c0f3.jpg)

Input Image                |  Predicted Mask           | Processing GIF           | Output Image
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
![t1](https://user-images.githubusercontent.com/39858354/89976409-fd7fe580-dc85-11ea-9626-adade30dc37d.jpg) | ![mask_t1](https://user-images.githubusercontent.com/39858354/89976421-053f8a00-dc86-11ea-8640-28c93b764981.jpg) | ![ezgif com-optimize](https://user-images.githubusercontent.com/39858354/89976499-315b0b00-dc86-11ea-8224-b6c9418987cc.gif) | ![t1](https://user-images.githubusercontent.com/39858354/89976475-21432b80-dc86-11ea-95d6-e3d1c70e8ed9.jpg)



## Now How we are getting this GIF.
To save this gif we have downloaded the code of the Image Inpainting algorithm and made some changes into that and as the pixel by pixel Image is being updated we are saving it into our Folder which is named as Patches (There would be a internal folder which would be having same name as the Image is having and Inside that there are Intermediate results).
Below are some snapshots of the folder
![Screenshot from 2020-11-24 18-33-58](https://user-images.githubusercontent.com/39858354/100098180-ae03a500-2e83-11eb-9467-fe80aeb190d8.png)

## For folder t21 (Which is name of the Image)
![Screenshot from 2020-11-24 18-36-04](https://user-images.githubusercontent.com/39858354/100098378-f91db800-2e83-11eb-8f0d-eed7804fdc86.png)
![Screenshot from 2020-11-24 18-35-59](https://user-images.githubusercontent.com/39858354/100098382-fa4ee500-2e83-11eb-9e1a-fe601ef07d48.png)

This is all Sir what we have done and currently we are studying Deep Learning and Internal Concepts as suggested by you Sir.

Thank you Sir.







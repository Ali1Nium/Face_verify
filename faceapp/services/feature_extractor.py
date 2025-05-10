# # feature_extractor.py
# import tensorflow as tf
# from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
# from tensorflow.keras.preprocessing import image
# import numpy as np

# # model = model.load_weights()
# model = ResNet50(weights='imagenet', include_top=False)

# model = ResNet50(weights=None, include_top=False)
# model = ResNet50(weights="imagenet", include_top=False, pooling='avg')

# model.load_weights("/home/fallah/Videos/Face_verify/faceapp/models/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5")
# def extract_features(image_path: str):
#     img = image.load_img(image_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = preprocess_input(img_array)
#     features = model.predict(img_array)
#     return features[0].tolist()


import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
import numpy as np

# بارگذاری مدل VGG16 با وزن‌های پیش‌ساخته از ImageNet
# model = VGG16(weights='imagenet', include_top=False)
model = VGG16(weights='/home/fallah/Videos/Face_verify/faceapp/models/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5', include_top=False)

async def extract_features(image_path: str):
    print("we aer here")
    # بارگذاری تصویر
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # پیش‌پردازش تصویر برای تطابق با ورودی مدل
    img_array = tf.keras.applications.vgg16.preprocess_input(img_array)
    
    # استخراج ویژگی‌ها
    features = model.predict(img_array)
    
    # برگرداندن ویژگی‌ها به صورت لیست
    return features[0].tolist()

import numpy as np
import cv2
from insightface.app import FaceAnalysis


class VerificationInsightFaceServices():

    def __init__(self, model_name="buffalo_l"):
        self.model = FaceAnalysis(name=model_name)
        self.model.prepare(ctx_id=0, det_size=(640, 640))


    def add_background_image(self, selfie_image_path):
        # print("selfie_image_path=", selfie_image_path)

        # with Image.open(selfie_image_path) as img:
        #     selfie_image = np.array(img)                                                     
        selfie_image = cv2.imread(selfie_image_path)
        # print("type image = ",type(selfie_image))


        background_height = selfie_image.shape[0] + 400  # Add space to the top and bottom
        background_width = selfie_image.shape[1] + 400  # Add space to the left and right
        background_color = (150, 1, 2)  # Blue color
        background_image = np.full((background_height, background_width, 3), background_color, dtype=np.uint8)

        x_offset = (background_width - selfie_image.shape[1]) // 2
        y_offset = (background_height - selfie_image.shape[0]) // 2

        background_image[y_offset:y_offset + selfie_image.shape[0], x_offset:x_offset + selfie_image.shape[1]] = selfie_image
        return background_image

    def get_face_embedding(self, img_input):
        if isinstance(img_input, str):
            img = cv2.imread(img_input)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
        faces = self.model.get(img_rgb)
        if len(faces) == 0:
            print(f"No face detected in the image.")
            return None

        embedding = faces[0].embedding
        # Apply L2 normalization
        norm_embedding = embedding / np.linalg.norm(embedding)
        return norm_embedding

    def compare_faces(self, id_image_path, selfie_image_path, threshold=0.50):
        selfie_background_img = self.add_background_image(selfie_image_path)
        id_embedding = self.get_face_embedding(id_image_path)
        selfie_embedding = self.get_face_embedding(selfie_background_img)

        if id_embedding is None:
            return "No face found in the ID image."
        if selfie_embedding is None:
            return "No face found in the selfie image."

        # Compute cosine similarity
        cosine_similarity = np.dot(id_embedding, selfie_embedding)
        print("cosine_similarity", cosine_similarity)
        if cosine_similarity > threshold:
            return True
        else:
            return False
        
    def compare_embeddings(self, db_vector: np.ndarray, selfie_path: str, threshold=0.5):
        """
        Compare the given db_vector (from the database) with the face embedding
        extracted from the selfie image at the given selfie_path.

        :param db_vector: Face vector from the database.
        :param selfie_path: Path to the selfie image for comparison.
        :param threshold: Minimum similarity score to consider as a match.
        :return: Cosine similarity score between the two face embeddings.
        """
        # استخراج ویژگی‌ها از تصویر سلفی
        selfie_vector = self.get_face_embedding(selfie_path)

        if selfie_vector is None:
            print("hi")

        # محاسبه شباهت بین ویژگی‌های دیتابیس و سلفی
        cosine_similarity = np.dot(db_vector, selfie_vector)

        # اگر شباهت از threshold بیشتر بود، تطابق در نظر گرفته می‌شود
        if cosine_similarity > threshold:
            return cosine_similarity
        else:
            return 0.0  # اگر شباهت کمتر از threshold بود، هیچ تطابقی وجود ندارد

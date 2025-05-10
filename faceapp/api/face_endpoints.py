# from django.http import JsonResponse
# from ninja.errors import HttpError
# from ninja_extra import api_controller, http_post
# from ninja import File
# from ninja.files import UploadedFile
# import numpy as np
# from faceapp.schemas.face_endpoints_schema import FaceRegistrationSchema
# from faceapp.models import FaceDetail
# from django.core.files.base import ContentFile
# import uuid
# import logging
# from asgiref.sync import sync_to_async
# from scipy.spatial.distance import cosine
# from faceapp.services.feature_extractor import extract_features
# from faceapp.services.img_handler import handle_file_upload
# from faceapp.exceptions import (
#     ImageProcessingError, FeatureExtractionError,
#     FileUploadError, DatabaseOperationError
# )
# import uuid
# import numpy as np
# import json
# from faceapp.services.insightface_service import VerificationInsightFaceServices

# logger = logging.getLogger(__name__)


# def error_response(message: str, status: int = 400):
#     return JsonResponse(
#         {"result": {}, "exception": message},
#         status=status
#     )


# @api_controller("/person", tags=["Person"])
# class PersonController:

# # کد ذخیره‌سازی ویژگی‌ها:
#     @http_post("/add", url_name="add_person")
#     async def add_person(
#         self,
#         data: FaceRegistrationSchema,
#         image: UploadedFile = File(...),
#     ):
#         try:
#             if not image:
#                 raise FileUploadError("No image uploaded.")

#             try:
#                 local_path = await handle_file_upload(image)
#             except Exception as e:
#                 raise FileUploadError(f"Error during file upload: {str(e)}")

#             filename = f"{uuid.uuid4()}.jpg"
#             content = await sync_to_async(image.read)()
#             file_content = ContentFile(content, name=filename)

#             try:
#                 vector = await extract_features(local_path)

#                 # بررسی نوع داده‌ها و تبدیل به رشته JSON
#                 if isinstance(vector, list):  # اگر خروجی یک لیست است
#                     vector_str = json.dumps(vector)  # تبدیل به JSON
#                 else:
#                     raise FeatureExtractionError("Unexpected vector type, expected a list.")

#             except Exception as e:
#                 raise FeatureExtractionError(f"Error during feature extraction: {str(e)}")

#             try:
#                 # ذخیره‌سازی ویژگی‌ها به همراه اطلاعات دیگر شخص
#                 person = await FaceDetail.objects.acreate(
#                     first_name=data.name, last_name=data.lastName, face_vector=vector_str
#                 )
#                 await person.asave()

#             except Exception as e:
#                 raise DatabaseOperationError(f"Error creating record in database: {str(e)}")

#             return JsonResponse(
#                 {
#                     "result": {
#                         "id": person.id,
#                         "name": person.first_name,
#                         "surname": person.last_name,
#                     },
#                     "exception": "",
#                 },
#                 status=201,
#             )

#         except FileUploadError as e:
#             logger.error(str(e))
#             return error_response(str(e), status=400)

#         except (ImageProcessingError, FeatureExtractionError) as e:
#             logger.error(str(e))
#             return error_response(str(e), status=422)

#         except DatabaseOperationError as e:
#             logger.error(str(e))
#             return error_response("A database error occurred.", status=500)

#         except Exception as e:
#             logger.exception("Unexpected error")
#             return error_response("An unexpected error occurred.", status=500)


#     # کد شناسایی ویژگی‌ها و مقایسه:
#     @http_post("/identify", url_name="identify_face")
#     async def identify_face(self, image: UploadedFile = File(...)):
#         try:
#             if not image:
#                 raise FileUploadError("No image uploaded.")

#             try:
#                 local_path = await handle_file_upload(image)
#             except Exception as e:
#                 raise FileUploadError(f"Error while uploading file: {str(e)}")

#             # استفاده از InsightFace برای استخراج بردار ویژگی
#             insight_service = VerificationInsightFaceServices()
#             input_vector = await sync_to_async(insight_service.get_face_embedding)(local_path)

#             if input_vector is None:
#                 raise FeatureExtractionError("No face detected in the uploaded image.")

#             all_faces = await sync_to_async(list)(FaceDetail.objects.exclude(face_vector=""))

#             if not all_faces:
#                 raise HttpError(404, "No faces registered in the database.")

#             closest_match = None
#             highest_similarity = -1

#             for face in all_faces:
#                 try:
#                     # تبدیل ویژگی‌های ذخیره‌شده از رشته JSON به آرایه numpy
#                     db_embedding = np.array(json.loads(face.face_vector))

#                     # تبدیل input_vector به آرایه numpy
#                     input_vector = np.array(input_vector)

#                     # مقایسه بردارها با استفاده از np.all() یا np.any()
#                     similarity = np.dot(db_embedding, input_vector)
#                     print("similarity", similarity)
#                     if np.any(similarity > 0.10):  # یا می‌توانید از np.all() استفاده کنید
#                         highest_similarity = similarity
#                         closest_match = face
#                 except Exception as e:
#                     logger.error(f"Error comparing face ID {face.id}: {str(e)}")  # چاپ خطای دقیق
#                     continue



#             if closest_match is None or np.any(highest_similarity < 0.10):
#                 print("Best match similarity:", highest_similarity)


#             return JsonResponse({
#                 "id": closest_match.id,
#                 "name": closest_match.first_name,
#                 "surname": closest_match.last_name,
#                 "similarity": round(float(np.max(highest_similarity)), 4)

#             })

#         except (FileUploadError, FeatureExtractionError) as e:
#             logger.error(str(e))

#         except Exception as e:
#             logger.exception("Unknown error occurred.")




from django.http import JsonResponse
from ninja.errors import HttpError
from ninja_extra import api_controller, http_post
from ninja import File
from ninja.files import UploadedFile
import numpy as np
import json
import uuid
import logging
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile

from faceapp.schemas.face_endpoints_schema import FaceRegistrationSchema
from faceapp.models import FaceDetail
from faceapp.services.feature_extractor import extract_features
from faceapp.services.img_handler import handle_file_upload
from faceapp.services.insightface_service import VerificationInsightFaceServices
from faceapp.services.face_picture_service import FacePictureService
from faceapp.exceptions import (
    ImageProcessingError, FeatureExtractionError,
    FileUploadError, DatabaseOperationError
)

logger = logging.getLogger(__name__)

def error_response(message: str, status: int = 400):
    return JsonResponse(
        {"result": {}, "exception": message},
        status=status
    )

@api_controller("/person", tags=["Person"])
class PersonController:

    @http_post("/add", url_name="add_person")
    async def add_person(
        self,
        data: FaceRegistrationSchema,
        image: UploadedFile = File(...),
    ):
        try:
            if not image:
                raise FileUploadError("No image uploaded.")

            # ذخیره فایل در دیسک با FacePictureService
            content = await sync_to_async(image.read)()
            filename = f"{uuid.uuid4()}.jpg"
            file_content = ContentFile(content, name=filename)

            picture_service = FacePictureService()
            local_path = await sync_to_async(picture_service.save_image)(file_content, filename)

            # استخراج ویژگی‌ها
            try:
                vector = await extract_features(local_path)
                if isinstance(vector, list):
                    vector_str = json.dumps(vector)
                else:
                    raise FeatureExtractionError("Unexpected vector type, expected a list.")
            except Exception as e:
                raise FeatureExtractionError(f"Error during feature extraction: {str(e)}")

            # ذخیره در پایگاه داده
            try:
                person = await FaceDetail.objects.acreate(
                    first_name=data.name,
                    last_name=data.lastName,
                    face_vector=vector_str
                )
                await person.asave()
            except Exception as e:
                raise DatabaseOperationError(f"Error creating record in database: {str(e)}")

            return JsonResponse(
                {
                    "result": {
                        "id": person.id,
                        "name": person.first_name,
                        "surname": person.last_name,
                    },
                    "exception": "",
                },
                status=201,
            )

        except FileUploadError as e:
            logger.error(str(e))
            return error_response(str(e), status=400)

        except (ImageProcessingError, FeatureExtractionError) as e:
            logger.error(str(e))
            return error_response(str(e), status=422)

        except DatabaseOperationError as e:
            logger.error(str(e))
            return error_response("A database error occurred.", status=500)

        except Exception as e:
            logger.exception("Unexpected error")
            return error_response("An unexpected error occurred.", status=500)

    @http_post("/identify", url_name="identify_face")
    async def identify_face(self, image: UploadedFile = File(...)):
        try:
            if not image:
                raise FileUploadError("No image uploaded.")

            content = await sync_to_async(image.read)()
            filename = f"{uuid.uuid4()}.jpg"
            file_content = ContentFile(content, name=filename)

            picture_service = FacePictureService()
            selfie_path = await sync_to_async(picture_service.save_image)(file_content, filename)

            insight_service = VerificationInsightFaceServices()
            all_faces = await sync_to_async(list)(FaceDetail.objects.exclude(face_vector=""))

            if not all_faces:
                raise HttpError(404, "No faces registered in the database.")

            # لیستی برای نگه‌داری نتایج
            similarity_results = []
            results = []  # لیست برای ذخیره نتایج
            for face in all_faces:
                try:
                    # ذخیره موقت تصویر کارت شناسایی از دیتابیس
                    id_vector = np.array(json.loads(face.face_vector))

                    # ساخت تصویر مصنوعی برای ID با ویژگی‌ها
                    id_image_path = await sync_to_async(picture_service.save_image)(
                        file_content, f"temp_{uuid.uuid4()}.jpg"
                    )

                    # مقایسه سلفی با عکس از دیتابیس
                    is_match, similarity_score = await sync_to_async(insight_service.compare_faces)(
                        id_image_path, selfie_path, threshold=0.50
                    )

                    # ذخیره نتایج در دیکشنری 
                    if is_match:
                        results.append({
                            "id": face.id,
                            "name": face.first_name,
                            "surname": face.last_name,
                            "similarity": similarity_score  # ذخیره امتیاز شباهت
                        })

                except Exception as e:
                    print(f"Error comparing face ID {face.id}: {e}")

            # اگر نتایج وجود داشته باشد، بیشترین شباهت را پیدا کنیم
            if results:
                best_match = max(results, key=lambda x: x['similarity'])  # بیشترین شباهت
                return JsonResponse(best_match)
            else:
                return JsonResponse({"message": "No match found"})
        except Exception as e:
            logger.exception("Unknown error occurred.")
            return error_response("Unexpected server error.", status=500)

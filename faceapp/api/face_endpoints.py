# views.py
from django.http import JsonResponse
from ninja_extra import  api_controller, http_post
from ninja import File
from ninja.files import UploadedFile
from faceapp.schemas.face_endpoints_schema import FaceRegistrationSchema
from faceapp.models import FaceDetail
from django.core.files.base import ContentFile
import numpy as np
from faceapp.services.feature_extractor import extract_features
import uuid

@api_controller("/person", tags=["Person"])
class PersonController:
    
    @http_post("/add", url_name="add_person")
    async def add_person(
        self,
        data: FaceRegistrationSchema,
        image: UploadedFile = File(...),
    ):
        # ذخیره فایل موقتی برای پردازش
        filename = f"{uuid.uuid4()}.jpg"
        file_content = ContentFile(image.read(), name=filename)

        person = await FaceDetail.objects.acreate(
            first_name=data.name,
            last_name=data.lastName,
        )

        # استخراج ویژگی‌ها (sync ولی می‌تونه خارج از async اجرا شه)
        vector = extract_features(person.image.path)  # path -> local path of uploaded image
        person.face_vector = vector
        await person.asave()

        return JsonResponse({"id": person.id, "name": person.first_name, "surname": person.last_nme},status=201)
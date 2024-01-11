from flask import Blueprint, request, Response
from google.cloud import storage
from util.env import get_env, load_dotenv
from PIL import Image
import uuid
import io
import json

load_dotenv()

upload_user_content = Blueprint(
    "upload-user-content",
    import_name="upload-user-content",
    url_prefix="/upload-user-content",
)

allow_image_types = {
    "image/png": "png",
    "image/jpg": "jpg",
    "image/jpeg": "jpeg",
    "image/webp": "webp",
}


@upload_user_content.post("")
def upload():
    file = request.get_data()
    if request.content_type not in allow_image_types:
        res = Response()
        res.data = json.dumps(
            {
                "msg": "invalid file",
                "content_type": request.content_type,
            }
        )
        res.status_code = 400
        return res
    file_name = str(uuid.uuid4())

    print(
        "::start upload file",
        f"file_name={file_name}",
        f"content_type={request.content_type}",
    )
    img = Image.open(io.BytesIO(file))

    # TODO resize

    client = storage.Client()
    bucket = client.bucket(get_env("GCP_GCS_USER_CONTENT_BUCKET"))
    blob = bucket.blob(file_name)

    img_bytes = image_to_bytes(img)
    blob.upload_from_string(
        img_bytes,
        content_type=request.content_type,
    )

    public_url = blob.public_url
    print(
        "::start upload file",
        f"file_name={file_name}",
        f"content_type={request.content_type}",
    )
    return {
        "msg": "ok",
        "public_url": public_url,
    }


def image_to_bytes(img: Image.Image):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes.getvalue()

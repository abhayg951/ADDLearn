import cloudinary
from ..config import settings
import cloudinary.uploader
import cloudinary.api
          
cloudinary.config( 
  cloud_name = settings.cloud_name, 
  api_key = settings.api_key, 
  api_secret = settings.api_secret 
)

async def upload_thumbnail(file) -> str:
    thumbnail_data = cloudinary.uploader.upload(
        file,
        folder = "image/",
    )

    return thumbnail_data['url']

async def upload_video(file, folder, file_name) -> str:
  video_data = cloudinary.uploader.upload_large(
        file,
        folder = f"courses/video/{folder}",
        resource_type = "video",
        public_id = file_name
    )
  return video_data['url']

async def upload_modules(file, folder, file_name) -> str:

  module_data = cloudinary.uploader.upload(
        file,
        folder = f"courses/modules/{folder}",
        resource_type = "raw",
        public_id = file_name
    )
  return module_data['url']
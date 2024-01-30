import cloudinary
from ..config import settings
import cloudinary.uploader
import cloudinary.api
          
cloudinary.config( 
  cloud_name = settings.cloud_name, 
  api_key = settings.api_key, 
  api_secret = settings.api_secret 
)

def upload_thumbnail(file) -> str:
    thumbnail_data = cloudinary.uploader.upload(
        file,
        folder = "image/",
    )

    return thumbnail_data['url']

def upload_video(file, folder) -> str:
  video_data = cloudinary.uploader.upload_large(
        file,
        folder = f"courses/video/{folder}"
    )
  
  return video_data['url']
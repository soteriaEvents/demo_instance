from dotenv import load_dotenv
load_dotenv() # this line must stay before cloudinary import

import requests
import cloudinary
import cloudinary.uploader

config = cloudinary.config(secure=True)

def fetch_images_from_repo():
	imges_reponse = requests.get("https://api.github.com/repos/soteriaEvents/demo_instance/contents/static/images")
	if imges_reponse.status_code != 200:
		raise requests.exceptions.HTTPError(f"Reponse was not successful, content is =>\n{imges_reponse.content}")

	images_list = []
	images_json = imges_reponse.json()
	for image_info in images_json:
		image_name = image_info.get("name", "no-name")
		image_url = image_info.get("download_url", None)
		images_list.append((image_name, image_url))
	print("\n\nreturned images_list: ", images_list, "\n\n")
	return images_list
images_list = fetch_images_from_repo()


def upload_images(images_list):
	for image_name, image_url in images_list:
		image_name_without_format = '.'.join( image_name.split('.')[0:-1] )
		image_id = "media/" + image_name_without_format
		cloudinary.uploader.upload(image_url, public_id=image_id, unique_filename = False, overwrite=True)
upload_images(images_list)
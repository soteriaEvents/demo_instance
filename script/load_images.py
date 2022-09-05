import os
import sys
import requests

try:
	input_download_path = sys.argv[1]
except IndexError:
	raise IndexError("You need to provide an argument to download the image into")

if not os.path.exists(input_download_path):
	raise ValueError(f"the given path {input_download_path} is not found")

absoulte_download_path = os.path.abspath(input_download_path)

demo_reponse = requests.get("https://api.github.com/repos/soteriaEvents/demo_instance/contents/static/images")
if demo_reponse.status_code != 200:
	raise requests.exceptions.HTTPError(f"Reponse was not successful, content is =>\n{demo_reponse.content}")

demo_content = demo_reponse.json()
for file_info in demo_content:
	file_name = file_info.get("name", "no-name")
	file_url = file_info.get("download_url", None)
	if not file_url:
		print(f"file {file_name} doesn't have download URL")
		continue

	download_response = requests.get(file_url)
	if download_response.status_code != 200:
		print(f"something went wrong when fetching data for {file_name}\nurl: {file_url}\nresponse: {download_response.content}")

	binary_image = download_response.content
	file_absulote_path = absoulte_download_path + '/' + file_name
	with open(file_absulote_path, 'w') as image_file:
		image_file.write(binary_image)
import requests
import base64

# replace 127.0.0.1 with the system ip address if needed
url = "http://127.0.0.1:5544/extract_text"
# add image file path here
imagepath = "<path to the image file>"

with open(imagepath, "rb") as img:
    image_b64 = base64.b64encode(img.read()).decode()

res = requests.post(url=url, data={"image": image_b64})
result_json = res.json()
print(result_json)
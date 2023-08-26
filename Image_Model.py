import os
import requests
import base64
import logging

# File storing function for API call to stability AI to generate the profile image.
# No model is stored, and there is only one function hence the lack of a need for a class.

def produce_image(prompt,sess_id):
    api_host = "https://api.stability.ai"
    url = f'{api_host}/v1/user/account'
    # REMOVED WHEN PUSHED TO GITHUB. IF YOU WANT TO RUN LOCALLY WILL NEED THIS.
    api_key = ''
    engine_id = "stable-diffusion-v1-5"

    # provides the API with the prompt.
    # clip_guidance_preset was changed to a value that images faster, but images that are slightly less "acurate" 
    # set clip_guidace and cfg scale to those that resulted in speed and accuracy balance. These also turned
    # out to be the default values
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": f"{prompt}"
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
        },
    )
    #returnings the status code in english for readability
    data = response.json()
    if response.status_code == 400:
        if data["message"] == 'Invalid prompts detected':
            return "InvalidPrompt"
        else:
            return "OtherError"
    #if no error saves image down as a file
    else:
        image = data["artifacts"][0]["base64"]
        if not os.path.exists(f"./static/{sess_id}"):
            os.makedirs(f"./static/{sess_id}")
        with open(f"./static/{sess_id}/profile_image.png", "wb") as f:
            f.write(base64.b64decode(image))
        return 'Success'


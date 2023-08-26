# Summary:

[Maximomoyer.com](maximomoyer.com) is a live web app wrapped around OpenAI's CLIP model and StabilityAI's stable diffusion model.

The novel functionality of the website is that it takes in a prompt from the user, and produces an image of that prompt in the style of a famous artist whose paintings are closet to the described prompt. For example, if the user inputs "a graffiti gorilla" 

<img width="1437" alt="Screen Shot 2023-08-21 at 8 07 12 PM" src="https://github.com/MaximoMoyer/personal_website/assets/41522480/b0876a2d-c966-4441-bd5e-8518e5c38b3b">

they will be shown an image of "a graffiti gorilla" in the style of Banksy (a famous street artist).

<img width="1440" alt="Screen Shot 2023-08-21 at 8 07 27 PM" src="https://github.com/MaximoMoyer/personal_website/assets/41522480/16649423-963b-4fdb-8f99-95449b12c01e">

# Stack:
Flask
bs4
OpenAI
StabilityAI

# Local hosting:
Go to [StabilityAI](https://platform.stability.ai/docs/api-reference) to get an api key. Fill in the api_key variable in line 13 in [Imagel_model.py](https://github.com/MaximoMoyer/personal_website/blob/main/Image_Model.py#L13). 

Requirements Setup:
In a terminal with venv installed (if venv is not installed can use `pip install venv`.) and python at least at version 3.0 run

```
python -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
```

Running WebApp:
```
python app.py
```

View WebApp:
Copy and paste http://127.0.0.1:5000 (or whatever your local host address is) into a browser.



# File explanations and design decisions:
app.py: Runs the web application.



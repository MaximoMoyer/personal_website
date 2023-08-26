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

# Cool Features/Functionality

  ### Adding Artist
  To add an artist to the database, all you must do is add them to the "artists" dictionary in [scraper.py] (https://github.com/MaximoMoyer/personal_website) and write a function in the style of every other   scraper. This style is that 
  
  1) Function is named "{Artist's key in dictionary}" (i.e. Banksy) + "_Scraper"
  2) Fuction takes in a variable called "url"
  
  ### Scraping only when needed
  The application is built to check if embeddings exist for each artist in the artist dictionary. If they do not exist, the application then checks if there are enough paintings of the artist to create        a representative average embedding. If there are not enough emebeddings, only then are the websites scrapped to gather the photos of the artists. I've uploaded the embeddings of the artists for              convenience, but i

  

# Local hosting:
Go to [StabilityAI](https://platform.stability.ai/docs/api-reference) to get an api key. Fill in the api_key variable in line 13 in [Imagel_model.py](https://github.com/MaximoMoyer/personal_website/blob/main/Image_Model.py#L13). 

Requirements Setup:

In a terminal with venv installed (if venv is not installed can use `pip install venv`) and python at least at version 3.0 run

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



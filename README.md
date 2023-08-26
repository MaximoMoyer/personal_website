# Summary:

[Maximomoyer.com](maximomoyer.com) is a live web app wrapped around OpenAI's CLIP model and StabilityAI's stable diffusion model.

The novel functionality of the website is that it takes in a prompt from the user, and produces an image of that prompt in the style of a famous artist whose paintings are closet to the described prompt. For example, if the user inputs "a graffiti gorilla" 

<img width="1437" alt="Screen Shot 2023-08-21 at 8 07 12 PM" src="https://github.com/MaximoMoyer/personal_website/assets/41522480/b0876a2d-c966-4441-bd5e-8518e5c38b3b">

they will be shown an image of "a graffiti gorilla" in the style of Banksy (a famous street artist).

<img width="1440" alt="Screen Shot 2023-08-21 at 8 07 27 PM" src="https://github.com/MaximoMoyer/personal_website/assets/41522480/16649423-963b-4fdb-8f99-95449b12c01e">

# Stack:
- Flask (web app)
- bs4 (scraping)
- OpenAI (embeddings)
- StabilityAI (image creation)
- Webflow (V1 Bone structure of site and animation on loading page)

# Cool Features/Functionality

  ### Adding Artists
To add an artist to the database, all you must do is add them to the "artists" dictionary in [scraper.py] (https://github.com/MaximoMoyer/personal_website/blob/main/Scraper.py#L11) and write a function in the style of every other scraper. This style is that 
  
1) Function is named "{Artist's key in dictionary}" (i.e. Banksy) + "_Scraper"
2) Fuction takes in a variable called "url"
  
  ### Scraping only when needed
The application is built to check if embeddings exist for each artist in the artist dictionary. If they do not exist, the application then checks if there are enough paintings of the artist to create a representative average embedding. If there are not enough emebeddings, only then are the websites scrapped to gather the photos of the artists. I've uploaded the embeddings of the artists for convenience, but you can delete the whole artist folder, the whole embedding folder, or indivudal embeddings to see this work.

  ### Efficient storage
  This application was built to be super efficient in storage. Everytime someone generates a new profile their previous profile image is removed. Whenever someone leaves a site, their profile image is removed. This might sound basic but was tricky! Things would get hairy when dealing with edge cases such as implementing the "loading is taking too long" button, handling users using the browser arrows to go forward or backward in pages, and users iterating rapidly through various pages.

  ### Handles bad prompts
  If you pass in a bad prompt, or try and skip to navigate to a page without giving the image time to load, or ever providing a prompt in the first place, you will receieve a Toucan, and it will be explained to you why you receieved a toucan.
  

  

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



# File Explanations and design decisions:

  ### app.py:
  Runs the web application. Built to be statelss and used the session "uid" and "skip_uid" to handle this
  
  ### Profile_Generation.py: 
  Class that acts as a wrapper around all profile generation tasks:
     - Generates artist embeddings
     - Gets the artist most similair to the prompt
     - Gets the image to be shown to the user
  
  ### Joint_Model.py: 
  Class that embeds both the photos from the artists and the prompt using the OpenAI CLIP model. Created as a class because it loads in a       model, so is somone choses to "create a new profile" you mustn't load the clip model in twice.
  
  ### Image_Model.py: 
  File with a function to call the Stability AI diffucion model. Created as a file because it has a single function with not need to store a     model or any information in class variables. 

  ### HTML, CSS, and JS files: 
  All these files are named intuitively. Used webflow to handle initial bone structure of the website and create the entire animation on the loading page. The files that were exact copies from webflow code have webflow in their name. All other files have intuitive design decisions made that priotized easy styling, effective navigation between pages, handling edgecase user behavior, and readbility (most notably in the html).


  

  

  
  

  

  





# Summary:

[Maximomoyer.com](Maximomoyer.com) is a live hosted web app wrapped around OpenAI's CLIP model and StabilityAI's stable diffusion model.

Please note, there are some bugs being fixed on the version accessible over the internet. Locally, there are no known bugs.

The novel functionality of the website is around "prompt engineering". It takes in a prompt from the user, finds the artist who has created paintings most similiar to that prompt. It then edits the prompt to produce an image of the passed in prompt in the style of the matched artist. For example, if the user inputs "a graffiti gorilla" 

<img width="1437" alt="Screen Shot 2023-08-21 at 8 07 12 PM" src="https://github.com/MaximoMoyer/personal_website/assets/41522480/b0876a2d-c966-4441-bd5e-8518e5c38b3b">

they will be shown an image of "a graffiti gorilla" in the style of Banksy (a famous street artist).

<img width="1440" alt="Screen Shot 2023-08-21 at 8 07 27 PM" src="https://github.com/MaximoMoyer/personal_website/assets/41522480/16649423-963b-4fdb-8f99-95449b12c01e">

Please note that Banksy is most frequently returned as the artists, likely due to the more modern character of his art. However, if you use prompts specific to other artists like a "a royal women in a red dress" for Lebrun, "A swirling landscape" for Picasso you will have other styles of paintings appear.

# Stack:
- Flask (web app)
- bs4 (scraping)
- OpenAI (embeddings)
- StabilityAI (image creation)
- Webflow (V1 Bone structure of site and animation on loading page)
- Python anywhere (hosting service)

# Cool Features/Functionality

  ### Adding Artists
To add an artist to the database, all you must do is add them to the "artists" dictionary in [scraper.py](https://github.com/MaximoMoyer/personal_website/blob/main/Scraper.py#L11) and write a function in the style of every other scraper. This style is that 
  
1) Function is named "{Artist's key in dictionary}" (i.e. Banksy) + "_Scraper"
2) Fuction takes in a variable called "url"
  
  ### Scraping only when needed
The application is built to check if embeddings exist for each artist in the artist dictionary. If they do not exist, the application then checks if there are enough paintings of the artist to create a representative average embedding. If there are not enough emebeddings, only then are the websites scrapped to gather the photos of the artists. I've uploaded the embeddings of the artists for convenience, but you can delete the whole artist folder, the whole embedding folder, or indivudal embeddings to see this work.

  ### No wasted storage
  This application was built to waste no storage space (to keep my hosting bill low). Everytime someone generates a new profile their previous profile image is removed. Whenever someone leaves a site, their profile image is removed. This might sound basic but it was slightly tricky! Things would get hairy when dealing with edge cases such as implementing the "loading is taking too long" button, handling users using the browser arrows to go forward or backward in pages, and users iterating rapidly through various pages.

  ### Handles innapropriate prompts and skipping the image generation step
  Innapropriate prompts were simple to handle becaue Stability's API checks for them and returns a corresponding error code. Handling skipping the loading of an image, navigating directly to a page (without entering a prompt), or using the back/forward arrows on the browser were more challenging to handle. But in any of these cases, instead of a customized image, you will receieve a Toucan, and it will be explained to you why you receieved a toucan.

  ### Redirect
  This was for the actual website. This redirect points maximomoyer.com to the maximomoyer.pythonanywhere.com which then points to the actual content (using this python anywhere URL saved me a monthly subscription charge :) ) 
  
# Models

## OpenAI CLIP model

This model embeds images and text into the same space. Though there were research papers discussing the idea, it was suprisinlgy hard for me to find off the shelf models that did this (maybe I was not searching well :) ).  But, I was able to find a [paper](https://arxiv.org/pdf/2103.00020.pdf) from OPEN AI that used jointly trained image and text embedding models to build an optimal _image_ classifcaiton model. This is a fairly novel approach becuase

Typically image recnogition models: 
- Train some sort of a feature extractor (CNN is a common example)
- Then uses a linear classifer to predict a label

But the CLIP model instead:
- Pre-Trains Text and image encoders jointly by setting the loss function to quantify how well these two encoders created embeddings that were simialir between  imag/prompt pairs.
- At serving time, given a possible set of labels, the text encoder is fed some default wording such as "a photo of" (could be blank) and the image encoder is feed the image to be classified. Then the label that produces the highest probability of a "match" between the image and encoder model is selected as the label.

_In this project I took the pre-trained embedding models and used those_. By embedding text and images, computing how close these embeddings are, and finding a match between an artist and text, I essentially performed the forward pass of the pretraining step (minus loss calculation).

When experimenting with various prompts, and studying the types of paintings that the various artists in the database would paint, qualitatively the model seemed to perform very well in matching artists and prompts. (See gorilla example at top of Read Me).


## Stability's Diffusion model

It is easy to find an off the shelf model that can take texts and produce an image from it. I chose to go with the Stability diffusion model vs. off the shelf models (hugging face) because through qualitative testing it seemed to produce images that were more accurate. And when compared to other paid options (namely open ai's dalle) this api was more configurable and it was slighlty more reasoanbley priced. Stability's model had fields such as:

- CFG scale: Stands for "classifier free guidance". Lets you toggle between "quality of image" vs. "image matching". This is a tricky idea, so I'll use an analogy. A "clown gorilla" that had maximum quality of image might just be a stunning clear photo of a monkey. A "clown gorilla" that had maximum "image matching" might have a very blurry gorilla with a red nose and big shoes that looks like it was drawn by someone who has a shakey hand.
  
- Steps: Toggles the quality of the image vs. the number of diffusion steps.

    My understanding [(one resource I found really helpful)](http://jalammar.github.io/illustrated-stable-diffusion/) is there are three core components of the      stable diffusion network
    1) Text embedding network
    2) A pretrained network ("U-Net") that is trained to predict how much noise is in latent information of an image given a corresponding prompt embedding
    3) A autoencoder/decoder that produces images.
    
    Stable diffusion pases the embedding prompt, alongside totally random latent "image" information (if this image were decoded it would just be fuzz). The "U-     Net" mechanism then predicts how much noise is in this latent representation, subtracts it from the latent space, and repeats this process **Steps** number      of times. After all steps, the diffused latent image information is passed through the encoder/decoder
    
    The higher the steps the longer the process takes and the more accurate the image gets. 

- Clip_guidance_preset: It was tough to find a detailed explanation on this one. But it seems this uses the CLIP model discussed above to guide the model as it goes through the difussion steps. It likely does so by comparing the latent image to the prompt at various steps (using the CLIP model) and somehow altering the image to be a closer match to the prompt. In practice this variable seemed to have a similair affect to steps in that different inputs traded off quality for production speed.

I am sad to admit, that after a good amount of experimentation, the defaults suggested for these three variables produced what seemed to be the best tradeoff between speed of production, quality of image, and accuracy of image.
  

# Local hosting:
Go to [StabilityAI](https://platform.stability.ai/docs/api-reference) to get an api key. Fill in the api_key variable in line 13 in [Imagel_model.py](https://github.com/MaximoMoyer/personal_website/blob/main/Image_Model.py#L13). 

#### Requirements Setup:

In a terminal with venv installed (if venv is not installed can use `pip install venv`) and python at least at version 3.0 run

```
python -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
```

#### Running WebApp:

```
python app.py
```

#### View WebApp:

Copy and paste http://127.0.0.1:5000 (or whatever your local host address is) into a browser.



# File Explanations and Design Decisions:

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
  All these files are named intuitively. Used webflow to handle initial bone structure of the website and create the entire animation on the loading page. The files that were exact copies from webflow code have webflow in their name. All other files have intuitive design decisions made that priotized easy styling, effective navigation between pages, handling edgecase user behavior, and readbility.

  
# Next Steps:
- Experiment with [Facebook's new joint embedding model](https://github.com/facebookresearch/ImageBind)
- Set up AWS hosting
- Set up Docker hosting
- Experiment with style transfer networks rather than prompt engineering (produce image using passed in prompt, then overlay style of an artist using separate     network)
- Experiment with displaying multiple images produced in different ways and allowing the user to select their favorite
  

  

  





#https://github.com/openai/CLIP
import torch
import clip
from PIL import Image
import os

# Class that is used to embed both the artists' paintings and the profile description.
# Note this was made a class so that the model only had to be loaded once.

class Joint_Model:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    #for each artist passed in, embeds all paintings associated with the artist, and saves the average
    # of all these embeddings 
    def embedd_images(self,artists):
        for artist in artists:
            image_count = 0
            while os.path.exists('Artists/' + artist + '/image_' + str(image_count)):
                image = self.preprocess(Image.open('Artists/' + artist + '/image_' + str(image_count))).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    if image_count == 0:
                        image_features = self.model.encode_image(image)
                    else:
                        image_features += self.model.encode_image(image)
                image_count +=1
            image_features = image_features / image_count
            torch.save(image_features, 'Artists/Embeddings/' + artist + '.pt')

    # function that calculates a similairity score for each artist's embedding in relation to the passed 
    # in profile description's embedding. Returns the artist with the most similair embeddings.
    def get_most_similair(self,prof_desc, artists):
        text = clip.tokenize([prof_desc]).to(self.device)
        cos = torch.nn.CosineSimilarity()
        max_cos = 0
        most_similair_artist = None
        with torch.no_grad():
            text_features = self.model.encode_text(text)
            logit_list = None
            for artist in artists:
                image_features = torch.load('Artists/Embeddings/' + artist + '.pt')
                sim = cos(image_features, text_features)
                if sim > max_cos:
                    max_cos = sim
                    most_similair_artist = artist
        return most_similair_artist
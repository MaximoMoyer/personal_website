import Scraper as scraper
import Joint_Model as joint_model
import os
import shutil
import Image_Model as Image_Model

# Profile Generator class that handles the high level logic around generating a profile photo.
# Uses  "scraper"  that, if an artist's average embedding is not saved and paintings are missing, is used to generate scrapped paintings for that artist.
# Uses "joint_model" that generates each artist's average embedding and the embedding of prompts in the same space.
# Can find the distance between each artist's average embedding and the prompt's embedding and return the closest match.

class Profile_Generator():
    def __init__(self):
        self.scraper = scraper.Scraper()
        self.artists = self.scraper.return_artists()
        self.joint_model = joint_model.Joint_Model()
        self.generate_embeddings()
        

    # Function that ensures each artist's embeddings are created and saved to the appropriate folder.
    # If embeddings have been created for a given artists, nothing is done. If embeddings have not been created for a given artist
    # the function first ensures that there are enough images of the artist's paintings scraped to accurately
    # represent the style of the artist (at lesat 10). If there are insufficient paintings, the scraper is run for that artist.
    # Once there are sufficient paintings, these photos are all embedded and their average embedding is saved down
    # by using the joint model.
    def generate_embeddings(self):

        if not os.path.exists('Artists/'):
            os.makedirs('Artists/')
        if not os.path.exists('Artists/Embeddings'):
            os.makedirs('Artists/Embeddings')
            
        embeddings = os.listdir('Artists/Embeddings')
        for artist in list(self.artists):
            if artist + '.pt' not in embeddings:
                if artist not in os.listdir('Artists/') or len(os.listdir('Artists/' + artist)) < 10:
                    file_path = os.path.join(os.getcwd(), 'Artists', artist)
                    if os.path.exists(file_path):
                        shutil.rmtree(file_path)
                    os.makedirs(file_path)
                    func_name = 'self.scraper.' + artist + '_Scraper'
                    eval(func_name + "(" + 'self.scraper.artists[artist]' + ")")
                self.joint_model.embedd_images([artist])
    
    #function to get the artist that is most similair to the passed in profile description from the user
    def get_similair_artist(self, prof_desc):
        #check to see the artist that the profile description is most similar to
        most_similair = self.joint_model.get_most_similair(prof_desc, self.artists)
        return most_similair
    

    # function that passes a prompt to the CLIP API instructing it to create a photo
    # of the profile description the user passed in, but "in the sytle of" the artist with the
    # average embedding that was nearest the given profile description
    def get_image(self,prof_desc,most_similair,sess_id):
        prompt = prof_desc + 'in the style of ' + most_similair
        #Stability Image model that generates images
        image_outcome = Image_Model.produce_image(prompt,sess_id)
        return image_outcome
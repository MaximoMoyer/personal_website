from bs4 import BeautifulSoup
import requests
import os
import shutil

# function that scrapes the internet for photos from each artist. The average (median) # of photos scraped for each artist
# is 67
class Scraper:
    def __init__(self):
        # to add an artist, add to dictionary below and create a function with the name of the artist + _Scraper
        self.artists = {
                'Banksy':'https://twistedsifter.com/2014/07/the-ultimate-banksy-gallery/',
                'Leonardo': 'https://www.atxfinearts.com/blogs/news/leonardo-da-vinci-most-famous-paintings',
                'Monet': 'https://dreamsinparis.com/famous-paintings-by-claude-monet/',
                'Dali': 'https://arthive.com/publications/4746~15_most_famous_surreal_paintings_by_salvador_dali',
                'Munch':'https://www.theartstory.org/artist/munch-edvard/',
                'VanGogh':'https://www.tallengestore.com/collections/vincent-van-gogh',
                'Vermeer':' http://www.essentialvermeer.com/vermeer_painting_part_one.html',
                'Kahlo':'https://www.fridakahlo.org/frida-kahlo-paintings.jsp',
                'Rembrandt':'https://www.theartstory.org/artist/rembrandt-van-rijn/',
                'Picasso':'https://www.pablopicasso.org/picasso-paintings.jsp',
                'Warhol':'https://magazine.artland.com/andy-warhol-portraits-a-definitive-guide/',
                'LeBrun':'https://www.theartstory.org/artist/vigee-le-brun-elisabeth-louise/'
                }

    def return_artists(self):
        return self.artists.keys()

    def scrape_all(self):
        for artist in self.artists.keys():
            func_name = 'self.' + artist + '_Scraper'
            file_path = os.path.join(os.getcwd(), 'Artists', artist)
            if os.path.exists(file_path):
                shutil.rmtree(file_path)
            os.makedirs(file_path)
            eval(func_name + "(" + 'str(self.artists[artist])' + ")")

    def Banksy_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url.startswith('http') and '.jpg' in img_url:
                write_count +=1
                filename = 'Artists/Banksy/image_' + str(int(write_count))
                if write_count < 127:
                    with open(filename, 'wb') as f:
                        f.write(requests.get(img_url).content)

    def Leonardo_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url.startswith('//cdn'):
                write_count += 1
                filename = 'Artists/Leonardo/image_' + str(write_count)
                img_url = 'https:' + img_url[0:-5]
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def Monet_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.find('main')
        img_tags  = main.find_all("img")
        write_count = -1
        count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url.startswith('https'):
                count +=1
                if count == 0 or count >13:
                    continue
                write_count +=1
                filename = 'Artists/Monet/image_' + str(write_count)
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def Dali_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        write_count = -1
        for img in img_tags:
            img_url = img.get('data-src')
            if img_url is not None and img_url.startswith('http') and ('article' in img_url or 'work' in img_url):
                write_count += 1
                filename = 'Artists/Dali/image_' + str(write_count)
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def Munch_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        count = -1
        for img in img_tags:
            img_url = img.get('data-src')
            if img_url is not None and img_url.startswith('/images20') and 'munch' in img_url:
                count += 1
                if count == 0 or count > 11:
                    continue
                write_count +=1
                filename = 'Artists/Munch/image_' + str(write_count)
                img_url = 'https://www.theartstory.org' + img_url
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def VanGogh_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url is not None and 'products' in img_url and img_url.startswith('//www'):
                write_count += 1
                filename = 'Artists/VanGogh/image_' + str(write_count)
                img_url = 'https:' + img_url
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def Vermeer_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url is not None and  img_url.startswith('directoryimages'):
                write_count += 1
                filename = 'Artists/Vermeer/image_' + str(write_count)
                img_url = 'http://www.essentialvermeer.com/' + img_url
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def Kahlo_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url is not None and  'images' in img_url:
                write_count += 1
                filename = 'Artists/Kahlo/image_' + str(write_count)
                img_url = 'https://www.fridakahlo.org/' + img_url
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def Rembrandt_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        for img in img_tags:
            img_url = img.get('data-src')
            if img_url is not None and img_url.startswith('/images20') and 'rembrandt' in img_url and 'works' in img_url:
                write_count +=1
                filename = 'Artists/Rembrandt/image_' + str(write_count)
                img_url = 'https://www.theartstory.org' + img_url
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)


    def Picasso_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url is not None:
                write_count +=1
                filename = 'Artists/Picasso/image_' + str(write_count)
                img_url = 'https://www.pablopicasso.org/' + img_url
                if write_count == 100:
                    break
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)


    def Warhol_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        for img in img_tags:
            img_url = img.get('src')
            if img_url is not None and img_url.startswith('https:') and '2020/09' in img_url and not('1e55ee7e37280268b072_Q8Hgs'  in img_url):
                write_count +=1
                filename = 'Artists/Warhol/image_' + str(write_count)
                if write_count == 100:
                    break
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)

    def LeBrun_Scraper(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags  = soup.find_all("img")
        write_count = -1
        count = -1
        for img in img_tags:
            img_url = img.get('data-src')
            if img_url is not None and img_url.startswith('/images20') and 'le_brun' in img_url:
                count +=1
                if count ==0 or count ==13:
                    continue
                write_count +=1
                filename = 'Artists/LeBrun/image_' + str(write_count)
                img_url = 'https://www.theartstory.org' + img_url
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)



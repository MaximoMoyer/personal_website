from flask import Flask, redirect, url_for, request, session, render_template
import Profile_Generation as PG
from Profile_Generation import Profile_Generator
import uuid
import os
import shutil

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# dipslays the homepage and assigns values to all session level variables
#'skip_uid' is created so that if a user skips over the loading of a prompt (fowrard skip or backwards to previous pages), they are always shown
# the default image even after their prompted image is eventually produced and save down
@app.route('/')
def index():
	if 'uid' not in session:
		session['uid'] = str(uuid.uuid4())
		session['skip_uid'] = 'Off'
	#setting defaults for variables to avoid any errors if pages are directly navigated to 
	session['image_status'] = 'default'
	session['similair_artist'] = 'default'
	session['prof_desc'] = 'default'
	return render_template('index.html')


# Loading page with animation once user submits prompt. Stores the prompt the user passes in as as session level variable
@app.route('/loading', methods=['POST','GET'])
def loading():
	if request.method == 'POST':
		session['prof_desc'] = request.form['nm']
		return render_template('loading.html')

#This page is called from the loading html file. Once create_profile is completed user is redirected to "home".
#Function creates a Profile_Generator class, find the artist with paintings closest to the prompt
#and generatest the described image, in the sytle of the closest artist, for the user.
@app.route('/create_profile')
def create_profile():
	#set here to avoid error when skipping image generation
	# resets the skip uid and id tags. removes old photo
	if session['skip_uid'] != 'Off':
		session['uid'] = session['skip_uid']
		session['skip_uid'] = 'Off'
	if os.path.exists(f'./static/{str(session["uid"])}'):
		shutil.rmtree(f'./static/{str(session["uid"])}')
	
	prof_desc = session['prof_desc']
	if not isinstance('profile_generator',Profile_Generator):
		profile_generator = PG.Profile_Generator()
	
	similair_artist = profile_generator.get_similair_artist(prof_desc)
	session['similair_artist'] = similair_artist
	
	#generates and saves down image for user. returns image status
	image_status = profile_generator.get_image(prof_desc, similair_artist, str(session['uid']))
	session['image_status'] = image_status
	return 'image creation done'

#home page of webiste
@app.route('/home')
def home():

	image_status = session['image_status']
	prof_desc = session['prof_desc']
	similair_artist = session['similair_artist']

	# path will not exist in cases where the user arrived at the homepage by skipping over the loading
	# of the image, or hitting back button in the browser twice while an image is being created ('/') 
	# Will also not exist if an inapropriate prompt was passed in.
	if os.path.exists(f'./static/{str(session["uid"])}/profile_image.png'):		
		return render_template('home.html', sentence = prof_desc, similair_artist = similair_artist, image_status = image_status, sess_id = str(session['uid']))
	else:
		# if Skip_uid is not storing the actual uid, then make it store the uid while uid is set to none so the checked file path does not exist
		if session['skip_uid'] == 'Off':
			session['skip_uid'] = session['uid']
			session['uid'] = None
		return render_template('home.html', sentence = prof_desc, similair_artist = similair_artist, image_status = image_status, sess_id = 'default')


# displays the about page. 
@app.route('/about')
def about_me():
	#see home function for explanation of checking this path
	if os.path.exists(f'./static/{str(session["uid"])}/profile_image.png'):
		return render_template('about.html', sess_id = str(session['uid']))
	else:
		return render_template('about.html', sess_id = 'default')


# displays the reading page.
@app.route('/reading')
def reading():
	#see home function for details of checking this path
	if os.path.exists(f'./static/{str(session["uid"])}/profile_image.png'):
		return render_template('reading.html', sess_id = str(session['uid']))
	else:
		return render_template('reading.html', sess_id = 'default')


# displays the chorebot page.

@app.route('/chorebot')
def chore_bot():
	#see home function for details of checking this path
	if os.path.exists(f'./static/{str(session["uid"])}/profile_image.png'):
		return render_template('chorebot.html', sess_id = str(session['uid']))
	else:
		return render_template('chorebot.html', sess_id = 'default')


#function called when the user exits the browser. Deletes the user's saved down image to save hosting $!
@app.route('/delete')
def delete():
	if session['skip_uid'] !=  'Off':
		session['uid'] = session['skip_uid']
		session['skip_uid'] = 'Off'
	if os.path.exists(f'./static/{str(session["uid"])}'):
		shutil.rmtree(f'./static/{str(session["uid"])}')
	return 'exited'


if __name__ == '__main__':
	app.secret_key = 'mysecretkey'
	app.run(debug=False)
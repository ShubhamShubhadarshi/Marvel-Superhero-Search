from marvel import Marvel
from flask import Flask, render_template, request


public_key = "fa4ab124665e62db3b9fdee7b401fef6"
private_key = "732f86a143c7807784668085fe6d1aeada9077b9"

m = Marvel(public_key,private_key)

characters = m.characters

def get_info(characters,name):
	character = characters.all(nameStartsWith=name)
	ch_ids = [char['id'] for char in character['data']['results']]
	ch_names = [char['name'] for char in character['data']['results']]
	descriptions = [char['description'].replace('<p class="Body">','') for char in character['data']['results']]
	images = [char['thumbnail']['path']+"/portrait_xlarge."+char['thumbnail']['extension'] for char in character['data']['results']]
	chars = []
	for i in range(len(ch_ids)):
		char = { 'id' : ch_ids[i],
		         'name': ch_names[i],
		         'description' : descriptions[i],
		         'image' : images[i] }
		chars.append(char)
	return chars


def get_comics_info(ch_id):	
	comics = characters.comics(ch_id)
	comic_names = [comic['title'] for comic in comics['data']['results']]
	comic_descriptions = [comic['description'] for comic in comics['data']['results']]
	comic_images = [comic['thumbnail']['path']+"/portrait_xlarge."+comic['thumbnail']['extension'] for comic in comics['data']['results']]
	comic_url = [comic['resourceURI'] for comic in comics['data']['results']]
	ch_comics = []
	for i in range(len(comic_names)):
		ch_comic = { 'name': comic_names[i],
		         'description' : comic_descriptions[i],
		         'image' : comic_images[i],
		         'url' : comic_url[i]}
		ch_comics.append(ch_comic)
	return ch_comics





app = Flask(__name__)

@app.route('/',methods=['POST','get'])
def index():
	chars = []
	if request.method == 'POST':
		try:
			name = request.form['search']
			chars = get_info(characters,name)
		except:
			res = request.form
			name = res['nm']
			iid = res['iid']
			image = res['imge']
			desc = res['inf']
			char = {'name': name, 'id': iid, 'description': desc, 'image': image}
			comics = get_comics_info(int(iid))
			return render_template('about.html', chars=comics)
	return render_template('index.html',chars=chars)


if __name__ == '__main__':
	app.run(debug = True)
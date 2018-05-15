import models
import flask
from sys import path as sys_path

sys_path.append('/usr/lib/python2.7/site-packages/flask')

# Initialising flask application
app = flask.Flask(__name__, template_folder = 'views')

@app.route("/")
def index():
  """ Renders main page """
  return flask.render_template("main_page.html")

@app.route("/shorten/")
def shorten():
  """ Returns short url of requested full url """

  # Validating the user input 
  full_url = flask.request.args.get('url')
  if not full_url:
    raise BadRequest()
  
  # Model returning object with short_url property
  url_model = models.Url.shorten(full_url)
  url_model.short_url

  # Passing the data to view and calling its render method
  short_url = flask.request.host + '/' + url_model.short_url
  return flask.render_template('success.html', short_url = short_url)

@app.route('/<path:path>')
def redirect_to_full(path = ''):
  """ gets the short url and redirects the user to the corresponding full url if found. """

  #Model returns object with full_url property
  url_model = models.Url.get_by_short_url(path)
  
  #Validate mode return
  if not url_model:
    raise NotFound()

  return redirect(url_model.full_url)

if __name__ == "__main__":
  app.run(debug=True)


  

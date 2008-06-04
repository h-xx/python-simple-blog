from datetime import datetime
import textile
import cherrypy
import re, os

# update config file to current working directory
regex = re.compile('current_directory')

f = open('post.config.base', 'r')
contents = f.read()
contents = regex.sub(os.getcwd(), contents)
f.close()

f = open('post.config', 'w')
f.write(contents)
f.close() 

class Post(object):
  def __init__(self, date = datetime.today().strftime('%Y%m%d%H%M%S'), title = "", body = ""):
    self.date = date
    self.title = title
    self.body = body
    self.markedupbody = textile.textile(self.body)

  def markupbody(self):
    self.markedupbody = textile.textile(self.body)

  def createPost(self, createDiv = True):
    div = []
    if (createDiv): div.append('''<div class="post" id="%s">''' % self.date )
    div.append('''<h2 class="thesubject">''' + self.title + '''</h2>''')
    div.append('''<h3 class="time">''' + self.date + '''</h3>''')
    div.append('''<div class="thebody">\n''' + self.markedupbody +'''\n</div>''')
    if (createDiv): div.append('''\n</div>''')
    div = '\n'.join(div)
    return div

  def createEditor(self, width, height):
    return '''
<input type="text" name="input_title" id="input_title" value="%s">
<br />
<textarea id="input_body" style = "width: %spx; height: %spx;">%s</textarea>
<br />
<form action="edit" method="post" name="postForm" id="postForm">
<input type="hidden" name="post_title" id="post_title">
<input type="hidden" name="post_body" id="post_body">
<input type="hidden" name="post_date" id="post_date" value="%s">
<input type="button" value="Submit Post" onclick="fill_form_and_escape(%s)">
<input type="button" value = "Cancel" onclick = "cancelEditing()">
</form>
''' % (self.title, width, height, self.body, self.date, self.date)

  def editPost(self, title, body):
    postfile = open('posts/' + self.date, 'w')
    postfile.write('\n'.join([title, body]))
    postfile.close()
    self.body = body
    self.title = title
    self.markupbody()

class Comment(Post):
  def __init__(self, date = datetime.today(), title = "", body = "",
commenterName = "Anonymous"):
    super(Comment, self).__init__(date, title, body)
    self.commenterName = commenterName

class Blog(object):
  def __init__(self, author = "Anonymous", url = "http://127.0.0.1"):
    self.posts = []
    self.author = author
    self.url = url
    self.getPosts()

  def getPosts(self):
    self.posts = []
    expression = re.compile('\d*')
    for file in os.listdir(os.getcwd() + '/posts/'):
      if expression.match(file) != None:
        currentPost = Post()
        filehandle = open('posts/' + file, 'r')
        currentPost = Post(file, (filehandle.readline())[0:-1], filehandle.read())
        filehandle.close()
        currentPost.markupbody()
        self.posts.append(currentPost)

  def index(self):
    page = []
    header = open('theme/header.php', 'r')
    page.append(header.read())
    header.close()
    
    for post in self.posts:
      page.append(post.createPost())
    
    footer = open('theme/footer.php', 'r')
    page.append(footer.read())
    footer.close()
    page = '\n\n'.join(page)
    return page
  index.exposed = True

  def ajaxedit(self, id, width, height):
    for post in self.posts:
      if post.date == id:
        return post.createEditor(width, height)
  ajaxedit.exposed = True

  def edit(self, post_title, post_body, post_date):
    for post in self.posts:
      if post.date == post_date:
        post.editPost(post_title, post_body)
        return 'Updated.'
  edit.exposed = True

  def ajaxget(self, id):
    for post in self.posts:
      if post.date == id:
        return post.createPost(False)
  ajaxget.exposed = True

      

cherrypy.tree.mount(Blog(), config='post.config')

if __name__ == '__main__':
  import os.path
  cherrypy.config.update(os.path.join(os.path.dirname(__file__), 'tutorial.conf'))
  
  cherrypy.server.quickstart()
  cherrypy.engine.start()


"""
[/]
tools.staticdir.root = os.path.normcase('C:/Documents and Settings/pnbersch/Desktop/play/ponies/')
[/js/jquery-1.2.1.js]
tools.staticfile.on = True
tools.staticfile.filename = os.path.normcase("C:/Documents and Settings/pnbersch/Desktop/play/ponies/js/jquery-1.2.1.js")

[/js/functions.js]
tools.staticfile.on = True
tools.staticfile.filename = os.path.normcase("C:/Documents and Settings/pnbersch/Desktop/play/ponies/js/functions.js")

[/theme/main.css]
tools.staticfile.on = True
tools.staticfile.filename = os.path.normcase("C:\Documents and Settings\pnbersch\Desktop\play\ponies/theme/main.css")




"""


# myblog = Blog()

# print myblog.makePage()

#for post in myblog.posts:
#  print post.title
#  print post.date
#  print post.markedupbody


#print myblog.posts[0].title
#print myblog.posts[0].date
#print myblog.posts[0].body

# datetime.today().strftime('%Y%m%d%H%M%S')

#thepost = Post()

#thepost.title = 'Fear!'
#thepost.body = 'I find that you should fear all _ponies_.'

#thepost.markupbody()

#print thepost.title

#print thepost.date.strftime('%Y%m%d%H%M%S')

#print thepost.body

#print thepost.markedupbody



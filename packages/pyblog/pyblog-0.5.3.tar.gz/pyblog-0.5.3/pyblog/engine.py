from . import utils
from datetime import datetime
from os import path
import jinja2

DEFAULT_CONFIG = """name: A PyBlog Blog
tagline: Demoing PyBlog, a lightweight python static blog generator
root_url: https://blog.com
"""

class Page:
    title           = u''
    content         = u''
    template        = None
    slug            = u''
    url             = u''
    date            = None
    
    def __init__(self, file_path):
        """Creates a generic page from a file"""
        parts = utils.file_get(file_path).split('\n\n', 1)
        if len(parts) == 2:
            meta = utils.parse_headers(parts[0])
            self.content = parts[1]
            self.insert_fields(meta)
            if self.date:
                self.date = datetime.strptime(meta['date'], '%Y-%m-%d %H:%M:%S')
            else:
                self.date = utils.file_mtime(file_path)
        else:
            self.content = parts[0]
            self.date = utils.file_mtime(file_path)
            
    def insert_fields(self, data={}):
        """Inserts values from a dictionary as fields"""
        for key in data:
            setattr(self, key, data[key])
        
    
    @staticmethod
    def make_post(blog, file):
        """Creates a post object"""
        post = Page(path.join(blog.posts_dir, file))
        post.slug = utils.slugify(post.title)
        post.url = post.date.strftime('%Y/')+post.slug+'.html'
        return post
    
    @staticmethod
    def make_page(blog, file):
        """Creates a page object"""
        page = Page(path.join(blog.pages_dir, file))
        page.slug = file
        page.url = file
        tpl = blog.env.from_string(page.content)
        page.content = tpl.render(blog=blog)
        return page
    
    def __repr__(self):
        return 'Blog.Page(%s)' % self.slug

class Blog:
    name            = u''
    root_url        = u''
    tagline         = u''
    in_dir          = u''
    config_file     = u''
    pages_dir       = u''
    posts_dir       = u''
    templates_dir   = u''
    static_dir      = u''
    out_dir         = u''
    env             = None
    
    def __init__(self, in_dir, out_dir, config_file=None):
        """Creates the blog object from the config file"""
        if config_file:
            self.config_file= path.abspath(config_file)
        else:
            self.config_file= path.abspath(path.join(in_dir, 'config.txt'))
        self.templates_dir  = path.abspath(path.join(in_dir, '_templates'))
        self.static_dir     = path.abspath(path.join(in_dir, '_static'))
        self.pages_dir      = path.abspath(path.join(in_dir, '_pages'))
        self.posts_dir      = path.abspath(path.join(in_dir, '_posts'))
        self.in_dir         = path.abspath(in_dir)
        self.out_dir        = path.abspath(out_dir)
        
        data = utils.file_get(self.config_file)
        options = utils.parse_headers(data)
        
        self.name           = options['name']
        self.tagline        = options['tagline']
        self.root_url       = options['root_url']
        
        utils.dir_make(out_dir)
        utils.dir_copy(self.static_dir, out_dir)
        self.env = utils.create_jinja_env(self.templates_dir)
    
    def get_posts(self):
        """returns a list of all posts objects"""
        files = utils.file_list(self.posts_dir, '.txt')
        return sorted([Page.make_post(self, file) for file in files],
            key=lambda x: x.date, reverse=True)
    
    def get_pages(self):
        """returns a list of all pages objects"""
        files = utils.file_list(self.pages_dir)
        return sorted([Page.make_page(self, file) for file in files],
            key=lambda x: x.date, reverse=True)
    
    def write_html(self, post):
        if(post.template):
            template = self.env.get_template(post.template)
            utils.file_put(path.join(self.out_dir, post.url),
                template.render(blog=self, post=post))
        else:
            utils.file_put(path.join(self.out_dir, post.url),
                post.content)
        
    
    @staticmethod
    def dir_init(dir):
        utils.dir_make(path.join(dir, '_posts'))
        utils.dir_make(path.join(dir, '_pages'))
        utils.dir_make(path.join(dir, '_static'))
        utils.dir_make(path.join(dir, '_templates'))
        utils.file_put(dir, 'config.txt', DEFAULT_CONFIG)
        pass
    
    def compile(self):
        """Used for command-line usage, compiles the blog"""
        for post in self.get_posts():
            self.write_html(post)
        for page in self.get_pages():
            self.write_html(page)
          
    
    def __repr__(self):
        return 'Blog.Engine(%s)' % root_url
        
# modification of config created here: https://gist.github.com/cscorley/9144544
try:
  from urllib.parse import quote  # Py 3
except ImportError:
  from urllib2 import quote  # Py 2
import os
import sys
import re

f = None
for arg in sys.argv:
  if arg.endswith('.ipynb'):
    f = arg.split('.ipynb')[0]
    break


c = get_config()
c.NbConvertApp.export_format = 'markdown'
# c.MarkdownExporter.template_path = ['/home/tdos/.ipython/templates'] #
# point this to your jekyll template file
c.MarkdownExporter.template_file = './jekyll.tpl'
# c.Application.verbose_crash=True

c.NbConvertApp.output_files_dir = '../images/{notebook_name}_files'
# c.FilesWriter.relpath = '../images/'
c.ExtractOutputPreprocessor.output_filename_template = '{cell_index}_{index}{extension}'

# modify this function to point your images to a custom path
# by default this saves all images to a directory 'images' in the root of
# the blog directory


def path2support(path):
  """Turn a file path into a URL"""
  return '/images/%s_files/%s' %  (f.lower(), os.path.basename(path))


def userfriendly_title(title):
  expr = re.compile('\d{4}-\d{2}-\d{2}-')
  title = re.sub(expr, '', title)
  return title.replace('-', ' ')

def markdown_changes(md):

  # convert inline maths: $y=x^2$ to $$y=x^2$$
  expr = re.compile('(?<!\$)\$(?!\$)')
  md = re.sub(expr, '$$', md)

  # header links
  md = re.sub(r'\(#.*?\)', lambda x: x.group(0).lower(), md, flags=re.M);

  return md


c.MarkdownExporter.filters = {
  'path2support': path2support,
  'userfriendly_title': userfriendly_title,
  'markdown_changes': markdown_changes
  }

if f:
  c.NbConvertApp.output_base = f.lower().replace(' ', '-')
  # point this to your build directory
  c.FilesWriter.build_directory = '../_posts'

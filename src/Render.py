from jinja2 import Environment, FileSystemLoader
import os

class TemplateRender:
    def __init__(self, server, template_dir="templates"):
        self.template_dir = template_dir
        self.templateEnv = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(server.context)), template_dir)))

    def render(self, template_file, data=None):
        if data is None:
            data = {}
        return self.templateEnv.get_template(template_file).render(data)
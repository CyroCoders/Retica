from jinja2 import Environment, FileSystemLoader
import os

class TemplateRender:
    """ A Template Renderer
    
    :param server: The server to use.
    :type server: Server
    :param template_dir: The directory to use for templates.
    :type template_dir: str
    
    :rtype: TemplateRender
    """
    def __init__(self, server, template_dir="templates"):
        """ Initialize the Template Renderer.
        
        :param server: The server to use.
        :type server: Server
        :param template_dir: The directory to use for templates.
        :type template_dir: str
        
        :rtype: TemplateRender
        """
        self.template_dir = template_dir
        self.templateEnv = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(server.context)), template_dir)))

    def render(self, template_file, data=None):
        """ Render a template.

        :param template_file: The template file to use.
        :type template_file: str
        :param data: The data to use.
        :type data: dict

        :rtype: str
        """
        if data is None:
            data = {}
        return self.templateEnv.get_template(template_file).render(data)
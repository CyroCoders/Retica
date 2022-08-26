import Retica
import Retica.Render

retica = Retica.Server(__name__)

templator = Retica.Render.TemplateRender(retica,template_dir="Templates")

libraries = '//libraries//'

metadata = '//metadata//'

@retica.create_endpoint("/")
def index(request: Retica.Request.request, response: Retica.Response.response, **data):
    data['libraries'] = libraries
    data['metadata'] = metadata
    response.body = templator.render("index.jinja", data)
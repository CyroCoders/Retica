import argparse

def main():
    args = argparse.ArgumentParser(description="The Retica CLI. Retica Is A Performant, Easy To Use Web Server Based On Python With HTTPS & Plugins Support.")
    args.add_argument("-c", "--create", help="Create a new project.", default=True, action="store_true")

    args = args.parse_args()
    if args.create:
        create()

def create():
    project_name = str(input("Project Name: ") or "Retica Project")
    templates_folder = str(input("Templates Folder: ") or "Templates")
    plugins_folder = str(input("Plugins Folder: ") or "Plugins")

    print("Creating project...")

    import os
    os.makedirs(project_name, exist_ok=True)
    os.makedirs(os.path.join(project_name, templates_folder), exist_ok=True)
    os.makedirs(os.path.join(project_name, plugins_folder), exist_ok=True)
    os.makedirs(os.path.join(project_name, "static"), exist_ok=True)

    with open(os.path.join(project_name, "app.py"), "w") as f:
        f.write('import Retica\n')
        f.write('import Retica.Render\n')
        f.write('retica = Retica.Server(__name__)\n\n')
        f.write('templator = Retica.Render.TemplateRender(retica)\n\n')
        f.write('@retica.create_endpoint("/hello/{name}")\n')
        f.write('def index(request: Retica.Request.request, response: Retica.Response.response, **data):\n')
        f.write('    response.body = f"Hello {data[\'name\']}"\n\n')

    with open(os.path.join(project_name, "run.py"), "w") as f:
        f.write('from app import retica\n')
        f.write('from Retica import Sockets\n\n')
        f.write('http_socket = Sockets.HTTP_Socket(Sockets.gethostname(), 80)\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    retica.run([http_socket])\n')



if __name__ == "__main__":
    main()
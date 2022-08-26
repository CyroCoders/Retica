def create(args):
    frontend_libraries = {
                            'React': [
                                '<script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>',
                                '<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>',
                                '<script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>'
                            ],
                            'Vue': [
                                '<script src="https://unpkg.com/vue@3"></script>'
                            ],
                        }
    project_name = str(input("Project Name: ") or "Retica Project")
    project_description = str(input("Project Description: ") or "Retica Is A Performant, Easy To Use Web Server Based On Python With HTTPS & Plugins Support.")
    project_author = str(input("Project Author: ") or "CyroCoders")
    project_keywords = str(input("Project Keywords: ") or "Retica,Python,Web Server,Web Framework,CyroCoders")

    if input("Import Frontend Libraries? (y/n) ") == "y":
        for index, value in enumerate(frontend_libraries.keys()):
            print(f"{index}. {value}")
        frontend_libraries_selection = input("Select Frontend Library(Separate With ','. No Space): ")

    print("Creating project...")

    import tarfile
    import os
    
    file = tarfile.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/default-homepage.tar.gz"))
    file.extractall(os.path.join(os.getcwd(), project_name))


    with open(os.path.join(os.getcwd(), project_name, "app.py"), "r") as in_data:
        in_data = in_data.readlines()
        
    with open(os.path.join(os.getcwd(), project_name, "app.py"), "w") as out_data:
        for line in in_data:
            if line.startswith("libraries = "):
                if frontend_libraries_selection:
                    out_data.write("libraries = {\n")
                    for lib in frontend_libraries_selection.split(","):
                        print(list(frontend_libraries.keys())[0])
                        out_data.write(f"   '{list(frontend_libraries.keys())[int(lib)]}': [\n")
                        for script in list(frontend_libraries.values())[int(lib)]:
                            out_data.write(f"       '{script}',\n")
                        out_data.write("   ],\n")
                    out_data.write("}\n")
                else:
                    out_data.write("libraries = {}\n")
            elif line.startswith("metadata = "):
                out_data.write("metadata = {\n")
                out_data.write(f"   'name': '{project_name}',\n")
                out_data.write(f"   'description': '{project_description}',\n")
                out_data.write(f"   'author': '{project_author}',\n")
                out_data.write(f"   'keywords': '{project_keywords}',\n")
                out_data.write("}\n")
            else:
                out_data.write(line)
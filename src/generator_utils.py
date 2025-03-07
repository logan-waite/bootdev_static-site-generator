import os
import shutil
import re

from markdown_html_converter import markdown_to_html_node


def __do_copy(source, target):
    paths = os.listdir(source)
    for _path in paths:
        path = os.path.join(source, _path)
        print(f"Copying {path}")
        if os.path.isfile(path):
            shutil.copy(path, target)
        else:
            _target = os.path.join(target, _path)
            if not os.path.exists(_target):
                os.mkdir(_target)
            __do_copy(path, _target)


def copy_directory(source, target):
    # check if target exists
    if os.path.exists(target):
        # if it does, empty it
        shutil.rmtree(target)

    # create it
    os.mkdir(target)

    # copy all files and subdirectories from source
    if os.path.exists(source):
        __do_copy(source, target)
    else:
        raise Exception(f"Source directory {source} does not exist!")


def extract_title(markdown):
    title = re.search(r"^# (.+)", markdown)
    if title is None:
        raise Exception("No title found!")
    return title.group(1)


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} using {template_path} and putting in {dest_path}")
    html = ""
    title = ""
    new_file = ""
    with open(from_path) as from_file:
        markdown = from_file.read()
        html = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

    with open(template_path) as template_file:
        template = template_file.read()
        new_file = template.replace("{{ Title }}", title)
        new_file = new_file.replace("{{ Content }}", html)
        new_file = new_file.replace('href="/', f"href=\"{basepath}")
        new_file = new_file.replace('src="/', f"src=\"{basepath}")

    with open(dest_path, 'w') as md_file:
        md_file.write(new_file)


def generate_page_recursively(start_path, template_path, dest_path, basepath):
    if os.path.exists(start_path):
        paths = os.listdir(start_path)
        for _path in paths:
            path = os.path.join(start_path, _path)
            target_path = os.path.join(dest_path, _path)
            if os.path.isfile(path):
                generate_page(path, template_path,
                              target_path[:-3] + '.html', basepath)
            else:
                if not os.path.exists(target_path):
                    os.mkdir(target_path)
                generate_page_recursively(
                    path, template_path, target_path, basepath)

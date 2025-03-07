import sys
from generator_utils import copy_directory, generate_page_recursively


def main():
    basepath = sys.argv[1] if len(sys.argv) == 2 else ""
    copy_directory('static', 'docs')
    generate_page_recursively(
        'content', 'template.html', 'docs', basepath)


if __name__ == "__main__":
    main()

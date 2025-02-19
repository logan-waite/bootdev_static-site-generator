from generator_utils import copy_directory, generate_page_recursively


def main():
    copy_directory('static', 'public')
    generate_page_recursively(
        'content', 'template.html', 'public')


if __name__ == "__main__":
    main()

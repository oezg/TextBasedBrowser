from collections import deque
import argparse
import os
import requests
import shutil
from bs4 import BeautifulSoup
import colorama


def get_dir_name():
    parser = argparse.ArgumentParser(
        description="This is a text-based browser. Please provide a name for the directory"
    )
    parser.add_argument("directory_name", help="Provide a name for the directory")
    args = parser.parse_args()
    try:
        os.mkdir(args.directory_name)
    except FileExistsError:
        print("Error:", args.directory_name, "exists")
    else:
        return args.directory_name


def save_content(directory, url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Incorrect URL")
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        file_name = url.replace("https://", "")
        file_path = os.path.join(directory, file_name[:file_name.rfind(".")])
        if os.access(file_path, os.F_OK):
            pass
        else:
            with open(file_name, "w", encoding="utf-8") as file:
                text = ''
                for tag in soup.find_all(True):
                    if tag.name == "a":
                        text += colorama.Fore.BLUE + tag.get_text()
                    elif tag.get_text():
                        text += colorama.Style.RESET_ALL + tag.get_text()
                file.write(text)
            shutil.move(file_name, directory)
        return text


def main():
    dir_name = get_dir_name()
    stack = deque()
    current_tab = ""
    while dir_name:
        url = input()
        if url == "exit":
            break
        elif url == "back":
            print(stack.pop())
        elif "." not in url[:-2]:
            print("Error: Incorrect URL")
        else:
            url = url if url.startswith("https://") else "https://" + url
            stack.append(current_tab)
            current_tab = save_content(dir_name, url)
            print(current_tab)


if __name__ == "__main__":
    main()

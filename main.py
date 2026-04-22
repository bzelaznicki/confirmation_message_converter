import argparse
import os
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description="Confirmation message converter")
    parser.add_argument("file_path", help="The file path")
    parser.add_argument("--url", help="The confirmation message link, default set to https://getresponse.com/?confirmation_click")
    
    args = parser.parse_args()

    file_path = args.file_path
    url = args.url


    file_data = parse_html_file(file_path, url)

    write_to_new_file(file_path, file_data)

def read_file_data(file_path:  str) -> str: 
    
    with open(file_path, 'r') as read_file:
        return read_file.read()

def parse_html_file(file_path: str, url: str = "https://getresponse.com/?confirmation_click"):

    file_data = read_file_data(file_path)

    soup = BeautifulSoup(file_data, "html.parser")

    for a in soup.find_all("a", href=url):
        a["href"] = "{{LINK `confirm`}}"

    for td in soup.find_all("td"):
        classes = td.get("class", [])
        if any(c.startswith("gr-footer-") for c in classes):
            td.decompose()

    return soup.prettify()

def write_to_new_file(file_path: str, file_content: str):
    input_dir = os.path.dirname(file_path)
    input_filename = os.path.basename(file_path)

    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}_converted{ext}"

    output_filepath = os.path.join(input_dir, output_filename)

    with open(output_filepath, 'w', encoding="utf-8") as f:
        f.write(str(file_content))



if __name__ == "__main__":
    main()

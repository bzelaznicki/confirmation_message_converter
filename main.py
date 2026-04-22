import argparse
import os
from bs4 import BeautifulSoup

DEFAULT_PLACEHOLDER = "https://getresponse.com/?confirmation_click"
CONFIRMATION_LINK = "{{LINK `confirm`}}"
DYNAMIC_CONTENT_TAGS = {
    "[[firstname]]": "{{CONTACT `subscriber_first_name`}}",
    "[[lastname]]": "{{CONTACT `subscriber_last_name`}}",
    "[[email]]": "{{CONTACT `email`}}",
    "[[name]]": "{{CONTACT `name`}}",
}


def main():
    parser = argparse.ArgumentParser(description="Confirmation message converter")
    parser.add_argument("file_path", help="The file path")
    parser.add_argument("--url", help="The confirmation message link, default set to https://getresponse.com/?confirmation_click")
    
    args = parser.parse_args()

    file_path = args.file_path
    url = args.url if args.url else DEFAULT_PLACEHOLDER

    file_data = parse_html_file(file_path, url)
    plain_text = extract_plain_text_version(file_data)
    
    write_to_html_file(file_path, file_data)
    write_to_txt_file(file_path, plain_text)
    


def read_file_data(file_path:  str) -> str: 
    
    with open(file_path, 'r') as read_file:
        return read_file.read()

def parse_html_file(file_path: str, url: str = DEFAULT_PLACEHOLDER):

    file_data = read_file_data(file_path)

    soup = BeautifulSoup(file_data, "html.parser")


    for a in soup.find_all("a", href=url):
        a["href"] = CONFIRMATION_LINK

    for td in soup.find_all("td"):
        classes = td.get("class", [])
        if any(c.startswith("gr-footer-") or c.startswith("gr-headerviewonline-") for c in classes):
            td.decompose()

    html_content = soup.prettify()

    for old, new in DYNAMIC_CONTENT_TAGS.items():
        html_content = html_content.replace(old, new)

    return html_content

def write_to_html_file(file_path: str, file_content: str):
    input_dir = os.path.dirname(file_path)
    input_filename = os.path.basename(file_path)

    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}_converted{ext}"

    output_filepath = os.path.join(input_dir, output_filename)

    with open(output_filepath, 'w', encoding="utf-8") as f:
        f.write(str(file_content))

def extract_plain_text_version(file_content: str) -> str:

    soup = BeautifulSoup(file_content, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    for a in soup.find_all("a", href=CONFIRMATION_LINK):
        a.replace_with(CONFIRMATION_LINK)

    return soup.get_text(separator="\n", strip=True)

def write_to_txt_file(file_path: str, file_content: str):
    input_dir = os.path.dirname(file_path)
    input_filename = os.path.basename(file_path)

    base, _ = os.path.splitext(input_filename)
    output_filename = f"{base}_converted.txt"

    output_filepath = os.path.join(input_dir, output_filename)

    with open(output_filepath, 'w', encoding="utf-8") as f:
        f.write(str(file_content))




if __name__ == "__main__":
    main()

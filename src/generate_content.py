from html_blocks import *
import os
import pathlib

def generate_page(from_path, template_path, dest_path):
    with open(from_path, encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()
    # print(f"{from_path} closed: {markdown_file.closed}")

    with open(template_path, encoding="utf-8") as template_file:
        template = template_file.read()
    # print(f"{template_path} closed: {template_file.closed}")

    page_content = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)

    final_page = template.replace("{{ Title }}", page_title)
    final_page = final_page.replace("{{ Content }}", page_content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "x", encoding="utf-8") as f:
        f.write(final_page)
    # print(f"{dest_path} closed: {f.closed}")
    
def generate_pages_recursive(content_path, template_path, destination_path):
    content_dir = os.listdir(content_path)
    print(f"destination: {destination_path}")
    print(f"dir {content_path}: {content_dir}")
    for filename in content_dir:
        file_path = pathlib.Path(content_path, filename)
        print(f"full path: {file_path}")

        if os.path.isfile(file_path) and file_path.suffix == ".md":
            print(f"markdown file: {filename}")
            page_path = pathlib.Path(destination_path, filename).with_suffix(".html")
            print(f"destination: {page_path}")
            generate_page(file_path, template_path, page_path)

        elif os.path.isdir(file_path):
            print(f"folder: {filename}")
            destination_path = os.path.join(destination_path, filename)
            print(f"new destination: {destination_path}")
            generate_pages_recursive(file_path, template_path, destination_path)



def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if not blocks[0].startswith("# "):
        raise Exception("Missing h1 header")
    return blocks[0][2:].strip()

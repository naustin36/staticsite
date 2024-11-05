from html_blocks import *
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

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
    
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if not blocks[0].startswith("# "):
        raise Exception("Missing h1 header")
    return blocks[0][2:].strip()

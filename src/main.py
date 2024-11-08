from textnode import TextNode, TextType
from copystatic import copy_over_directory
from generate_content import generate_page, generate_pages_recursive
import os
import shutil

static_path = "./static"
public_path = "./public"

content_path = "./src/content"
template_path = "template.html"

def main():
    print(f"Deleting directory {public_path} for clean copy...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print(f"copying files from static directory {static_path} to public directory {public_path}")
    copy_over_directory(static_path, public_path)
    
    print(f"Generating pages from {content_path} using {template_path} -> {public_path}")
    # print(f"Generating page from {content_path} using{template_path} -> {public_path}")
    # generate_page(content_path, template_path, "public/index.html")
    generate_pages_recursive(content_path, template_path, public_path)

main()

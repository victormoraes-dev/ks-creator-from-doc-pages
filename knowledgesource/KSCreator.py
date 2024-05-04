import os

import requests
from bs4 import BeautifulSoup

base_url = "https://ai.stackspot.com"

doc_links = [
    "https://ai.stackspot.com/docs/",
    "https://ai.stackspot.com/docs/stackspot-ai/about",
    "https://ai.stackspot.com/docs/stackspot-ai/coming-soon",
    "https://ai.stackspot.com/docs/stackspot-ai/ide-usage",
    "https://ai.stackspot.com/docs/stackspot-ai/extensions",
    "https://ai.stackspot.com/docs/stackspot-ai/concepts",
    "https://ai.stackspot.com/docs/stackspot-ai/tokens",
    "https://ai.stackspot.com/docs/stackspot-ai/try-feature",
    "https://ai.stackspot.com/docs/stackspot-ai/best-practices",
    "https://ai.stackspot.com/docs/account/about",
    "https://ai.stackspot.com/docs/account/invite-members",
    "https://ai.stackspot.com/docs/knowledge-source/ks",
    "https://ai.stackspot.com/docs/knowledge-source/create-knowledge-source",
    "https://ai.stackspot.com/docs/knowledge-source/add-knowledge-source-workspace",
    "https://ai.stackspot.com/docs/knowledge-source/update-knowledge-source",
    "https://ai.stackspot.com/docs/knowledge-source/create-update-via-api",
    "https://ai.stackspot.com/docs/knowledge-source/ks-default",
    "https://ai.stackspot.com/docs/knowledge-source/manage-knowledge-source",
    "https://ai.stackspot.com/docs/quick-commands/quick-command",
    "https://ai.stackspot.com/docs/quick-commands/create-custom-quick-command",
    "https://ai.stackspot.com/docs/quick-commands/create-remote-qc",
    "https://ai.stackspot.com/docs/quick-commands/example-quick-command",
    "https://ai.stackspot.com/docs/quick-commands/use-custom-quickcommand",
    "https://ai.stackspot.com/docs/community-hub/",
    "https://ai.stackspot.com/docs/tutorials/create-workspace",
    "https://ai.stackspot.com/docs/tutorials/create-stack-ai",
    "https://ai.stackspot.com/docs/tutorials/monitor-resources",
    "https://ai.stackspot.com/docs/tutorials/community-hub",
    "https://ai.stackspot.com/docs/troubleshooting"
]


def download_image(image_url, save_path):
    try:
        # Check if the image URL is relative and prepend the base URL
        if image_url.startswith('/'):
            image_url = base_url + image_url

        response = requests.get(image_url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Successfully downloaded {save_path}")
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")


def scrape_and_save(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.replace(' ', '_').replace('/', '_') + '.md'
        filepath = os.path.join('knowledge_sources', title)

        content_list = []  # List to store both text and images with their order

        # Extract text and images, storing them in content_list with their type
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
            if tag.name == 'img':
                img_url = tag.get('src')
                if img_url:
                    img_filename = img_url.split('/')[-1]
                    img_save_path = os.path.join('knowledge_sources', 'images', img_filename)
                    download_image(img_url, img_save_path)
                    content_list.append(('img', img_save_path))
            else:
                content_list.append(('text', tag.get_text()))

        # Write the content to the markdown file in the correct order
        with open(filepath, 'w', encoding='utf-8') as file:
            for content_type, content in content_list:
                if content_type == 'text':
                    file.write(content + '\n\n')
                elif content_type == 'img':
                    file.write(f"![Image]({content})\n\n")

        print(f"Successfully created {filepath}")
    except Exception as e:
        print(f"Failed to scrape {link}: {e}")


# Ensure the knowledge_sources directory exists
os.makedirs('knowledge_sources/images', exist_ok=True)

# Iterate over the documentation links and scrape content
for link in doc_links:
    scrape_and_save(link)

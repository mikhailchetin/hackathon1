from openai import OpenAI
import os
import dotenv
import re
from bs4 import BeautifulSoup
import random

dotenv.load_dotenv()

# Set up your OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def send_html_to_gpt4(html_content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": f"Improve UI of the following HTML element. Return only the improved HTML, nothing else::\n\n{html_content}"} #Come up with better UI for an HTML and return only the modified HTML
            ],
        )

        content = response.choices[0].message.content
        content = re.sub(r'^```html\n|```$', '', content, flags=re.MULTILINE)
        return content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def read_html_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
    

def get_next_index(directory):
    pattern = re.compile(r'index(\d+)\.html')
    max_index = -1
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            index = int(match.group(1))
            max_index = max(max_index, index)
    return max_index + 1

def get_output_file_path(input_file_path):
    directory = os.path.dirname(input_file_path)
    next_index = get_next_index(directory)
    new_filename = f"index{next_index}.html"
    return os.path.join(directory, new_filename)

# Example HTML content

html_file_path = "downloaded_websites/hockeystack.com/hockeystack.com/hockeystack.com/index.html"  # Change this to your HTML file path
#html_file_path = "downloaded_websites/github.com/github.com/github.com/index.html"  # Change this to your HTML file path
output_html_file = get_output_file_path(html_file_path)

# Read HTML from file
html_content = read_html_from_file(html_file_path)

print("TOTAL LENGTH",len(html_content))
def remove_first_and_last_lines(text):
    lines = text.split('\n')
    if len(lines) > 2:
        return '\n'.join(lines[1:-1])
    return text 

if not html_content.startswith("Error"):
    # Send the HTML to GPT-4 and print the response
    soup = BeautifulSoup(html_content, 'html.parser')
    # with open(html_file_path, 'w', encoding='utf-8') as file:
    #     file.write(str(soup))
    # exit()
    # Get all buttons

    # regex = re.compile('.*button.*')
    # all_elements = soup.find_all("div", {"class" : regex})
    # Find all elements that contain a string
    all_elements = soup.find_all(string=True)
    
    print("TOTAL ELEMENTS",len(all_elements))
    # Select 5 random elements
    # Shuffle all elements to randomize the order
    # random.shuffle(all_elements)
    
    improved_count = 0
    while improved_count < 100:
        element = random.choice(all_elements)
        if not element.parent:
            continue

        print("ELEMENT STRING", element.string)
        original_html = str(element)
        if len(original_html) < 1000 and len(element.string) > 10:
            print("LENGTH", len(original_html))
            print("ELEMENT", original_html)
            print()
            
            improved_html = send_html_to_gpt4(original_html)
            
            print("IMPROVED LENGTH", len(improved_html))
            print("IMPROVED ELEMENT", improved_html)
            print()
            # Replace the original element with the improved version
            improved_soup = BeautifulSoup(improved_html, 'html.parser')

            # try:
            element.replace_with(improved_soup)
            improved_count += 1
            # except Exception as e:
            #     print("FAILED TO REPLACE")
            #     continue

    new_html = str(soup)
    print("NEW LENGTH",len(new_html))
    #print("NEW HTML",new_html)

    with open(output_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

else:
    print(html_content)  

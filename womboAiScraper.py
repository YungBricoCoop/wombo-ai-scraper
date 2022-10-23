import os
from queue import Queue
import threading
import time
import requests
from io import BytesIO



# Import third part modules
from PIL import Image
from rich import print
from rich.prompt import Prompt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


# Chrome driver path
CHROME_DRIVER_PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# Page elements xpath
XPATH_TEXT_FIELD = '//*[@id="blur-overlay"]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/input'
XPATH_IMG_STYLE = '//img[@class="Thumbnail__StyledThumbnail-sc-p7nt3c-0 hxvLKC"'
XPATH_IMG_STYLES_CONTAINER = '//div[@class="Thumbnail__StyledThumbnailContainer-sc-p7nt3c-1 gqZQZu"]'
XPATH_BTN_GENERATE = '//*[@id="blur-overlay"]/div/div/div/div[2]/button'
XPATH_RESULT_IMG = '//img[@class="ArtCard__CardImage-sc-67t09v-2 dOXnUm"]'
XPATH_BTN_GO_BACK = '//*[@id="blur-overlay"]/div/div/div[1]/div[1]/div/button'

# Crop coordinates (x1, y1, x2, y2)
CROP_COORDINATES = (81, 232, 999, 1756)

# Styles of images to generate
STYLES = ["Bad Trip","Cartoonist","HDR","Realistic","Meme", "Isometric","Analogue","Retro-Futurism",
            "Paint","Polygon","Gouache","Line-Art","Malevolent","Surreal","Throwback", "Street Art",
            "No Style", "Ghibli", "Melancholic", "Pandora", "Daydream", "Provenance", "Arcane", "Toasty",
            "Transitory", "Etching", "Mystical", "Dark Fantasy", "Psychic", "HD", "Vibrant", "Fantasy Art",
            "Steampunk", "Rose Gold", "Wuhtercuhler", "Psychedelic", "Synthwave", "Ukiyoe"]

# Default number of instances to run
INSTANCES = 1

# Image extension
IMG_EXTENSIONS = ".png"

class Worker(threading.Thread):
    def __init__(self, queue, id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id

    def get_element_from_xpath(self, xpath, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def crop_an_save_image(self, image_src, style, item):
        image_name = item.replace(" ", "_").lower()
        nb_of_same_images = len([name for name in os.listdir(style) if name.split("-")[0] == image_name])
        image_name = image_name + "-" + str(nb_of_same_images) + IMG_EXTENSIONS
        image = Image.open(BytesIO(requests.get(image_src).content))
        image = image.crop(CROP_COORDINATES)
        image.save(f"{style}/{image_name}")

    def run(self):
        # Create a new Chrome session
        self.browserOptions = Options()
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,options=self.browserOptions)
        self.actions = ActionChains(self.driver)
        self.driver.get("https://app.wombo.art/")

        # While there are items in the queue
        while self.queue.qsize() > 0:
            item, style = self.queue.get()
            print(f"Thread [bold cyan]#{self.id}[/bold cyan] : [bold violet]Generating...[/bold violet] [bold cyan]({item})[/bold cyan] with style [bold cyan]({style})[/bold cyan]")
            
            # Scroll and click on the image style
            image_style = self.get_element_from_xpath(f'{XPATH_IMG_STYLE} and @alt="{style}"]')
            self.actions.move_to_element(image_style).perform()
            image_style.click()

            # Type the text in the text field
            input_text = self.get_element_from_xpath(XPATH_TEXT_FIELD)
            input_text.clear()
            input_text.send_keys(item)

            # Click on the generate button
            generate_button = self.get_element_from_xpath(XPATH_BTN_GENERATE)
            generate_button.click()

            # Wait for the result image to load
            result_image = self.get_element_from_xpath(XPATH_RESULT_IMG, 100)
            image_src = result_image.get_attribute("src")
            self.crop_an_save_image(image_src, style, item)
            
            print(f"Thread [bold cyan]#{self.id}[/bold cyan] : [bold violet]Saved[/bold violet] [bold cyan]({item})[/bold cyan] with style [bold cyan]({style})[/bold cyan]")

            # Click on the go back button
            go_back_button = self.get_element_from_xpath(XPATH_BTN_GO_BACK)
            go_back_button.click()

            self.queue.task_done()

        print(f"Thread [bold cyan]#{self.id}[/bold cyan] : [bold violet]Finished[/bold violet]")
        time.sleep(0.5)
        
        # Quit the Chrome driver
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    # Set the default directory to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Asks for number of selenium instances to run
    instances = Prompt.ask("How many instances do you want to run", default=str(INSTANCES))
    try: instances = int(instances)
    except: instances = INSTANCES
    
    # Asks for what to generate
    items_to_generate = Prompt.ask("What do you want to generate (separate items with commas)", default="chicken")
    items_to_generate = items_to_generate.split(",") if "," in items_to_generate else [items_to_generate]
    for i, item in enumerate(items_to_generate):
        item = item.strip()
        if "#" in item: 
            item_instances = int(item.split("#")[1]) -1
            item = item.split("#")[0]
            items_to_generate.extend([item for x in range(item_instances)])
        items_to_generate[i] = item

    # Asks for which style(s) to use
    print(f"[bold cyan]Available styles[/bold cyan] : [bold violet] {', '.join(STYLES)} [/bold violet]")
    items_styles = Prompt.ask("Which styles (separate styles with commas)", default=STYLES[0])
    items_styles = items_styles.split(",") if "," in items_styles else [items_styles]
    for  i, style in enumerate(items_styles):
        style = style.strip()
        if style not in STYLES:
            style = STYLES[0]
        items_styles[i] = style
        if not os.path.exists(style): os.mkdir(style)

    # Create the queue
    queue = Queue()

    # Create the workers
    for i in range(instances):
        worker_id = i + 1
        print(f"Thread [bold cyan]#{worker_id}[/bold cyan] : [bold violet]Starting...[/bold violet]")
        worker = Worker(queue, worker_id)
        #worker.setDaemon(True)
        worker.start()
        print(f"Thread [bold cyan]#{worker_id}[/bold cyan] : [bold violet]Ready[/bold violet]")

    # Fill the queue
    for item in items_to_generate:
        for style in items_styles:
            queue.put((item, style))

    # Wait for the queue to be empty
    queue.join()

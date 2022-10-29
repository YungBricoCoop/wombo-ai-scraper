# [Wombo AI Scraper](https://app.wombo.art/)

This script is simply made to scrape the [Wombo AI](https://app.wombo.art/) website and save the images in a folder.


## ⬇️ Download

```bash
git clone https://github.com/YungBricoCoop/WomboAiScraper.git
cd WomboAiScraper
pip install -r requirements.txt
```
## ⚠️ Warning

This script use selenium so make sure you specifies the **path**(LINE 16 in the script) to your **chromedriver**.

The Wombo website is subject to change so you might need to update the XPATH requests to find elements on the page.

If you make to many requests to the website, you might get timed out to.

## ✔️ Usage

First you can edit the categories if you want on **line 25**. By default categories are: ["Mystical","HD","Synthwave","Vibrant"]

To start the script you just need to run the following command : <code>python womboAiScraper.py </code>
Then you need to answer the questions : 
```python
> How many instances do you want to run (1): 5
> What do you want to generate (separate items with commas) (chicken): space, stars, galaxy#2
> Which styles (separate styles with commas) (Bad Trip): Synthwave, HDR
```

Instances : 
> How many instances of chrome do you want to run (*a number between* **5** *and* **10** *is favorable to generate several dozen images quickly*, *the use of a large number of instances can create problems*)

Items : 
> What do you want to generate, to indicate several items separate them with commas, if you want to generate several instances of the same item, add an hashtag and a number after the item name (ex: galaxy#2)

Styles :
> Which styles do you want to use, to indicate several styles separate them with commas (the script displays the available styles)


The next chapter shows the images generated with the theme of **Space**

## 👍 Result

>## Mystical 

![Space](./Space/0SpaceMystical.png)
>## HD 

![Space](./Space/0SpaceHD.png)
>## Synthwave 

![Space](./Space/0SpaceSynthwave.png)
>## Vibrant 

![Space](./Space/0SpaceVibrant.png)
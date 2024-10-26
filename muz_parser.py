import sys
import re
import logging
import bs4
import requests
# import lxml

BASE_URL = 'https://www.lastminutemusicians.com'
YOUTUBE_URL = 'https://www.youtube.com/watch?v='

logging.basicConfig(level=logging.ERROR, stream=sys.stdout)



def get_subcategories(category: str) -> list[dict]:
    response = requests.get(BASE_URL + category, timeout=10)
    sub_categories = list()
    logging.debug(response.status_code)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    sub_cats = soup.find_all('div', class_='col-xs-6 col-md-3 margin-bottom-big')
    for sub in sub_cats:
        link = sub.find('a')['href']
        logging.debug(link)
        title = sub.find('h2').text
        members = sub.find('p').text
        logging.debug(title, members)
        image_bg = BASE_URL + sub.find('a', class_='topLevelCatImage')['data-inline-bg-url']
        logging.debug(image_bg)
        sub_categories.append(
            {
                'link': link,
                'title': title,
                'members': members,
                'image_bg': image_bg
            }
        )
    return sub_categories


def get_musicians(sub_cat_link: str) -> list[dict]:
    full_info = list()
    response = requests.get(BASE_URL + sub_cat_link, timeout=10)
    logging.debug(response.status_code)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    musicians = soup.find_all('div', class_="search-result panel panel-default")
    for musician in musicians:
        video_link = musician.find('div', class_="video-player")
        media_type = None
        media_link = None
        if video_link and video_link.get('data-youtube-id'):
            video_link = video_link['data-youtube-id']
            media_type = 'video'
            media_link = video_link
            logging.debug(video_link)
        elif video_link and video_link.get('data-mp3-id'):
            audio_link = video_link['data-mp3-id']
            media_type = 'audio'
            media_link = audio_link
            logging.debug(audio_link)
        else:
            search_result = musician.find('a', class_="searchResultsImage")
            if search_result.get('data-inline-bg-url'):
                img_link = search_result.get('data-inline-bg-url')
            else:

                style_tag = search_result.get('style')
                pattern = r"\(([^)]+)\);"
                match = re.search(pattern, style_tag)
                if match:
                    img_link = match.group(1)
            media_type = 'image'
            media_link = img_link
            logging.debug(img_link)
        musician_info = musician.find('div', class_="listingResult")
        musician_title = musician_info.find('h2').text
        musician_link = BASE_URL + musician_info.find('a')['href']
        musician_description = musician.find('div', class_="overflowHidden small short-description").text
        location_info = musician.find('div', class_="smaller margin-top-sm").find_all('div', class_="overflowHidden")
        for loc in location_info:
            if loc.find('p'):
                location = loc.find('p').text.strip()
                continue
        price = musician.find('span', class_="tooltipActiveNoDelay imgLink brand-primary").text[:-1]
        logging.debug(price)
        logging.debug(location)
        logging.debug(musician_title)
        logging.debug(musician_link)
        logging.debug(musician_description)
        full_info.append(
            {
                'title': musician_title,
                'description': musician_description,
                'location': location,
                'price': price,
                'link': musician_link,
                'media_type': media_type,
                'media_link': media_link
            }
        )
    return full_info
    

if __name__ == '__main__':
    # tests
    get_subcategories('/bands.html')
    get_subcategories('/musicians.html')
    get_subcategories('/entertainment-services.html')
    # get_musicians('https://www.lastminutemusicians.com/search/sound_engineers.html')
    
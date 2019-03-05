import re
import vk
import os

from exceptions import IncorrectInputException
from exceptions import WrongUrlException
from exceptions import PostWithoutImagesException

VK_API_KEY = os.environ('VK_API_KEY')


def get_images_from_post(post: dict):
    if 'attachments' not in post:
        raise PostWithoutImagesException()
    attachments = post['attachments']
    photos = []
    for attch in attachments:
        if 'photo' in attch:
            photos.append(attch['photo'])
    if len(photos) == 0:
        raise PostWithoutImagesException()
    photo_links = []
    for ph in photos:
        max_height, url = None, None
        for candidate in ph['sizes']:
            if max_height is None or max_height < candidate['height']:
                max_height, url = candidate['height'], candidate['url']
        photo_links.append(url)
    return photo_links


def get_post_data(post_id: str):
    ses = vk.Session(access_token=VK_API_KEY)
    api = vk.API(ses, v='5.92', timeout=10)
    posts = api.wall.getById(posts=[post_id])
    if len(posts) != 1:
        raise WrongUrlException()
    return posts[0]


def get_wall_id(user_string: str) -> str:
    reg = re.compile(r'wall(-+\d+_\d+)')
    search_result = reg.search(user_string)
    if search_result is None:
        raise IncorrectInputException()
    else:
        return search_result.group(1)


def process_user_request(user_string: str):
    wall_id = get_wall_id(user_string)
    post = get_post_data(wall_id)
    return get_images_from_post(post)

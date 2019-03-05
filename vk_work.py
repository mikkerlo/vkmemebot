"""
This module handle interaction with VK, mostly processing the user request to retrieve the post memes.
In the user side just use get_photo_links_user_request method
"""
import re
import vk
import os

from exceptions import IncorrectInputException
from exceptions import WrongUrlException
from exceptions import PostWithoutImagesException

_VK_API_KEY = os.environ('VK_API_KEY')
_REGEX_WALL_ID = re.compile(r'wall(-?\d+_\d+)')


def _get_images_from_post(post: dict):
    if 'attachments' not in post:
        raise PostWithoutImagesException()
    attachments = post['attachments']
    photos = []
    for attach in attachments:
        if 'photo' in attach:
            photos.append(attach['photo'])
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


def _get_post_data(post_id: str):
    ses = vk.Session(access_token=_VK_API_KEY)
    api = vk.API(ses, v='5.92', timeout=10)
    posts = api.wall.getById(posts=[post_id])
    if len(posts) != 1:
        raise WrongUrlException()
    return posts[0]


def _get_wall_id(user_string: str) -> str:
    search_result = _REGEX_WALL_ID.search(user_string)
    if search_result is None:
        raise IncorrectInputException()
    else:
        return search_result.group(1)


def get_photo_links_user_request(user_string: str):
    wall_id = _get_wall_id(user_string)
    post = _get_post_data(wall_id)
    return _get_images_from_post(post)

import os
from pywps import configuration

import logging
LOGGER = logging.getLogger(__name__)


def esgfsearch_url():
    url = configuration.get_config_value("extra", "esgfsearch_url")
    if not url:
        LOGGER.warn("No ESGF Search URL configured. Using default value.")
        url = 'https://esgf-data.dkrz.de/esg-search'
    return url


def shapefiles_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'shapefiles')


def Rsrc_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Rsrc')


def JSsrc_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'JSsrc')


def masks_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'masks')


def static_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')


def cache_path():
    cache_path = configuration.get_config_value("cache", "cache_path")
    if not cache_path:
        LOGGER.warn("No cache path configured. Using default value.")
        cache_path = os.path.join(os.sep, "tmp", "cache")
    return cache_path


def output_path():
    try:
        output_path = configuration.get_config_value("server", "outputpath")
    except:
        output_path = None
        LOGGER.warn('no output path configured')
    return output_path


def outputUrl_path():
    try:
        outputUrl = configuration.get_config_value("server", "outputurl")
    except:
        outputUrl = None
        LOGGER.warn('no outputUrl configured')
    return outputUrl


def www_url():
    try:
        url = configuration.get_config_value("extra", "www_url")
    except:
        url = None
        LOGGER.warn('no www-url configured')
    return url

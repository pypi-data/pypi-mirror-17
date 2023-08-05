from django.conf import settings
from django.utils import six
from tinycontent.utils.importer import import_from_dotted_path


def get_filter_list():
    try:
        path_list = getattr(settings, 'TINYCONTENT_FILTER')
    except AttributeError:
        return []

    if isinstance(path_list, six.string_types):
        path_list = [path_list, ]

    return [import_from_dotted_path(path) for path in path_list]

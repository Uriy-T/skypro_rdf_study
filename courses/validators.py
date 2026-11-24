from rest_framework.serializers import ValidationError
from configuration import VIDEO_LINK

class VideoLinkValidator:

    def __init__(self, field):
        self.field = field


    def __call__(self, value):
        link_in_request = dict(value).get(self.field)
        if not bool(VIDEO_LINK.match(link_in_request)):
            raise ValidationError('Ссылка должна быть с сервиса видео хостинга YouTube')
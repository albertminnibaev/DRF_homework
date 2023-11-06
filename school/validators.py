import re
from rest_framework.serializers import ValidationError


# проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com
class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        #reg = re.compile(('?<=https://www.youtube.com/'))
        tmp_value = dict(value).get(self.field)
        if not bool(re.match(r'https://www.youtube.com/', tmp_value)):
            raise ValidationError('Video is not ok')

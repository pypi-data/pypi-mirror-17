import re

from rest_framework import serializers


class FileProxyURLSerializer(serializers.Serializer):

    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.SerializerMethodField()
    file_original_name = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.pop('base_url', None)

        super(FileProxyURLSerializer, self).__init__(*args, **kwargs)

    def get_url(self, obj):
        if not self.base_url:
            return obj.get('url')

        reo = re.compile('(?:[^/][\d\w\.]+)$')
        result = reo.findall(obj.get('url'))

        return '{}{}'.format(self.base_url, result[0])

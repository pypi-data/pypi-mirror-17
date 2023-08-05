# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_str
from ..utils import (
    float_or_none,
    int_or_none,
    try_get,
)


class CarambaTVIE(InfoExtractor):
    _VALID_URL = r'(?:carambatv:|https?://video1\.carambatv\.ru/v/)(?P<id>\d+)'
    _TESTS = [{
        'url': 'http://video1.carambatv.ru/v/191910501',
        'md5': '2f4a81b7cfd5ab866ee2d7270cb34a2a',
        'info_dict': {
            'id': '191910501',
            'ext': 'mp4',
            'title': '[BadComedian] - Разборка в Маниле (Абсолютный обзор)',
            'thumbnail': 're:^https?://.*\.jpg',
            'duration': 2678.31,
        },
    }, {
        'url': 'carambatv:191910501',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        video = self._download_json(
            'http://video1.carambatv.ru/v/%s/videoinfo.js' % video_id,
            video_id)

        title = video['title']

        base_url = video.get('video') or 'http://video1.carambatv.ru/v/%s/' % video_id

        formats = [{
            'url': base_url + f['fn'],
            'height': int_or_none(f.get('height')),
            'format_id': '%sp' % f['height'] if f.get('height') else None,
        } for f in video['qualities'] if f.get('fn')]
        self._sort_formats(formats)

        thumbnail = video.get('splash')
        duration = float_or_none(try_get(
            video, lambda x: x['annotations'][0]['end_time'], compat_str))

        return {
            'id': video_id,
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'formats': formats,
        }


class CarambaTVPageIE(InfoExtractor):
    _VALID_URL = r'https?://carambatv\.ru/(?:[^/]+/)+(?P<id>[^/?#&]+)'
    _TEST = {
        'url': 'http://carambatv.ru/movie/bad-comedian/razborka-v-manile/',
        'md5': '',
        'info_dict': {
            'id': '191910501',
            'ext': 'mp4',
            'title': '[BadComedian] - Разборка в Маниле (Абсолютный обзор)',
            'thumbnail': 're:^https?://.*\.jpg$',
            'duration': 2678.31,
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        video_url = self._og_search_property('video:iframe', webpage, default=None)

        if not video_url:
            video_id = self._search_regex(
                r'(?:video_id|crmb_vuid)\s*[:=]\s*["\']?(\d+)',
                webpage, 'video id')
            video_url = 'carambatv:%s' % video_id

        return self.url_result(video_url, CarambaTVIE.ie_key())

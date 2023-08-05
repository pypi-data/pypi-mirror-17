from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..compat import (
    compat_HTTPError,
    compat_str,
    compat_urlparse,
)
from ..utils import (
    ExtractorError,
    int_or_none,
    urlencode_postdata,
)


class LyndaBaseIE(InfoExtractor):
    _SIGNIN_URL = 'https://www.lynda.com/signin'
    _PASSWORD_URL = 'https://www.lynda.com/signin/password'
    _USER_URL = 'https://www.lynda.com/signin/user'
    _ACCOUNT_CREDENTIALS_HINT = 'Use --username and --password options to provide lynda.com account credentials.'
    _NETRC_MACHINE = 'lynda'

    def _real_initialize(self):
        self._login()

    @staticmethod
    def _check_error(json_string, key_or_keys):
        keys = [key_or_keys] if isinstance(key_or_keys, compat_str) else key_or_keys
        for key in keys:
            error = json_string.get(key)
            if error:
                raise ExtractorError('Unable to login: %s' % error, expected=True)

    def _login_step(self, form_html, fallback_action_url, extra_form_data, note, referrer_url):
        action_url = self._search_regex(
            r'<form[^>]+action=(["\'])(?P<url>.+?)\1', form_html,
            'post url', default=fallback_action_url, group='url')

        if not action_url.startswith('http'):
            action_url = compat_urlparse.urljoin(self._SIGNIN_URL, action_url)

        form_data = self._hidden_inputs(form_html)
        form_data.update(extra_form_data)

        try:
            response = self._download_json(
                action_url, None, note,
                data=urlencode_postdata(form_data),
                headers={
                    'Referer': referrer_url,
                    'X-Requested-With': 'XMLHttpRequest',
                })
        except ExtractorError as e:
            if isinstance(e.cause, compat_HTTPError) and e.cause.code == 500:
                response = self._parse_json(e.cause.read().decode('utf-8'), None)
                self._check_error(response, ('email', 'password'))
            raise

        self._check_error(response, 'ErrorMessage')

        return response, action_url

    def _login(self):
        username, password = self._get_login_info()
        if username is None:
            return

        # Step 1: download signin page
        signin_page = self._download_webpage(
            self._SIGNIN_URL, None, 'Downloading signin page')

        # Already logged in
        if any(re.search(p, signin_page) for p in (
                'isLoggedIn\s*:\s*true', r'logout\.aspx', r'>Log out<')):
            return

        # Step 2: submit email
        signin_form = self._search_regex(
            r'(?s)(<form[^>]+data-form-name=["\']signin["\'][^>]*>.+?</form>)',
            signin_page, 'signin form')
        signin_page, signin_url = self._login_step(
            signin_form, self._PASSWORD_URL, {'email': username},
            'Submitting email', self._SIGNIN_URL)

        # Step 3: submit password
        password_form = signin_page['body']
        self._login_step(
            password_form, self._USER_URL, {'email': username, 'password': password},
            'Submitting password', signin_url)


class LyndaIE(LyndaBaseIE):
    IE_NAME = 'lynda'
    IE_DESC = 'lynda.com videos'
    _VALID_URL = r'https?://www\.lynda\.com/(?:[^/]+/[^/]+/\d+|player/embed)/(?P<id>\d+)'

    _TIMECODE_REGEX = r'\[(?P<timecode>\d+:\d+:\d+[\.,]\d+)\]'

    _TESTS = [{
        'url': 'http://www.lynda.com/Bootstrap-tutorials/Using-exercise-files/110885/114408-4.html',
        # md5 is unstable
        'info_dict': {
            'id': '114408',
            'ext': 'mp4',
            'title': 'Using the exercise files',
            'duration': 68
        }
    }, {
        'url': 'https://www.lynda.com/player/embed/133770?tr=foo=1;bar=g;fizz=rt&fs=0',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        video = self._download_json(
            'http://www.lynda.com/ajax/player?videoId=%s&type=video' % video_id,
            video_id, 'Downloading video JSON')

        if 'Status' in video:
            raise ExtractorError(
                'lynda returned error: %s' % video['Message'], expected=True)

        if video.get('HasAccess') is False:
            self.raise_login_required('Video %s is only available for members' % video_id)

        video_id = compat_str(video.get('ID') or video_id)
        duration = int_or_none(video.get('DurationInSeconds'))
        title = video['Title']

        formats = []

        fmts = video.get('Formats')
        if fmts:
            formats.extend([{
                'url': f['Url'],
                'ext': f.get('Extension'),
                'width': int_or_none(f.get('Width')),
                'height': int_or_none(f.get('Height')),
                'filesize': int_or_none(f.get('FileSize')),
                'format_id': compat_str(f.get('Resolution')) if f.get('Resolution') else None,
            } for f in fmts if f.get('Url')])

        prioritized_streams = video.get('PrioritizedStreams')
        if prioritized_streams:
            for prioritized_stream_id, prioritized_stream in prioritized_streams.items():
                formats.extend([{
                    'url': video_url,
                    'width': int_or_none(format_id),
                    'format_id': '%s-%s' % (prioritized_stream_id, format_id),
                } for format_id, video_url in prioritized_stream.items()])

        self._check_formats(formats, video_id)
        self._sort_formats(formats)

        subtitles = self.extract_subtitles(video_id)

        return {
            'id': video_id,
            'title': title,
            'duration': duration,
            'subtitles': subtitles,
            'formats': formats
        }

    def _fix_subtitles(self, subs):
        srt = ''
        seq_counter = 0
        for pos in range(0, len(subs) - 1):
            seq_current = subs[pos]
            m_current = re.match(self._TIMECODE_REGEX, seq_current['Timecode'])
            if m_current is None:
                continue
            seq_next = subs[pos + 1]
            m_next = re.match(self._TIMECODE_REGEX, seq_next['Timecode'])
            if m_next is None:
                continue
            appear_time = m_current.group('timecode')
            disappear_time = m_next.group('timecode')
            text = seq_current['Caption'].strip()
            if text:
                seq_counter += 1
                srt += '%s\r\n%s --> %s\r\n%s\r\n\r\n' % (seq_counter, appear_time, disappear_time, text)
        if srt:
            return srt

    def _get_subtitles(self, video_id):
        url = 'http://www.lynda.com/ajax/player?videoId=%s&type=transcript' % video_id
        subs = self._download_json(url, None, False)
        if subs:
            return {'en': [{'ext': 'srt', 'data': self._fix_subtitles(subs)}]}
        else:
            return {}


class LyndaCourseIE(LyndaBaseIE):
    IE_NAME = 'lynda:course'
    IE_DESC = 'lynda.com online courses'

    # Course link equals to welcome/introduction video link of same course
    # We will recognize it as course link
    _VALID_URL = r'https?://(?:www|m)\.lynda\.com/(?P<coursepath>[^/]+/[^/]+/(?P<courseid>\d+))-\d\.html'

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        course_path = mobj.group('coursepath')
        course_id = mobj.group('courseid')

        course = self._download_json(
            'http://www.lynda.com/ajax/player?courseId=%s&type=course' % course_id,
            course_id, 'Downloading course JSON')

        if course.get('Status') == 'NotFound':
            raise ExtractorError(
                'Course %s does not exist' % course_id, expected=True)

        unaccessible_videos = 0
        entries = []

        # Might want to extract videos right here from video['Formats'] as it seems 'Formats' is not provided
        # by single video API anymore

        for chapter in course['Chapters']:
            for video in chapter.get('Videos', []):
                if video.get('HasAccess') is False:
                    unaccessible_videos += 1
                    continue
                video_id = video.get('ID')
                if video_id:
                    entries.append({
                        '_type': 'url_transparent',
                        'url': 'http://www.lynda.com/%s/%s-4.html' % (course_path, video_id),
                        'ie_key': LyndaIE.ie_key(),
                        'chapter': chapter.get('Title'),
                        'chapter_number': int_or_none(chapter.get('ChapterIndex')),
                        'chapter_id': compat_str(chapter.get('ID')),
                    })

        if unaccessible_videos > 0:
            self._downloader.report_warning(
                '%s videos are only available for members (or paid members) and will not be downloaded. '
                % unaccessible_videos + self._ACCOUNT_CREDENTIALS_HINT)

        course_title = course.get('Title')
        course_description = course.get('Description')

        return self.playlist_result(entries, course_id, course_title, course_description)

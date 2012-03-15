from django.template import Template, Context
from django.conf import settings


def parse(kwargs):
    id = kwargs.get('v')
    width = int(kwargs.get('w',
                           getattr(settings, 'SHORTCODES_YOUTUBE_WIDTH', 480)))
    height = int(kwargs.get('h',
                          getattr(settings, 'SHORTCODES_YOUTUBE_HEIGHT', 385)))
    jquery = getattr(settings, 'SHORTCODES_YOUTUBE_JQUERY', False)

    if jquery:
        html = '<a id="yt_{{ id }}"'
        html += ' href="http://www.youtube.com/watch?v={{ id }}">'
        html += '<span>Watch the YouTube video</span></a>\n'
        html += '<script type="text/javascript">\n'
        html += '\t$("#yt_{{ id }}").flash(\n'
        html += '\t\t{\n'
        html += '\t\t\tsrc: "http://www.youtube.com/v/{{ id }}",\n'
        html += '\t\t\twidth: {{ width }},\n'
        html += '\t\t\theight: {{ height }}\n'
        html += '\t\t}\n'
        html += '\t);\n'
        html += '\t$("#yt_{{ id }} span").hide()\n'
        html += '</script>\n'
    else:
        html = '<object width="{{ width }}" height="{{ height }}">'
        html += '<param name="movie" value="http://www.youtube.com/v/{{ id }}'
        html += '&hl=en&fs=1"></param>'
        html += '<param name="allowFullScreen" value="true"></param>'
        html += '<param name="allowscriptaccess" value="always"></param>'
        html += '<embed src="http://www.youtube.com/v/{{ id }}&hl=en&fs=1" '
        html += 'type="application/x-shockwave-flash" '
        html += 'allowscriptaccess="always" allowfullscreen="true" '
        html += 'width="{{ width }}" height="{{ height }}"></embed>'
        html += '</object>'

    template = Template(html)
    context = Context({
            'id': id,
            'width': width,
            'height': height})

    if id:
        return template.render(context)
    else:
        return 'Video not found'

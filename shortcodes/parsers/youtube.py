from django.template import Template, Context
from django.conf import settings

def parse(kwargs):
	id = kwargs.get('id')
	width = int(kwargs.get('width', getattr(settings, 'SHORTCODES_YOUTUBE_WIDTH', 425)))
	height = int(kwargs.get('height', 0))
	jquery = getattr(settings, 'SHORTCODES_YOUTUBE_JQUERY', False)
	
	if height == 0:
		height = int(round(width / 425.0 * 344.0))
	
	if jquery:
		html = '<a id="yt_{{ id }}" href="http://www.youtube.com/watch?v={{ id }}">'
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
		html += '<param name="movie" value="http://www.youtube.com/v/{{ id }}&hl=en&fs=1"></param>'
		html += '<param name="allowFullScreen" value="true"></param>'
		html += '<param name="allowscriptaccess" value="always"></param>'
		html += '<embed src="http://www.youtube.com/v/{{ id }}&hl=en&fs=1" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="{{ width }}" height="{{ height }}"></embed>'
		html += '</object>'
	
	template = Template(html)
	context = Context(
		{
			'id': id,
			'width': width,
			'height': height
		}
	)
	
	if id:
		return template.render(context)
	else:
		return 'Video not found'
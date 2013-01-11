from django.template import Template, Context
from django.template.loader import render_to_string
from django.conf import settings


def parse(kwargs, template_name="shortcodes/vimeo.html"):
    video_id = kwargs.get('id')
    if video_id:
        width = int(kwargs.get(
            'width',
            getattr(settings, 'SHORTCODES_VIMEO_WIDTH', 480))
        )
        height = int(kwargs.get(
            'height',
            getattr(settings, 'SHORTCODES_VIMEO_HEIGHT', 385))
        )

        ctx = {
            'video_id': video_id,
            'width': width,
            'height': height
        }
        return render_to_string(template_name, ctx)

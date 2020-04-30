from sekizai.templatetags.sekizai_tags import (
    validate_context, Tag, Options, Argument, SekizaiParser, get_varname,
    import_processor, template)

register = template.Library()


class CustomRenderBlock(Tag):
    """To enable multiple sekizai render even if name is not JS/CSS
    """
    name = 'render_block'

    options = Options(
        Argument('name'),
        Argument('js_or_css', required=False, default=None, resolve=False),
        'postprocessor',
        Argument('postprocessor', required=False, default=None, resolve=False),
        parser_class=SekizaiParser,
    )

    def render_tag(self, context, name, js_or_css, postprocessor, nodelist):
        if not validate_context(context):
            return nodelist.render(context)
        rendered_contents = nodelist.render(context)
        varname = get_varname()
        data = '\n'.join(context[varname][name])
        if postprocessor:
            func = import_processor(postprocessor)
            if js_or_css:
                data = func(context, data, js_or_css)  # the custom
            else:
                data = func(context, data, name)
        return '%s\n%s' % (data, rendered_contents)


register.tag('custom_render_block', CustomRenderBlock)

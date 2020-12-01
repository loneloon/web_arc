from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def page_render(template_file, folder='templates', **kwargs):

    try:
        env = Environment()
        env.loader = FileSystemLoader(folder)

        template = env.get_template(template_file)
    # try:
    #     with open(template_file, encoding='utf-8') as t:
    #         template = Template(t.read())

        return template.render(**kwargs).encode('utf-8')
    except Exception as e:
        return b'Failed to render page: ' + str(e).encode('utf-8')
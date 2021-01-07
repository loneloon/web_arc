from core.utils import *
from core.render import page_render as render
from logger.logger_module import Log
import copy


class PrototypeMixin:

    def clone(self):
        return copy.deepcopy(self)


class ModelMixin:

    def get_attrs(self):
        return dict((key, self.__getattribute__(key)) for key in self.__slots__ if self.__getattribute__(key) is not None)

    @classmethod
    def init_and_get_attrs(cls, *args, **kwargs):
        return cls(*args, **kwargs).get_attrs()


class BaseView:
    __slots__ = 'title', 'content', 'template'

    @classmethod
    @Log()
    def view(cls, request, db=None, site=None):
        if request['method'] == 'GET':
            return cls().get(request, db, site)
        else:
            return cls().post(request, db, site)

    def response(self, request, appendix=None):
        object_list = {'title': self.title,
                       'content': self.content,
                       'path': request['path'],
                       'user': request['user']}

        if appendix is not None:
            object_list.update(appendix)

        if request['next']:
            if request['path'] == signin_link:
                object_list['next'] = request.pop('next')
            elif request['next'] == signin_link:
                return redirect_302(f"{request.pop('next')}?next={request['path']}")
            else:
                return redirect_302(f"{request.pop('next')}")

        res = render(self.template, object_list=object_list)
        return '200 OK', [res]

    def get(self, request, db, site):
        return self.response(request)

    def post(self, request, db, site):
        return self.response(request)

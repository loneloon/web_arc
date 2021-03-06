from views import *

url_paths = {
    '/': Index().view,
    '/comments/': Comments().view,
    '/online-courses/': Categories().view,
    '/create-category/': CategoryCreate().view,
    '/create-course/': CourseCreate().view,
    "\/online-courses\/([a-zA-Z0-9])*\/": CategoryView().view,
    "\/online-courses\/([a-zA-Z0-9])*\/([a-zA-Z0-9])*\/": Course().view,
    "/signup/": SignUp().view,
    "/signin/": SignIn().view,
    "/signout/": SignOut().view,
    "/admin/": AdminView().view,
    "\/admin\/([a-zA-Z0-9])*\/": AdminView().view,
    "\/admin\/([a-zA-Z0-9])*\/([a-z])*\/": AdminView().view,
    "/user/": UserView().view,
    "/user/edit/": UserView().view,
    "/user/edit/pass/": UserView().view
}

from views import *

url_paths = {
    '/': Index().view,
    '/comments/': Comments().view,
    '/online-courses/': Categories().view,
    "\/online-courses\/([a-zA-Z0-9])*\/": CategoryView().view,
    "\/online-courses\/([a-zA-Z0-9])*\/([a-zA-Z0-9])*\/": Course().view,
    "/register/": Register().view
}

from views import *

url_paths = {
    '/': Index().view,
    '/comments/': Comments().view,
    '/online-courses/': Categories().view,
    "\/online-courses\/([a-zA-Z])*\/": category_view,
    "\/online-courses\/([a-zA-Z])*\/([a-zA-Z])*\/": course_view
}

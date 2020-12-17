from views import *

url_paths = {
    '/': index,
    '/comments/': comments,
    '/online-courses/': courses,
    "\/online-courses\/([a-zA-Z])*\/": category_view,
    "\/online-courses\/([a-zA-Z])*\/([a-zA-Z])*\/": course_view
}

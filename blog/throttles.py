from rest_framework.throttling import UserRateThrottle

class BlogPostThrottle(UserRateThrottle):
    scope = 'blog_post'

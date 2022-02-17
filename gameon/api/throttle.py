from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
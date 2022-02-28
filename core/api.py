from rest_framework import routers
from rentall import api_views as rental_views
from rest_framework_extensions.routers import NestedRouterMixin
# from rentall import views as myapp_views

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
friends = router.register(r"friends", rental_views.FriendViewset)
friends.register(
    r"borrowings",
    rental_views.BorrowedViewset,
    basename="friend-borrow",
    parents_query_lookups=["to_who"],
)
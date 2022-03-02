from dynamic_rest.routers import DynamicRouter
from rest_framework_extensions.routers import NestedRouterMixin
from rentall import api_views as myapp_views
router = DynamicRouter()
friends = router.register(r'friends', myapp_views.FriendViewset)
router.register(r'belongings', myapp_views.BelongingViewset)
router.register(r'borrowings', myapp_views.BorrowedViewset)

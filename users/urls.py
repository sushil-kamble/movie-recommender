from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostListViewUser,
                    PostUpdateView, PostDeleteView)

urlpatterns = [
    # Reviews Create
    path('review/', views.formFill, name="review"),
    # Reviews CRUD CLASS BASED VIEWS
    path('reviews/', PostListViewUser.as_view(), name="myReviews"),
    path('reviews/allreviews/', PostListView.as_view(), name="allReviews"),     # Private - Only Admin access
    path('reviews/<int:pk>/', PostDetailView.as_view(), name="review-detail"),
    path('reviews/<int:pk>/update/', PostUpdateView.as_view(), name="review-update"),
    path('reviews/<int:pk>/delete/', PostDeleteView.as_view(), name="review-delete")

    #
]

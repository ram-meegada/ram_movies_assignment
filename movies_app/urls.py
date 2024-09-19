from movies_app.views import onboardingView
from movies_app.views import moviesView

from django.urls import path

urlpatterns = [
    #onboarding
    path("registration/", onboardingView.UserRegistrationView.as_view()),

    #movies(collection)
    path("movies/", moviesView.MoviesListingView.as_view()),
    path("collection/", moviesView.ReadWriteCollectionView.as_view()),
    path("collection/<str:collection_uuid>/", moviesView.FetchUpdateDeleteCollectionView.as_view())
]

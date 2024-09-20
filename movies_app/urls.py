from movies_app.views import onboardingView, moviesView, requestCounterView
from django.urls import path

urlpatterns = [
    # onboarding
    path("registration/", onboardingView.UserRegistrationView.as_view()),

    # movies(collection)
    path("movies/", moviesView.MoviesListingView.as_view()),
    path("collection/", moviesView.ReadWriteCollectionView.as_view()),
    path("collection/<str:collection_uuid>/", moviesView.FetchUpdateDeleteCollectionView.as_view()),

    # requests to server
    path("request-count/", requestCounterView.RequestsToServerView.as_view()),
    path("request-count/reset/", requestCounterView.ResetRequestsToServerView.as_view()),

]

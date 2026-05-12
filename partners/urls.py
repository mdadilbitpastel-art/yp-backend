"""Partners app API routes — mounted under /api/partners/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.PartnersPageView.as_view(), name="api-partners"),
    path("hero/", views.PartnersHeroSectionView.as_view(), name="api-partners-hero"),
    path("partner/", views.PartnersPartnerSectionView.as_view(), name="api-partners-partner"),
    path("family/", views.PartnersFamilySectionView.as_view(), name="api-partners-family"),
    path("review/", views.PartnersReviewSectionView.as_view(), name="api-partners-review"),
    path("founder/", views.PartnersFounderSectionView.as_view(), name="api-partners-founder"),
]

from django.conf.urls import patterns, url
from tenthoughts import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^home/', views.homepage, name='home'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^featured_articles/', views.featuredArticles, name='featured_articles'),
        url(r'^community_articles/(?P<community>[\w\-]+)/$', views.communityArticles, name = 'community_articles'),
        url(r'^submit_articles/', views.submitArticle, name='submit articles'),
        url(r'^communitylist/', views.communitylist, name ='communitylist'),
        url(r'^community/(?P<bschool>[\w\-]+)/$', views.community, name='community'),
        url(r'^your_community/', views.your_community, name='your_community'),
        url(r'^follow/(?P<client>[\w\-]+)/$', views.follow, name='follow'),
        url(r'^unfollow/(?P<client>[\w\-]+)/$', views.unfollow, name='unfollow'),
        url(r'^refer10thoughts/', views.refer, name='refer'),
    
    )

        

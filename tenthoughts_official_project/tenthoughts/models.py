from django.db import models
from django.contrib.auth.models import User



class UserProf(models.Model):
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    #Text versions of python lists for storing in the database
    followers = models.TextField(default='email')
    following = models.TextField(default='email')
    groups = models.CharField(max_length=128, default='bschool')


    def followers_list(self):
        followers_list = self.followers.split(',')
        return followers_list

    def following_list(self):
        following_list = self.following.split(',')
        return following_list

    def group_list(self):
        group_list = self.groups.split(',')
        return group_list
    
    def num_followers(self):
        followers_list = self.followers.split(',')
        return int(len(followers_list)-1)

    def num_following(self):
        following_list = self.following.split(',')
        return int(len(following_list)-1)

    def num_groups(self):
        group_list = self.groups.split(',')
        return len(group_list)
   
    def __str__(self):
        return self.user.username








class Article(models.Model):
    submitter = models.ForeignKey(UserProf)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    submission_date = models.DateTimeField()


    def __str__(self):
        return self.title






class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.TextField(null=True)

    def __str__(self):
        return self.name

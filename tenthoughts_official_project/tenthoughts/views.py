from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from tenthoughts.models import UserProf, Article, Group
from tenthoughts.forms import UserForm, UserProfileForm, ArticleForm, GroupSelectForm 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail



def index(request):
    context_dict={}
    return render(request,'tenthoughts/index.html', context_dict)




def about(request):
    context_dict={}
    return render(request,'tenthoughts/about.html', context_dict)




def register(request):
    registered = False
    group_form = GroupSelectForm()
    
    if request.method == 'POST':     
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        group_form = GroupSelectForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and group_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            #add group to profile and update group member list
            bschool = group_form.cleaned_data['bschool']
            profile.groups = bschool.name
            bschool.members = bschool.members + ',' + user.username
            profile.save()
            bschool.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'tenthoughts/register.html',
            {'user_form': user_form, 'profile_form': profile_form,
             'group_form': group_form, 'registered': registered})




def user_login(request):

    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['password']

        find_user = User.objects.get(email=email)

        user = authenticate(username=find_user.username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/10thoughts/home')
            else:
                return HttpResponse("Your 10thoughts account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(email, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'tenthoughts/login.html', {})



    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/10thoughts/')





@login_required
def homepage(request):
    
    context_dict={}
    client = UserProf.objects.get(user=request.user)
    
    if request.user.is_authenticated():
        context_dict['email'] = client.user.email
        context_dict['num_followers'] = client.num_followers()
        context_dict['num_following'] = client.num_following()
        return render(request, 'tenthoughts/home.html', context_dict)
    
    else:
        return render(request, 'tenthoughts/index.html', context_dict)




def featuredArticles(request):
    context_dict={}
    return render(request, 'tenthoughts/featured_articles.html', context_dict)





@login_required
def submitArticle(request):
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        article = form.save(commit=False)

        if form.is_valid():
            article.submitter = UserProf.objects.get(user=request.user)
            article.views = 0
            article.submission_date = datetime.now()
            article.save()
            return HttpResponseRedirect('/10thoughts/home')
            
        else:
            print(form.errors)

    else:
        form = ArticleForm()

    return render(request, 'tenthoughts/submit_articles.html', {'form':form})




def communityArticles(request, community):
    context_dict = {}
    context_dict['community_name'] = community
    return render(request, 'tenthoughts/community_articles.html', context_dict)







@login_required
def communitylist(request):
    context_dict = {}
    return render(request, 'tenthoughts/communitylist.html', context_dict)
    



@login_required
def community(request, bschool):
    context_dict={}
   
    try:
        bschool = Group.objects.get(name=bschool)
        context_dict['bschool_name'] = bschool.name
        members = UserProf.objects.filter(groups=bschool.name)
        context_dict['members'] = members
        context_dict['bschool'] = bschool

    except Group.DoesNotExist:
        pass

    return render(request, 'tenthoughts/community.html', context_dict)




@login_required
def your_community(request):
    context_dict={}

    Profile = UserProf.objects.get(user=request.user)
    follower_list = UserProf.objects.filter(following__contains=Profile.user.username)
    following_list = UserProf.objects.filter(followers__contains=Profile.user.username)

    
    context_dict['follower_list'] = follower_list
    context_dict['following_list'] = following_list

    return render(request, 'tenthoughts/your_community.html', context_dict)
    



@login_required
def follow(request, client):

    user_profile = UserProf.objects.get(user=request.user)
    follow_user = User.objects.get(username=client)
    follow_userprof = UserProf.objects.get(user=follow_user)

    following_list = user_profile.following.split(',')

    if client in following_list:
        return HttpResponseRedirect('/10thoughts/home')
        
    else:
        user_profile.following = user_profile.following + ',' + client
        user_profile.save()
        follow_userprof.followers = follow_userprof.followers + ',' + user_profile.user.username
        follow_userprof.save()

        return HttpResponseRedirect('/10thoughts/home')




@login_required
def unfollow(request, client):
    
    user_profile = UserProf.objects.get(user=request.user)
    following_user = User.objects.get(username=client)
    following_userprof = UserProf.objects.get(user=following_user)

    following_list = user_profile.following.split(',')

    if client in following_list:
        following_list.remove(client)
        following_list_new=",".join(following_list)
        user_profile.following = following_list_new
        user_profile.save()

        follower_list = following_userprof.followers.split(',')
        follower_list.remove(user_profile.user.username)
        follower_list_new=",".join(follower_list)
        following_userprof.followers = follower_list_new
        following_userprof.save()

        return HttpResponseRedirect('/10thoughts/home')

    else:
        return HttpResponseRedirect('/10thoughts/home')



@login_required
def refer(request):
    return render(request, 'tenthoughts/refer.html', {})
    



from django.shortcuts import render, redirect
from .models import Group, Membership
from django.contrib.auth.decorators import login_required
from .forms import GroupForm, JoinGroupForm, LeaveGroupForm


@login_required
def create_group(request):
    if request.method == 'POST':
       form = GroupForm(request.POST)
       if form.is_valid():
           group = form.save(commit=False)
           group.creator = request.user
           group.save()
           return redirect('group_list')
    else:
       form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def details_group(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'groups/group_detail.html', {'group':group})
        
@login_required
def user_groups(request):
    # Fetch all memberships for the current user
    memberships = Membership.objects.filter(user=request.user)

    # Fetch all groups that the current user is a member of
    groups = Group.objects.filter(memberships_user=request.user)

    return render(request, 'groups/user_groups.html', {'groups': groups})

@login_required
def join_group(request, group_id):
    if request.method == 'POST':
       form = JoinGroupForm(request.POST)
       if form.is_valid():
           group_id = form.cleaned_data['group_id']
           group = Group.objects.get(id=group_id)
           Membership.objects.create(user=request.user, group=group)
           return redirect('details', group_id=group_id)
    else:
       form = JoinGroupForm()
       
    return render(request, 'groups/join_group.html', {'form': form})
    
@login_required
def leave_group(request, group_id):
    if request.method == 'POST':
      form = LeaveGroupForm(request.POST)
      if form.is_valid():
          group_id = form.cleaned_data['group_id']
          membership = Membership.objects.get(user=request.user, group_id=group_id)
          membership.delete()
          return redirect('group_detail', group_id=group_id)
    else:
      form = LeaveGroupForm()

    return render(request, 'groups/leave_group.html', {'form': form})
    
@login_required
def user_groups_list(request):
   # Fetch all groups that the current user is a member of
   groups = Group.objects.filter(members=request.user)

   return render(request, 'groups/user_groups_list.html', {'groups': groups})

@login_required
def groups(request):
   # Fetch all groups
   groups = Group.objects.all()

   # Fetch all memberships
   memberships = Membership.objects.all()

   # Join groups and memberships based on a common field (e.g., group_id)
   joined_data = []
   for membership in memberships:
       for group in groups:
           if group.id == membership.group_id:
               joined_data.append({
                 'group_name': group.name,
                 'member_name': membership.user.username,
                 'date_joined': membership.date_joined,
               })

   return render(request, 'groups/group_list.html', {'groups':groups})
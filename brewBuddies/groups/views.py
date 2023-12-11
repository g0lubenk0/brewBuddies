from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm

@login_required
def group_list(request):
    groups = Group.objects.all()
    print(groups)
    return render(request, 'groups/group_list.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_detail.html', {'group': group})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
    return redirect('user_group_list')

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id, creator=request.user)
    group.delete()
    return redirect('group_list')

@login_required
def update_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, creator=request.user)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/update_group.html', {'form': form, 'group': group})

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    request.user.joined_groups.remove(group)
    return redirect('user_group_list')

@login_required
def user_group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/user_group_list.html', {'groups': groups})

@login_required
def group_chat(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_chat.html', {'group': group})

@login_required
def map(request):
    groups = Group.objects.all()
    return render(request, 'groups/map.html', {'groups': groups})

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id, creator=request.user)
    group.delete()
    return redirect('group_list')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm

@login_required
def group_list(request):
    """
    Render a list of all groups.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Rendered HTML response displaying a list of all groups.
    """
    groups = Group.objects.all()
    print(groups)
    return render(request, 'groups/group_list.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    """
    Render details of a specific group.

    Args:
        request: HttpRequest object.
        group_id: Integer, the unique identifier of the group.

    Returns:
        HttpResponse: Rendered HTML response displaying details of the specified group.
    """
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_detail.html', {'group': group})

@login_required
def create_group(request):
    """
    Create a new group.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Rendered HTML response displaying the group creation form.
    """
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
    """
    Join an existing group.

    Args:
        request: HttpRequest object.
        group_id: Integer, the unique identifier of the group.

    Returns:
        HttpResponse: Redirects to the user's group list.
    """
    group = get_object_or_404(Group, pk=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
    return redirect('user_group_list')

@login_required
def delete_group(request, group_id):
    """
    Delete a group if the authenticated user is the creator.

    Args:
        request: HttpRequest object.
        group_id: Integer, the unique identifier of the group.

    Returns:
        HttpResponse: Redirects to the group list.
    """
    group = get_object_or_404(Group, pk=group_id, creator=request.user)
    group.delete()
    return redirect('group_list')

@login_required
def update_group(request, group_id):
    """
    Update group information if the authenticated user is the creator.

    Args:
        request: HttpRequest object.
        group_id: Integer, the unique identifier of the group.

    Returns:
        HttpResponse: Rendered HTML response displaying the group update form.
    """
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
    """
    Leave a group.

    Args:
        request: HttpRequest object.
        group_id: Integer, the unique identifier of the group.

    Returns:
        HttpResponse: Redirects to the user's group list.
    """
    group = get_object_or_404(Group, id=group_id)
    request.user.joined_groups.remove(group)
    return redirect('user_group_list')

@login_required
def user_group_list(request):
    """
    Render a list of groups that the authenticated user has joined.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Rendered HTML response displaying a list of joined groups.
    """
    groups = Group.objects.all()
    return render(request, 'groups/user_group_list.html', {'groups': groups})

@login_required
def group_chat(request, group_id):
    """
    Render the group chat view.

    Args:
        request: HttpRequest object.
        group_id: Integer, the unique identifier of the group.

    Returns:
        HttpResponse: Rendered HTML response displaying the group chat.
    """
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_chat.html', {'group': group})

@login_required
def map(request):
    """
    Render the map view with all groups displayed.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Rendered HTML response displaying the map with groups.
    """
    groups = Group.objects.all()
    return render(request, 'groups/map.html', {'groups': groups})

@login_required
def delete_group(request, group_id):
    """
    Deletes a group if the logged-in user is the creator of the group.

    Args:
        request (HttpRequest): The request object.
        group_id (int): The ID of the group to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the group list page after successful deletion.

    Raises:
        Http404: If the requested group is not found.
        PermissionDenied: If the logged-in user is not the creator of the group.
    """
    group = get_object_or_404(Group, pk=group_id, creator=request.user)
    group.delete()
    return redirect('group_list')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView


def user_dashboard(request):
    """
    This will show the user dashboard.
    :param request: Django's HTTP Request object
    :return: Render dashboard or redirect to login form
    """
    # If user is logged in only then show dashboard else redirect to login form
    if not request.user.is_anonymous:
        return render(request, "User/dashboard.html")
    return redirect('loginform')


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    """
       Update the user's first name, last name and Email
       :param LoginRequiredMixin, UpdateView: Mixin that will check if user is logged in, Django's Generic View
       :return: Render dashboard or 404
       """
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'User/user_update_form.html'

    def get_object(self, queryset=None):
        """This will verify if the current user is updating his profile or not"""
        current_user = super(UpdateUserProfile, self).get_object(queryset)
        # If the logged in user id trying to change any other user's profile information, this will restrict them
        if current_user.username != self.request.user.username:
            raise Http404("Please respect other's privacy!")
        return current_user


class DeleteUserProfile(LoginRequiredMixin, DeleteView):
    """
        Deletes the user profile
        :param LoginRequiredMixin, DeleteView: Mixin that will check if user is logged in, Django's Generic View
        :return: Render login form if successfully delete the current session and redirect.
    """
    model = User
    success_url = reverse_lazy('loginform')
    template_name = 'User/user_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        """Deletes the session"""
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        del request.session['username']
        request.session.modified = True
        return HttpResponseRedirect(success_url)

    def get_object(self, queryset=None):
        """This will verify if the current user is deleting his profile or not"""
        current_user = super(DeleteUserProfile, self).get_object(queryset)
        # If the logged in user id trying to delete any other user's profile information, this will restrict them
        if current_user.username != self.request.user.username:
            raise Http404("Please respect other's privacy!")
        return current_user

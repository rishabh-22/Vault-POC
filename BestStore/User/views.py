from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView


def user_dashboard(request):
    """This will show the user dashboard."""
    if not request.user.is_anonymous:
        return render(request, "User/dashboard.html")
    return redirect('loginform')


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    """Update the user's first name, last name and Email"""
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'User/user_update_form.html'

    def get_object(self, queryset=None):
        """This will verify if the current user is updating his profile or not"""
        current_user = super(UpdateUserProfile, self).get_object(queryset)
        if current_user.username != self.request.user.username:
            raise Http404("Company does not exist")
        return current_user


class DeleteUserProfile(LoginRequiredMixin, DeleteView):
    """Deletes the user profile """
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


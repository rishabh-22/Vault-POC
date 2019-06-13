from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from User.forms import ContactQueryForm, UserAddressForm
from .models import UserAddress


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


def contact_us(request):
    form = ContactQueryForm()
    if request.method == 'POST':
        form = ContactQueryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contact/')
        else:
            form = ContactQueryForm()
    return render(request, 'General/contact_us.html', {'form': form})


def privacy(request):
    return render(request, 'General/privacy.html')


def tnc(request):
    return render(request, 'General/tnc.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = User.objects.get(username__exact=request.user.username)

        if password1 == password2:
            if user.check_password(request.POST['old_password']):
                user.set_password(password1)
                user.save()
                return redirect('password_reset_complete')
            else:
                messages.error(request, "The old password you have entered is wrong")
                # import pdb; pdb.set_trace()
                return render(request, 'Auth/change_password.html')

        else:
            messages.error(request, "Passwords do not match")
            return render(request, 'Auth/change_password.html')

    else:
        return render(request, 'Auth/change_password.html')


def settings(request):
    return render(request, 'User/settings.html')


def add_address(request):
    form = UserAddressForm()
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            # import pdb; pdb.set_trace()
            form.instance.user = request.user
            form.save()
            messages.error(request, "Your address is saved successfully!")
            return HttpResponseRedirect('/dashboard/')
        else:
            # form.errors
            return render(request, 'User/add_address.html', {'form': form})

    return render(request, 'User/add_address.html', {'form': form})


def view_address(request):
    try:
        address = UserAddress.objects.filter(user=request.user)

    except:
        messages.error(request, "No saved addresses found for your account.")
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'User/user_address.html', {'address': address})


def delete_address(request, pk):

    if request.method == 'POST':
        add = UserAddress.objects.get(pk=pk)
        add.is_deleted = True
        add.save()
    return HttpResponseRedirect('/dashboard/')

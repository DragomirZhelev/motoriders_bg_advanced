from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from assistance.models import Rider, HelpRequest
from assistance.forms import HelpRequestCreateForm, HelpRequestEditForm, HelpRequestDeleteForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from common import choices


# Create your views here.
class HelpRequestListView(ListView):
    model = HelpRequest
    template_name = 'assistance/help-request-list.html'
    context_object_name = 'help_requests'

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get('status')

        if status:
            queryset = queryset.filter(status = status)

        return queryset

class HelpRequestDetailView(DetailView):
    model = HelpRequest
    template_name = 'assistance/help-request-details.html'
    context_object_name = 'help_request'


class HelpRequestCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'assistance.add_helprequest'

    model = HelpRequest
    form_class = HelpRequestCreateForm
    template_name = 'assistance/help-request-create.html'
    success_url = reverse_lazy('assistance:help-request-list')

    def form_valid(self, form):
        rider = Rider.objects.filter(user = self.request.user).first()

        if rider is None:
            form.add_error(None, 'Existing Rider Profile required before road assistance request could be submitted')
            return self.form_invalid(form)

        form.instance.rider = rider

        return super().form_valid(form)


class HelpRequestEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'assistance.change_helprequest'

    model = HelpRequest
    form_class = HelpRequestEditForm
    template_name = 'assistance/help-request-edit.html'
    context_object_name = 'help_request'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(status = choices.HelpRequestStatusChoices.OPEN)

        queryset = queryset.filter(rider__user = self.request.user)

        return queryset

    def get_success_url(self):
        return reverse_lazy('assistance:help-request-details', kwargs={'pk': self.object.pk})


class HelpRequestDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'assistance.delete_helprequest'

    model = HelpRequest
    template_name = 'assistance/help-request-delete.html'
    context_object_name = 'help_request'
    success_url = reverse_lazy('assistance:help-request-list')

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(rider__user = self.request.user)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = HelpRequestDeleteForm(instance=self.object)

        return context



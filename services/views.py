from django.db.models import Q, Avg
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from services.forms import GarageCreateForm, GarageEditForm, GarageDeleteForm, GarageReviewCreateForm, GarageReviewEditForm, GarageReviewDeleteForm
from services.models import Garage, GarageReview
from riders.models import Rider
# Create your views here.

class GarageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'services.add_garage'

    model = Garage
    form_class = GarageCreateForm
    template_name = 'services/garage-create.html'
    success_url = reverse_lazy('services:garage_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GarageListView(ListView):
    model = Garage
    template_name = 'services/garage-list.html'
    context_object_name = 'garages'

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(city__icontains=search) |
                Q(services__name__icontains=search)
            ).distinct()

        return queryset


class GarageDetailView(DetailView):
    model = Garage
    template_name = 'services/garage-details.html'
    context_object_name = 'garage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        garage = self.object
        garage_reviews = garage.reviews.all()

        rating = garage_reviews.aggregate(average_rating = Avg('rating'))

        average_rating = rating['average_rating']

        context['average_rating'] = average_rating

        return context



class GarageEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'services.change_garage'

    model = Garage
    form_class = GarageEditForm
    template_name = 'services/garage-edit.html'
    context_object_name = 'garage'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            owner=self.request.user
        )

        return queryset

    def get_success_url(self):
        return reverse_lazy('services:garage_details', kwargs={'pk': self.object.pk})

class GarageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'services.delete_garage'

    model = Garage
    template_name = 'services/garage-delete.html'
    context_object_name = 'garage'
    success_url = reverse_lazy('services:garage_list')

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            owner = self.request.user
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = GarageDeleteForm(instance = self.object)

        return context



class GarageReviewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'services.add_garagereview'

    model = GarageReview
    form_class = GarageReviewCreateForm
    template_name = 'services/garage-review-create.html'
    success_url = reverse_lazy('services:garage_review_list')

    def form_valid(self, form):
        garage = form.cleaned_data.get('garage')

        if garage.owner == self.request.user:
            form.add_error(None, 'The owner of the garage can not provide review for it')
            return self.form_invalid(form)

        review = GarageReview.objects.filter(garage = garage, reviewer = self.request.user,)

        if review.exists():
            form.add_error(None, 'Can not provide another review for the same garage')
            return self.form_invalid(form)

        form.instance.reviewer = self.request.user

        return super().form_valid(form)

class GarageReviewListView(ListView):
    model = GarageReview
    template_name = 'services/garage-review-list.html'
    context_object_name = 'garage_reviews'

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(garage__name__icontains=search) |
                Q(reviewer__first_name__icontains=search) |
                Q(reviewer__last_name__icontains=search) |
                Q(reviewer__username__icontains=search)
            )

        return queryset

class GarageReviewDetailView(DetailView):
    model = GarageReview
    template_name = 'services/garage-review-details.html'
    context_object_name = 'garage_review'




class GarageReviewEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'services.change_garagereview'

    model = GarageReview
    form_class = GarageReviewEditForm
    template_name = 'services/garage-review-edit.html'
    context_object_name = 'garage_review'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            reviewer = self.request.user
        )

        return queryset


    def get_success_url(self):
        return reverse_lazy('services:garage_review_details', kwargs={'pk': self.object.pk})


class GarageReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'services.delete_garagereview'

    model = GarageReview
    template_name = 'services/garage-review-delete.html'
    context_object_name = 'garage_review'
    success_url = reverse_lazy('services:garage_review_list')

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            reviewer = self.request.user
        )

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = GarageReviewDeleteForm(instance = self.object)

        return context


















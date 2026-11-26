from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from common import choices
from riders.models import Rider
from rides.models import Ride, RideReview
from rides.forms import RideCreateForm, RideEditForm, RideDeleteForm, RideReviewCreateForm, RideReviewEditForm, RideReviewDeleteForm, JoinRideForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.


class RideListView(ListView):
    model = Ride
    template_name = 'rides/ride-list.html'
    context_object_name = 'rides'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search')
        status = self.request.GET.get('status')
        sort = self.request.GET.get('sort')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(ride_organizer__user__first_name__icontains=search_query) |
                Q(ride_organizer__user__last_name__icontains=search_query) |
                Q(ride_organizer__nickname__icontains=search_query) |
                Q(participants__user__first_name__icontains=search_query) |
                Q(participants__user__last_name__icontains=search_query) |
                Q(participants__nickname__icontains=search_query) |
                Q(meeting_point__icontains=search_query) |
                Q(destination__icontains=search_query) |
                Q(road_types__icontains=search_query) |
                Q(road_difficulty__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()
        if status:
            queryset = queryset.filter(status=status)

        if sort == 'latest':
            queryset = queryset.order_by('-created_at')

        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')

        return queryset

class RideDetailView(DetailView):
    model = Ride
    template_name = 'rides/ride-details.html'
    context_object_name = 'ride'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_rider = None
        is_organizer = False
        is_participant = False

        if self.request.user.is_authenticated:
            current_rider = Rider.objects.filter(user = self.request.user).first()

            if current_rider is not None:
                ride = self.object
                ride_organizer = ride.ride_organizer
                participants = ride.participants.all()

                if ride_organizer == current_rider:
                    is_organizer = True

                if current_rider in participants:
                    is_participant = True

        context['current_rider'] = current_rider
        context['is_organizer'] = is_organizer
        context['is_participant'] = is_participant

        return context






class RideCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'rides.add_ride'

    model = Ride
    form_class = RideCreateForm
    template_name = 'rides/ride-create.html'
    success_url = reverse_lazy('rides:ride-list')

    def form_valid(self, form):
        rider = Rider.objects.filter(user = self.request.user).first()

        if rider is None:
            form.add_error(None, 'Rider Profile registration is required to be able to organize a ride')
            return self.form_invalid(form)

        form.instance.ride_organizer = rider

        return super().form_valid(form)





class RideEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'rides.change_ride'

    model = Ride
    form_class = RideEditForm
    template_name = 'rides/ride-edit.html'
    context_object_name = 'ride'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(status = choices.TripStatusChoices.PLANNED)

        queryset = queryset.filter(ride_organizer__user = self.request.user)

        return queryset

    def get_success_url(self):
        return reverse_lazy('rides:ride-details', kwargs={'pk': self.object.pk})



class RideDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'rides.delete_ride'

    model = Ride
    template_name = 'rides/ride-delete.html'
    success_url = reverse_lazy('rides:ride-list')
    context_object_name = 'ride'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(ride_organizer__user = self.request.user)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RideDeleteForm(instance=self.object)

        return context



class RideReviewDetailView(DetailView):
    model = RideReview
    template_name = 'rides/ride-review-details.html'
    context_object_name = 'ride_review'



class RideReviewListView(ListView):
    model = RideReview
    template_name = 'rides/ride-review-list.html'
    context_object_name = 'ride_reviews'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(ride__title__icontains=search_query) |
                Q(reviewer__user__first_name__icontains=search_query) |
                Q(reviewer__user__last_name__icontains=search_query) |
                Q(reviewer__nickname__icontains=search_query)
            )

        return queryset



class RideReviewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'rides.add_ridereview'

    model = RideReview
    form_class = RideReviewCreateForm
    template_name = 'rides/ride-review-create.html'
    success_url = reverse_lazy('rides:ride-review-list')

    def form_valid(self, form):
        rider = Rider.objects.filter(user = self.request.user).first()

        if rider is None:
            form.add_error(None, 'Rider Profile registration is required to be able to submit a review')

            return self.form_invalid(form)

        ride = form.cleaned_data.get('ride')
        organizer = ride.ride_organizer
        participants = ride.participants.all()

        if rider != organizer and rider not in participants:
            form.add_error(None, 'Reviews can be submitted only by ride organizer or participants')
            return self.form_invalid(form)

        existing_review = RideReview.objects.filter(ride = ride, reviewer = rider).exists()
        if existing_review:
            form.add_error(None, 'Review for this ride submitted by you already exists')
            return self.form_invalid(form)

        form.instance.reviewer = rider
        return super().form_valid(form)



class RideReviewEditView(LoginRequiredMixin,  PermissionRequiredMixin, UpdateView):
    permission_required = 'rides.change_ridereview'

    model = RideReview
    form_class = RideReviewEditForm
    template_name = 'rides/ride-review-edit.html'
    context_object_name = 'ride_review'


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(reviewer__user = self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('rides:ride-review-details', kwargs={'pk': self.object.pk})


class RideReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'rides.delete_ridereview'

    model = RideReview
    template_name = 'rides/ride-review-delete.html'
    context_object_name = 'ride_review'
    success_url = reverse_lazy('rides:ride-review-list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(reviewer__user = self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = RideReviewDeleteForm(instance=self.object)

        return context

@login_required
@permission_required('rides.change_ride', raise_exception=True)
def join_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk)

    rider = Rider.objects.filter(user = request.user).first()

    if rider is None:
        return redirect('riders:rider-create')

    if request.method == 'POST':
        form = JoinRideForm(request.POST)
        if form.is_valid():
            # rider = form.cleaned_data['rider']
            if ride.status != 'Planned':
                form.add_error(None, 'You can join only Rides in status Planned')

            elif ride.participants.count() >= ride.maximum_riders_to_join:
                form.add_error(None, 'Number of maximum riders for this ride has been reached already')

            elif rider == ride.ride_organizer:
                # raise ValidationError('The organizer of the ride can not join the participants list')
                form.add_error(None, 'The organizer of the ride shall not join as participant')
            elif rider in ride.participants.all():
                form.add_error(None, 'This rider is already part of the participants list')
            else:
                ride.participants.add(rider)

                return redirect('rides:ride-details', pk=ride.pk)

    else:
        form = JoinRideForm()

    context = {'ride': ride, 'form': form,}

    return render(request, 'rides/ride-join.html', context)

@login_required
@permission_required('rides.change_ride', raise_exception=True)
@require_POST
def leave_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    # rider = get_object_or_404(Rider, pk=rider_pk)

    rider = Rider.objects.filter(user = request.user).first()

    if rider is None:
        return redirect('riders:rider-create')

    status_ride = ride.status

    if status_ride == choices.TripStatusChoices.PLANNED:
        if rider in ride.participants.all():
            ride.participants.remove(rider)

    return redirect('rides:ride-details', pk=pk)

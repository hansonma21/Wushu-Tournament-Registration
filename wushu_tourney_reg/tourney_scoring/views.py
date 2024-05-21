from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from tourney_reg.models import TournamentEvent, Tournament, Registration
from tourney_scoring.models import FinalScore, JudgeScore
from .forms import FinalScoreForm, JudgeScoreForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def judge_required(view_func):
    @login_required(login_url='tourney_profiles:login', redirect_field_name=None)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.profile.is_judge:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# # need to be logged in and have the correct permissions to view this page (they must be a judge or an admin)
# # if the user is not logged in, redirect them to the login page
# @login_required(login_url='tourney_profiles:login', redirect_field_name=None)
# @user_passes_test(is_judge_or_admin, login_url='tourney_pages:home', redirect_field_name=None)
@judge_required
def main_dashboard_view(request):
    tournaments = Tournament.objects.filter(is_active=True)
    return render(request, 'tourney_scoring/judging_dashboard.html', {'tournaments': tournaments})

@judge_required
def tournament_dashboard_view(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament_events = TournamentEvent.objects.filter(tournament=tournament, order__isnull=False).order_by('order')
    mat_or_locations = tournament_events.values_list('mat_or_location', flat=True).distinct()
    mat_or_locations_dict = {}
    for mat_or_location in mat_or_locations:
        mat_or_locations_dict[mat_or_location] = tournament_events.filter(mat_or_location=mat_or_location)

    return render(request, 'tourney_scoring/tournament_dashboard.html', {'tournament': tournament, 'mat_or_locations': mat_or_locations_dict})

@judge_required
def tournament_event_dashboard_view(request, tournament_id, tournament_event_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament_event = get_object_or_404(TournamentEvent, pk=tournament_event_id)
    competitors = Registration.objects.filter(tournament_event=tournament_event).exclude(Q(finalscore__isnull=True) | Q(order__isnull=True)).order_by('order')
    if tournament_event.tournament != tournament:
        # invalid link error
        raise PermissionDenied
    return render(request, 'tourney_scoring/tournament_event_dashboard.html', {'tournament_event': tournament_event, 'competitors': competitors})

@judge_required
def event_scoring_view(request, tournament_id, tournament_event_id, order):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament_event = get_object_or_404(TournamentEvent, pk=tournament_event_id)
    if tournament_event.tournament != tournament:
        # invalid link error
        raise PermissionDenied
    
    next_tournament_event = TournamentEvent.objects.filter(tournament=tournament, order__gt=tournament_event.order).order_by('order').first()
    previous_tournament_event = TournamentEvent.objects.filter(tournament=tournament, order__lt=tournament_event.order).order_by('-order').first()

    competitor = get_object_or_404(Registration, tournament_event=tournament_event, order=order)
    final_score_obj = competitor.finalscore
    if not final_score_obj:
        # a final score object has not been created for this competitor, possibly because the registration has not been approved yet
        raise PermissionDenied
    
    next_competitor = Registration.objects.filter(tournament_event=tournament_event, order__gt=order).order_by('order').first()
    previous_competitor = Registration.objects.filter(tournament_event=tournament_event, order__lt=order).order_by('-order').first()

    # check if current user is head judge
    is_head_judge = False
    if final_score_obj.head_judge == request.user.profile:
        is_head_judge = True
    
    # initalize final_form and judge_form to display on the page (may be overwritten later if POST request is made)
    final_form = FinalScoreForm(instance=final_score_obj) if is_head_judge else None    # can't fail since we checked final_score_obj is not None above
    # only head judge can see other judges' scores
    other_judges_scores = JudgeScore.objects.filter(final_score=final_score_obj).exclude(judge=request.user.profile).order_by if is_head_judge else None

    judge_score = JudgeScore.objects.filter(final_score=final_score_obj, judge=request.user.profile).first()
    judge_form = JudgeScoreForm(instance=judge_score) if judge_score else JudgeScoreForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # check if the form is a judge form or a final form
        if form_type == 'judge_form':
            if judge_score:
                # judge has already submitted a judge score, update it
                judge_form = JudgeScoreForm(request.POST, instance=judge_score)
            else:
                # judge has not submitted a judge score, create a new one
                judge_form = JudgeScoreForm(request.POST)
            
            # check for valid scoring and save the form
            if judge_form.is_valid():
                judge_score = judge_form.save(commit=False)
                judge_score.final_score = final_score_obj
                judge_score.judge = request.user.profile
                judge_score.save()
                messages.success(request, 'Judge score submitted successfully.')
                
        elif form_type == 'final_form':
            if not is_head_judge:
                # user is not the head judge for this event
                raise PermissionDenied
            
            # final form is only for the head judge, and is always already created so we just need to update it
            final_form = FinalScoreForm(request.POST, instance=final_score_obj)
            if final_form.is_valid():
                final_form.save()
                messages.success(request, 'Final score submitted successfully.')
        else:
            # invalid form type
            raise PermissionDenied
        
    context = {
        'tournament_event': tournament_event,
        'competitor': competitor,
        'final_form': final_form,
        'judge_form': judge_form,
        'is_head_judge': is_head_judge,
        'other_judges_scores': other_judges_scores,
        'next_competitor': next_competitor,
        'next_tournament_event': next_tournament_event,
        'previous_competitor': previous_competitor,
        'previous_tournament_event': previous_tournament_event
    }

    return render(request, 'tourney_scoring/tournament_event_scoring.html', context)

# @judge_required
# def submit_judge_form_view(request, tournament_id, tournament_event_id, order):
#     if request.method != 'POST':
#         # invalid request method
#         raise PermissionDenied
    
#     tournament = get_object_or_404(Tournament, pk=tournament_id)
#     tournament_event = get_object_or_404(TournamentEvent, pk=tournament_event_id)
#     if tournament_event.tournament != tournament:
#         # invalid link error
#         raise PermissionDenied

#     competitor = get_object_or_404(Registration, tournament_event=tournament_event, order=order)
#     final_score_obj = competitor.finalscore

#     if final_score_obj.head_judge != request.user.profile:
#         # user is not head judge
#         raise PermissionDenied

#     judge_form = JudgeScoreForm(request.POST)
#     if judge_form.is_valid():
#         judge_score = judge_form.save(commit=False)
#         judge_score.final_score = final_score_obj
#         judge_score.judge = request.user.profile
#         judge_score.save()

#     return redirect('tourney_scoring:event_scoring', tournament_id=tournament_id, tournament_event_id=tournament_event_id, order=order)

# @judge_required
# def submit_final_form_view(request, tournament_id, tournament_event_id, order):
#     if request.method != 'POST':
#         # invalid request method
#         raise PermissionDenied
    
#     tournament = get_object_or_404(Tournament, pk=tournament_id)
#     tournament_event = get_object_or_404(TournamentEvent, pk=tournament_event_id)
#     if tournament_event.tournament != tournament:
#         # invalid link error
#         raise PermissionDenied

#     competitor = get_object_or_404(Registration, tournament_event=tournament_event, order=order)
#     final_score_obj = competitor.finalscore

#     if final_score_obj.head_judge != request.user.profile:
#         # user is not head judge
#         raise PermissionDenied

#     final_form = FinalScoreForm(request.POST, instance=final_score_obj)
#     if final_form.is_valid():
#         final_form.save()
#         return redirect('tourney_scoring:event_scoring', tournament_id=tournament_id, tournament_event_id=tournament_event_id, order=order)
    
#     return render(request, 'tourney_scoring/tournament_event_scoring.html', {'final_form': final_form})
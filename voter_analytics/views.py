from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Count, Q
import plotly
import plotly.graph_objs as go
from datetime import datetime

# View for listing voter records, including filtering and pagination
class VoterListView(ListView):
    '''View to display voter records with filtering options'''
    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters' 
    paginate_by = 50

    def get_queryset(self):
        '''Filter voter records based on query parameters'''
        qs = super().get_queryset()

        # Apply filters based on query parameters from the GET request
        party = self.request.GET.get('party_affiliation', None)
        min_dob = self.request.GET.get('min_dob', None)
        max_dob = self.request.GET.get('max_dob', None)
        voter_score = self.request.GET.get('voter_score', None)
        voted_elections = self.request.GET.getlist('voted_elections', None)  # Multiple values for checkboxes

        # Filter by party affiliation
        if party:
            qs = qs.filter(party_affiliation=party)
        
        # Filter by date of birth range
        if min_dob:
            qs = qs.filter(date_of_birth__gte=f"{min_dob}-01-01")
        if max_dob:
            qs = qs.filter(date_of_birth__lte=f"{max_dob}-12-31")
        
        # Filter by voter score
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        
        # Filter by participation in specific elections
        if voted_elections:
            for election in voted_elections:
                qs = qs.filter(**{election: True})  # Dynamic filter for each election checkbox

        return qs  # Return the filtered QuerySet

    def get_context_data(self, **kwargs):
        '''Add additional context variables for the template'''
        context = super().get_context_data(**kwargs)  # Start with default context

        # Add distinct party affiliations to the context for the filter dropdown
        context['party_affiliations'] = (
            Voter.objects.values_list('party_affiliation', flat=True)
            .distinct()
            .order_by('party_affiliation')
        )

        # Add a range of years for the date of birth filter dropdowns
        current_year = datetime.now().year
        context['years_range'] = range(1920, current_year + 1)

        # Add voter score range for the score filter dropdown
        context['score_range'] = range(0, 6)

        return context  # Return the modified context


# View for displaying details of a single voter
class VoterDetailView(DetailView):
    '''Display a single Voter on its own page'''
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        '''Add additional context for voter detail page'''
        context = super().get_context_data(**kwargs)  # Start with default context

        # Generate a Google Maps link for the voter's address
        voter = self.get_object()  # Get the current voter object
        full_address = f"{voter.street_number} {voter.street_name}, {voter.apartment_number or ''}, {voter.zip_code}"
        context['google_maps_link'] = f"https://www.google.com/maps/search/?api=1&query={full_address.replace(' ', '+')}"

        return context  # Return the modified context


# View for generating and displaying graphs based on voter data
class GraphsView(ListView):
    '''View to display graphs of voter data'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        '''Filter voter records based on query parameters'''
        qs = super().get_queryset()  # Start with the default QuerySet

        # Apply the same filters as VoterListView to ensure graphs match filtered data
        party = self.request.GET.get('party_affiliation', None)
        min_dob = self.request.GET.get('min_dob', None)
        max_dob = self.request.GET.get('max_dob', None)
        voter_score = self.request.GET.get('voter_score', None)
        voted_elections = self.request.GET.getlist('voted_elections', None)

        if party:
            qs = qs.filter(party_affiliation=party)
        if min_dob:
            qs = qs.filter(date_of_birth__gte=f"{min_dob}-01-01")
        if max_dob:
            qs = qs.filter(date_of_birth__lte=f"{max_dob}-12-31")
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        if voted_elections:
            for election in voted_elections:
                qs = qs.filter(**{election: True})

        return qs  # Return the filtered QuerySet

    def get_context_data(self, **kwargs):
        '''Generate graphs and pass them to the template'''
        context = super().get_context_data(**kwargs)  # Start with default context
        voters = self.get_queryset()  # Get the filtered voter data

        context['party_affiliations'] = (
            Voter.objects.values_list('party_affiliation', flat=True)
            .distinct()
            .order_by('party_affiliation')
        )

        # Add a range of years for the date of birth filter dropdowns
        current_year = datetime.now().year
        context['years_range'] = range(1920, current_year + 1)

        # Add voter score range for the score filter dropdown
        context['score_range'] = range(0, 6)

        # Graph 1: Histogram for voter distribution by year of birth
        birth_years = Voter.objects.values_list('date_of_birth__year', flat=True)
        fig1 = go.Histogram(x=list(birth_years))  # Plotly histogram
        title_text = 'Voter Distribution by Year of Birth'
        hist_div = plotly.offline.plot(
            {'data': [fig1], "layout_title_text": title_text,}, 
            auto_open=False, output_type='div'
        )
        context['hist_div'] = hist_div  # Pass graph as HTML div

        # Graph 2: Pie chart for party affiliation distribution
        party_counts = voters.values('party_affiliation').annotate(count=Count('party_affiliation')).order_by('-count')
        fig_pie = go.Pie(labels=[p['party_affiliation'] for p in party_counts], values=[p['count'] for p in party_counts])
        title_text = 'Voter Distribution by Party Affiliation'
        pie_div = plotly.offline.plot(
            {'data': [fig_pie], "layout_title_text": title_text}, 
            auto_open=False, output_type='div'
        )
        context['pie_div'] = pie_div  # Pass graph as HTML div

        # Graph 3: Bar chart for election participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [voters.filter(**{election: True}).count() for election in elections]
        fig_bar = go.Bar(x=elections, y=election_counts)  # Bar chart for elections
        title_text = 'Vote Count by Election'
        bar_div = plotly.offline.plot(
            {'data': [fig_bar], "layout_title_text": title_text}, 
            auto_open=False, output_type='div'
        )
        context['bar_div'] = bar_div  # Pass graph as HTML div

        return context  # Return the modified context

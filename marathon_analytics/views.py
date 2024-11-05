from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Result
class ResultsListView(ListView):
    '''View to display marathon results'''
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50

    def get_queryset(self):
        '''Limit the results to a small number of records'''
        # limit results to first 25 records (for now)
        qs = super().get_queryset()
        # return qs[:25]
        
        # filter results by these field(s):
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            # filter the results by this parameter
            qs = Result.objects.filter(city_icontains=city)
        
        return qs
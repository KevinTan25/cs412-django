from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result
import plotly
import plotly.graph_objs as go

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
    
class ResultDetailView(DetailView):
    '''Display a single Result on it's own page'''

    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'

    # implement some methods...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Provide context variables for use in template'''

        # get the superclass version of the context
        context = super().get_context_data(**kwargs)
        r = context['r'] # obtain the single result instance

        # create graph of first half/second half as pie chart:
        first_half_seconds = r.time_half1.hour * 3600 + r.time_half1.minute * 60 + r.time_half1.second
        second_half_seconds = r.time_half2.hour * 3600 + r.time_half2.minute * 60 + r.time_half2.second
        
        # build a pie chart
        x = ['first half', 'second half']
        y = [first_half_seconds , second_half_seconds]
        
        # generate the Pie chart
        fig = go.Pie(labels=x, values=y) 
        title_text = f"Half Marathon Splits"
        # obtain the graph as an HTML div"
        graph_div_splits = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['graph_div_splits'] = graph_div_splits

        # in-class example
        # pie_div = plotly.offline.plot({'data':[fig]},
        #                               auto_open=False,
        #                               output_type="div")
        # context['pie_div'] = pie_div

        # create graph of runners who passed/passed by
        x= [f'Runners Passed by {r.first_name}', f'Runners who Passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        
        fig = go.Bar(x=x, y=y)
        title_text = f"Runners Passed/Passed By"
        graph_div_passed = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         ) 
        context['graph_div_passed'] = graph_div_passed
        
        return context
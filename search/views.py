from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from search.forms import SearchForm


class SearchView(generic.TemplateView):
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            form = SearchForm(self.request.GET)
        else:
            form = SearchForm()
        context['form'] = form

        return context

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)

        if form.is_valid():
            # redirect_url = reverse('search:flights')
            # params = '&'.join([f'{k}={v}' for k, v in request.GET.items()])
            # return redirect(f'{redirect_url}?{params}')
            # return redirect('search:flights', kwargs = request.get_full_path())
            return redirect(reverse('search:flights') + request.get_full_path()[1:])

        return super().get(request, *args, **kwargs)


class ResultsView(generic.TemplateView):
    template_name = 'search/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            form = SearchForm(self.request.GET)
        else:
            form = SearchForm()
        context['form'] = form

        return context


class ResultsAjaxView(generic.TemplateView):
    template_name = 'search/results_ajax.html'

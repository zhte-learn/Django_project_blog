from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class RulesPageView(TemplateView):
    template_name = 'pages/rules.html'


# class PageNotFoundView(TemplateView):
#     template_name = 'pages/404.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['error_message'] = "Страница не найдена"
#         return context


# class ServerErrorView(TemplateView):
#     template_name = 'pages/500.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['error_message'] = "Произошла ошибка на сервере"
#         return context


# class CSRFErrorView(TemplateView):
#     template_name = 'pages/403csrf.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['error_message'] = "Произошла ошибка CSRF"
#         return context

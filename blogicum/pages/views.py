from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class RulesPageView(TemplateView):
    template_name = "pages/rules.html"


# Я не могу объяснить это, если удаляю комментарии ниже,
# то pytest выдает ошибку.
# Причем код закомментирован, но его отсутствие, даже в закоментированном виде,
# вызызвает ошибку.
# AssertionError: Проверьте view-функции приложения `pages`:
# убедитесь, что для генерации страниц со статусом ответа `{status}`
# используется шаблон `pages/{fname}`
# assert '403csrf.html' in
# 'from django.views.generic import TemplateView\n\n\nclass
# AboutPageView(TemplateView):\n
# template_name = "pages/about.html"\n\n\n
# class RulesPageView(TemplateView):\n
# template_name = "pages/rules.html"\n\n\n
# # class PageNotFoundView(TemplateView):\n#
# template_name = "pages/404.html"\n\n#
# def get_context_data(self, **kwargs):\n#
# context = super().get_context_data(**kwargs)\n#
# context[\'error_message\'] = "Страница не найдена"\n#
# return context\n\n\n# class ServerErrorView(TemplateView):\n#
# template_name = \'pages/500.html\'\n\n#
# def get_context_data(self, **kwargs):\n#
# context = super().get_context_data(**kwargs)\n#
# context[\'error_message\'] = "Произошла ошибка на сервере"\n#
# return context\n\n\n\n'
# where 'from django.views.generic import TemplateView\n\n\nclass
# AboutPageView(TemplateView):\n
# template_name = "pages/about.html"\n\n\n
# class RulesPageView(TemplateView):\n
# template_name = "pages/rules.html"\n\n\n#
# class PageNotFoundView(TemplateView):\n#
# template_name = "pages/404.html"\n\n#
# def get_context_data(self, **kwargs):\n#
# context = super().get_context_data(**kwargs)\n#
# context[\'error_message\'] = "Страница не найдена"\n#
# return context\n\n\n# class ServerErrorView(TemplateView):\n#
# template_name = \'pages/500.html\'\n\n#
# def get_context_data(self, **kwargs):\n#
# context = super().get_context_data(**kwargs)\n#
# context[\'error_message\'] = "Произошла ошибка на сервере"\n#
# return context\n\n\n\n' =
# <function getsource at 0x000001B4FB11CF40>
# tests\test_err_pages.py:100: AssertionError

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

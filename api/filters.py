from django.db.models import QuerySet, Count
from rest_framework import filters
from rest_framework.request import Request
from django.db.models.functions import Length


# class ChoiceCountFilter(filters.BaseFilterBackend):
#     def filter_queryset(self, request: Request, queryset: QuerySet, view):
#         min_choice_count = request.query_params.get('min_choice_text')
#         max_choice_count = request.query_params.get('min_choice_text')
#         if min_choice_count is not None:
#             queryset = queryset.annotate(choice_count=Count('choices')).filter(
#                 choice_count__gte=min_choice_count).filter(choice_count__lte=max_choice_count)
#             return queryset

class ChoiceCountFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        min_choice_count = request.query_params.get('min_choice_count')
        max_choice_count = request.query_params.get('max_choice_count')
        c_question_text = request.query_params.get('question_text')
        if c_question_text is not None:
            queryset = queryset.filter(question_text__icontains=c_question_text)
        if min_choice_count is not None or max_choice_count is not None:
            queryset = queryset.annotate(choice_count=Count('choices'))
        if min_choice_count is not None:
            queryset = queryset.filter(choice_count__gte=min_choice_count)
        if max_choice_count is not None:
            queryset = queryset.filter(choice_count__lte=max_choice_count)
        return queryset


class ArticlesCountWordFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        min_article_text_length = request.query_params.get('min_article_text_length')

        # if min_article_text_length is not None:
        #     queryset = queryset.annotate(text__length__gte=int(min_article_text_length))
        # if min_choice_count is not None:
        #     queryset = queryset.filter(choice_count__gte=min_choice_count)
        # if min_article_text_length is not None:
        #     queryset = queryset.filter(text__length__gte=int(min_article_text_length))
        if min_article_text_length is not None:
            queryset = queryset.annotate(text_length=Length('text')).filter(text_length__gte=int(min_article_text_length))
        return queryset

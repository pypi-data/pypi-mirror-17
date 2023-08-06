from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.cache import add_never_cache_headers
from django.views.decorators.cache import cache_control

from bulbs.content.views import BaseContentDetailView
from bulbs.special_coverage.models import SpecialCoverage
from bulbs.utils.methods import redirect_unpublished_to_login_or_404


class SpecialCoverageView(BaseContentDetailView):
    redirect_correct_path = False

    def get_template_names(self):
        template_names = ["special_coverage/landing.html"]
        template_names.insert(0, getattr(self.special_coverage, "custom_template_name", ""))
        return template_names

    def get(self, request, *args, **kwargs):
        response = super(SpecialCoverageView, self).get(request, *args, **kwargs)

        # Extra unpublished check on Special Coverage activation (BaseContentDetailView only checks
        # first piece of content).
        if not self.special_coverage.is_active:
            if self.show_published_only():
                raise Http404("Special Coverage does not exist.")
            elif not request.user.is_staff:
                return redirect_unpublished_to_login_or_404(request=request,
                                                            next_url=request.get_full_path())

            # Never cache unpublished content
            add_never_cache_headers(response)

        return response

    def get_object(self, *args, **kwargs):
        self.special_coverage = get_object_or_404(SpecialCoverage, slug=self.kwargs.get("slug"))

        qs = self.special_coverage.get_content(published=self.show_published_only()).full()
        if qs.count() == 0:
            raise Http404("No Content available in content list")

        return qs[0]

    def get_context_data(self, *args, **kwargs):
        context = super(SpecialCoverageView, self).get_context_data()
        per_page = 10
        context["per_page"] = per_page

        content_list = self.special_coverage.get_content(
            published=self.show_published_only()
        )[:100]

        context["content_list_total"] = len(content_list)
        context["content_list"] = content_list[:per_page]

        if len(content_list) > per_page:
            context["more_content"] = True
        else:
            context["more_content"] = False

        if hasattr(self.object, "get_reading_list"):
            context["reading_list"] = self.object.get_reading_list()
        context["special_coverage"] = self.special_coverage
        context["targeting"] = {}

        try:
            context["current_video"] = self.special_coverage.videos[0]
        except IndexError:
            context["current_video"] = None

        if self.special_coverage:
            context["targeting"]["dfp_specialcoverage"] = self.special_coverage.slug
            if self.special_coverage.tunic_campaign_id:
                context["targeting"]["dfp_campaign_id"] = self.special_coverage.tunic_campaign_id

        return context

    def show_published_only(self):
        """
        Returns True if `full_preview` is not a query_parameter.
        Used to determine unpublished preview state.
        """
        return bool("full_preview" not in self.request.GET)


class SpecialCoverageLoadMoreView(SpecialCoverageView):

    def get_template_names(self, *args, **kwargs):
        return ["special_coverage/more.html"]

    def get_context_data(self, *args, **kwargs):
        per_page = 10
        offset = int(self.kwargs.get("offset"))
        context = super(SpecialCoverageLoadMoreView, self).get_context_data()
        context["content_list"] = self.special_coverage.get_content(
            published=self.show_published_only()
        )[offset:offset + per_page]

        return context


class SpecialCoverageVideoView(SpecialCoverageView):

    def get_context_data(self, *args, **kwargs):
        context = super(SpecialCoverageVideoView, self).get_context_data()

        video_id = int(self.kwargs.get('video_id'))
        if video_id not in self.special_coverage.videos:
            raise Http404('Video with id={} not in SpecialCoverage'.format(video_id))

        context['current_video'] = video_id

        return context


special_coverage = cache_control(max_age=600)(SpecialCoverageView.as_view())
special_coverage_load_more = cache_control(max_age=600)(SpecialCoverageLoadMoreView.as_view())
special_coverage_video = cache_control(max_age=600)(SpecialCoverageVideoView.as_view())

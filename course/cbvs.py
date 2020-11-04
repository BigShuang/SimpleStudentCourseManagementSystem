from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, reverse, redirect

# Relative import of GeeksModel
from .models import Schedule, StudentCourse
from .forms import ScoreForm, RateForm


class ScheduleDeleteView(DeleteView):
    model = Schedule


class ScoreUpdateView(UpdateView):
    model = StudentCourse
    form_class = ScoreForm
    template_name = 'course/teacher/score.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        title = "给分"
        if request.GET.get("update"):
            title = "修改成绩"

        info = {}
        return_url = reverse("course", kwargs={"kind": "teacher"})
        if self.object:
            teacher = self.object.course.teacher
            info = {
                "name": teacher.name,
                "kind": "teacher",
            }
            return_url = reverse("view_detail", kwargs={"course_id": self.object.course.id})

        return self.render_to_response(self.get_context_data(info=info, title=title, return_url=return_url))

    def get_success_url(self):
        if self.object:
            return reverse("view_detail", kwargs={"course_id": self.object.course.id})
        else:
            return reverse("course", kwargs={"kind": "teacher"})


class RateUpdateView(UpdateView):
    model = StudentCourse
    form_class = RateForm
    template_name = 'course/student/rating.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        info = {}
        return_url = reverse("view_course", kwargs={"view_kind": "is_end"})
        if self.object:
            student = self.object.student
            info = {
                "name": student.name,
                "kind": "student",
            }

        return self.render_to_response(self.get_context_data(info=info, return_url=return_url))

    def get_success_url(self):
        return reverse("view_course", kwargs={"view_kind": "is_end"})


class StudentCourseDetailView(DetailView):
    model = StudentCourse
    template_name = 'course/student/course.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            context["info"] = {
                "name": self.object.student.name,
                "kind": "student",
            }
        return self.render_to_response(context)

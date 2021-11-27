from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import gettext_lazy as _
from oscar.apps.catalogue.models import Product
from ckeditor_uploader.fields import RichTextUploadingField


class SlidesFlatPage(models.Model):
    name = models.CharField(_("name"), max_length=30)
    specific_explanation = models.CharField(_("specific explanation"), max_length=200)
    slide_photo = models.FileField(
        _("slide photo"), upload_to="publisher_photo/", null=True, blank=True
    )
    publications_slide = models.BooleanField(
        _("publish slide photo"), default=False, null=True, blank=True
    )
    paragraph = RichTextUploadingField(
        _("paragraph"),
    )
    product_link = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    # ...
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # ...

    created_at = models.DateTimeField("Date of creation", auto_now_add=True)
    modified_at = models.DateTimeField("Date of change", auto_now=True)

    to_publish = models.BooleanField(_("to publish slideshows"), default=False)

    class Meta:
        ordering = ("-modified_at",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "catalogue:detail", kwargs={"product_slug": self.slug, "pk": self.id}
        )


class SlidesFlatShow(models.Model):
    slides_show_name = models.CharField(_("slides show name"), max_length=33)
    image = GenericRelation(SlidesFlatPage, related_query_name="slidesflatpage")
    published = models.BooleanField(_("published"), default=True)

    def __str__(self):
        return self.slides_show_name

    class Meta:
        ordering = ("-published",)

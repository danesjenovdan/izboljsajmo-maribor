from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext as _

from urllib.parse import urlparse, parse_qs

from behaviors.behaviors import Timestamped

class AboutType(models.TextChoices):
    TITLE = 'H2', _('Title')
    TITLE2 = 'H3', _('Title2')
    TEXT = 'TXT', _('Text')
    IMAGE = 'IMG', _('Image')
    YOUTUBE_EMBED = 'YT', _('YoutubeEmbed')
    LINK = 'LINK', _('Link')


class About(Timestamped):
    order = models.IntegerField(_("Order"), default=1)
    type = models.CharField(
        _('About section type'),
        max_length=5,
        choices=AboutType.choices,
        default=AboutType.TITLE)
    content = models.TextField(_("Content"), null=True, blank=True)
    image = models.ImageField(
        _('Image'),
        null=True,
        blank=True)
    url = models.URLField(null=True, blank=True)
    description = models.CharField(
        _('Description of section'),
        max_length=50)

    def preview(self):
        content = ''
        if self.type == AboutType.IMAGE:
            content = mark_safe(
                f'<img src="{self.image.url if self.image else self.url}" max-width="200" height="100">'
            )
        elif self.type == AboutType.TITLE:
            content = mark_safe(
                f'<h3>{self.content}</h3>'
            )
        elif self.type == AboutType.TITLE2:
            content = mark_safe(
                f'<h4>{self.content}</h4>'
            )
        elif self.type == AboutType.TEXT:
            content = mark_safe(
                f'{self.content}'
            )
        elif self.type == AboutType.YOUTUBE_EMBED:
            parsed_url = urlparse(self.url)
            video_id = parse_qs(parsed_url.query)['v'][0]

            content = mark_safe(
                f'<img src="https://img.youtube.com/vi/{video_id}/0.jpg" max-width="200" height="100">'
            )
        elif self.type == AboutType.LINK:
            content = mark_safe(
                f'<a href="{self.url}">{self.url}</a>'
            )
        return content

    class Meta:
        verbose_name = u"Preview"


class YoutubeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=AboutType.YOUTUBE_EMBED)


class TitleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=AboutType.TITLE)


class Title2Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=AboutType.TITLE2)


class ImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=AboutType.IMAGE)


class ContentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=AboutType.TEXT)


class AboutYoutubeEmbed(About):
    objects = YoutubeManager()
    class Meta:
        proxy=True


class AboutTitle(About):
    objects = TitleManager()
    class Meta:
        proxy=True


class AboutTitle2(About):
    objects = Title2Manager()
    class Meta:
        proxy=True


class AboutImage(About):
    objects = ImageManager()
    class Meta:
        proxy=True


class AboutContent(About):
    objects = ContentManager()
    class Meta:
        proxy=True

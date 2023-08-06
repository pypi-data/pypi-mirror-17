Django integration of GpxPy
===========================
[![Build Status](https://travis-ci.org/PetrDlouhy/django-gpxpy.svg?branch=master)](https://travis-ci.org/PetrDlouhy/django-gpxpy)


This module only contains simple code that parses GPX file to MultiLineString using GpxPy. In the future it might also contain GPX model field and GPX form field which would be used to upload GPX file and parse it.

Installation
------------

```
pip install django-gpxpy
```

Example of usage
-----

```
from django_gpxpy import gpx_parse

class TrackModel(models.Model):
      track = models.MultiLineStringField(
          verbose_name=_(u"trasa"),
          srid=4326,
          null=True,
          blank=True,
          geography=True,
      )

class TrackForm(ModelForm):
    gpx_file = forms.FileField(required=False, help_text=_(u"Upload geometry by GPX file"))

    class Meta:
        model = TrackModel

    def clean(self):
        if self.gpx_file:
            self.track_clean = gpx_parse.parse_gpx_filefield(track_file)
```


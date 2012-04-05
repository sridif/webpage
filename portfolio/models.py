from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
import datetime


class Award(models.Model):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    year = models.DateField()
    url = models.URLField('URL', blank=True)

    class Meta:
        ordering = ['organization', 'category', '-year']

    def __unicode__(self):
        return u'%s' % (self.name)


class Client(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    url = models.URLField('URL', blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)


class Review(models.Model):
    STAR_CHOICES = (
        ('five', '5 stars'),
        ('four', '4 stars'),
        ('three', '3 stars'),
        ('two', '2 stars'),
        ('one', '1 star'),
        ('zero', '0 stars')
    )
    quote = models.TextField()
    stars = models.CharField(max_length=100, choices=STAR_CHOICES, blank=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    url = models.URLField('URL', blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)


class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)


class Technology(models.Model):
    name = models.CharField(max_length=255)
    abbr = models.CharField('Abbreviation', max_length=255, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Technologies'

    def __unicode__(self):
        return u'%s' % (self.name)


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(active_status=True)


class FeaturedManager(models.Manager):
    def get_query_set(self):
        return super(FeaturedManager, self).get_query_set().filter(active_status=True).filter(featured_status=True)


class Work(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    order = models.PositiveIntegerField()
    date_launched = models.DateField()
    logo = models.ImageField(blank=True, null=True, upload_to='img/portfolio/logos')
    description = models.TextField()
    client = models.ForeignKey(Client, blank=True, null=True)
    review = models.ManyToManyField(Review, blank=True, null=True)
    award = models.ManyToManyField(Award, blank=True, null=True)
    url = models.URLField('URL', blank=True)
    style = models.TextField(blank=True, help_text='Custom CSS for the page')

    active_status = models.BooleanField('Active?', default=True)
    featured_status = models.BooleanField('Featured?')
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)

    active = ActiveManager()
    featured = FeaturedManager()
    objects = models.Manager()

    class Meta:
        ordering = ['order']
        get_latest_by = 'date_launched'

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        super(Work, self).save(*args, **kwargs)

    def get_previous_work(self):
        return self.get_previous_by_date_launched()

    def get_next_work(self):
        return self.get_next_by_date_launched()

    def get_absolute_url(self):
        return ('portfolio_work_detail', [self.slug])
    get_absolute_url = models.permalink(get_absolute_url)


class Project(models.Model):
    work = models.ForeignKey(Work)
    service = models.ForeignKey(Service)
    order = models.PositiveIntegerField()
    description = models.TextField()
    technology = models.ManyToManyField(Technology)
    url = models.URLField('URL', blank=True)
    itunes = models.BooleanField('iTunes App Store URL?')

    active_status = models.BooleanField('Active?', default=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)

    active = ActiveManager()
    objects = models.Manager()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s, %s' % (self.work, self.service)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        super(Project, self).save(*args, **kwargs)


class Media(models.Model):
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('flash', 'Flash'),
        ('pdf', 'PDF'),
        ('other', 'Other')
    )
    project = models.ForeignKey(Project)
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    image = models.ImageField(blank=True, null=True, upload_to='img/portfolio')
    file = models.FileField(blank=True, null=True, upload_to='files')

    active_status = models.BooleanField('Active?', default=True)

    active = ActiveManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Media'

    def __unicode__(self):
        return u'%s' % (self.title)

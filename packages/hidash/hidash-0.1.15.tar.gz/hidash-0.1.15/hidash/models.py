from django.db import models


FREQUENCY = ((0, 'Daily'),
             (1, 'Weekly'),
             (2, 'Monthly'),
             (3, 'Yearly'))

CHART_WIDTHS = ((1, '1'), (2, '2'), (3, '3'), (4, '4'),
                (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                (9, '9'), (10, '10'), (11, '11'), (12, '12'))


class Chart(models.Model):
    '''
    Holds the configuration of a chart
    '''
    name = models.CharField(max_length=25, unique=True)
    library = models.CharField(max_length=15, null=True, blank=True)
    dimension = models.CharField(max_length=50, null=True, blank=True)
    chart_type = models.CharField(max_length=15, null=True, blank=True)
    query = models.TextField(max_length=10000)
    frequency = models.IntegerField(choices=FREQUENCY, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    grid_width = models.IntegerField(choices=CHART_WIDTHS, null=True, blank=True)
    height = models.CharField(max_length=3, null=True, blank=True)
    priority = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class ChartGroup(models.Model):
    '''
    Holds the Group names for grouping multiple charts under that group
    '''
    name = models.CharField(max_length=25)
    chart = models.ForeignKey(Chart)

    def __unicode__(self):
        return self.name


class ChartMetric(models.Model):
    '''
    One to many mapping to hold the metrics of a chart
    '''
    chart = models.ForeignKey(Chart, related_name='chart')
    metric = models.CharField(max_length=50)

    def __unicode__(self):
        return self.metric


class ChartAuthGroup(models.Model):
    '''
    One to many mapping to hold the chart_groups permitted to view the chart
    '''
    chart = models.ForeignKey(Chart)
    auth_group = models.CharField(max_length=50)

    def __unicode__(self):
        return self.auth_group


class ChartAuthPermission(models.Model):
    '''
    One to many mapping to hold the needed permissions to view the chart
    '''
    chart = models.ForeignKey(Chart)
    permission = models.CharField(max_length=50)

    def __unicode__(self):
        return self.permission


class ScheduledReport(models.Model):
    '''
    It will contain the parameters for the reports and reports recipients
    '''
    report = models.ManyToManyField(Chart)


class ReportRecipients(models.Model):
    '''
    It will store all the recipients for a given group of reports
    '''
    email_address = models.CharField(max_length=512, default='', blank=True)
    report = models.ForeignKey(ScheduledReport)


class ScheduledReportParam(models.Model):
    '''
    It will store the query parameters for every schedule report
    '''
    parameter_name = models.CharField(max_length=128, default='', blank=True)
    parameter_value = models.CharField(max_length=128, default='', blank=True)
    scheduled_report = models.ForeignKey(ScheduledReport)

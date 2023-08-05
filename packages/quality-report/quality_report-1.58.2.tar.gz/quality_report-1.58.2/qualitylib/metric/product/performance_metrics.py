"""
Copyright 2012-2016 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import

import datetime

from ... import domain, metric_source


class ResponseTimes(domain.Metric):
    """ Class for measuring response times as determined by performance tests. """
    name = 'Overschrijding van responsetijden'
    unit = 'performancetestqueries'
    missing_report_template = 'Er is geen performancetestrapport voor {name}:{version}.'
    norm_template = 'Geen van de {unit} overschrijdt de gewenste responsetijd. Als een of meer ' \
        '{unit} de maximum responsetijd overschrijden is de score rood, anders geel.'
    above_target_template = 'Alle {nr_queries} {unit} draaien in 90% van de gevallen binnen de ' \
        'gewenste responsetijd (meting {date}, {age} geleden).'
    below_max_target_template = '{value_max} van de {nr_queries} {unit} draaien niet in 90% ' \
        'van de gevallen binnen de maximale responsetijd (meting {date}, {age} geleden).'
    below_wish_target_template = '{value_wish} van de {nr_queries} {unit} draaien niet in 90% ' \
        'van de gevallen binnen de gewenste responsetijd (meting {date}, {age} geleden).'
    below_both_targets_template = '{value_max} van de {nr_queries} {unit} draaien niet in 90% ' \
        'van de gevallen binnen de maximale responsetijd en {value_wish} van de {nr_queries} {unit} draaien niet ' \
        'in 90% van de gevallen binnen de gewenste responsetijd (meting {date}, {age} geleden).'
    metric_source_classes = (metric_source.PerformanceReport,)

    perfect_value = 0
    target_value = 0  # Not used
    low_target_value = 0  # Not used

    def __init__(self, *args, **kwargs):
        super(ResponseTimes, self).__init__(*args, **kwargs)
        if not self._subject.product_version():
            self.old_age = datetime.timedelta(hours=7 * 24)
            self.max_old_age = datetime.timedelta(hours=14 * 24)
            self.norm_template = 'Geen van de {unit} overschrijdt de gewenste responsetijd en de performancemeting ' \
                'is niet ouder dan {old_age}. Als een of meer {unit} de maximum responsetijd overschrijden of als ' \
                'de meting ouder is dan {max_old_age}, is de score rood, anders geel.'

    def value(self):
        return None  # We use max_violations and wish_violations as value

    def numerical_value(self):
        max_violations = self._max_violations()
        wish_violations = self._wish_violations()
        return -1 if None in (max_violations, wish_violations) else max_violations + wish_violations

    def _max_violations(self):
        """ The number of performance queries that is slower than the maximum response time. """
        return self._metric_source.queries_violating_max_responsetime(*self.__product_id())

    def _wish_violations(self):
        """ The number of performance queries that is slower than the wished for response time. """
        return self._metric_source.queries_violating_wished_responsetime(*self.__product_id())

    def _is_perfect(self):
        return self._max_violations() == self._wish_violations() == 0 and not self._is_old() and self.__report_exists()

    def _needs_immediate_action(self):
        return self._max_violations() > 0 or self._is_too_old() or not self.__report_exists()

    def _is_below_target(self):
        return self._max_violations() > 0 or self._wish_violations() > 0 or self._is_old() or not self.__report_exists()

    def _missing(self):
        return self.numerical_value() < 0

    def _get_template(self):
        if self.status() in ('missing_source', 'missing'):
            return super(ResponseTimes, self)._get_template()
        if not self.__report_exists():
            return self.missing_report_template
        max_violations = self._max_violations()
        wish_violations = self._wish_violations()
        if max_violations and wish_violations:
            return self.below_both_targets_template
        elif max_violations:
            return self.below_max_target_template
        elif wish_violations:
            return self.below_wish_target_template
        else:
            return self.above_target_template

    def _parameters(self):
        parameters = super(ResponseTimes, self)._parameters()
        if self.__report_exists():
            parameters.update(dict(nr_queries=self.__nr_queries(),
                                   value_max=self._max_violations(),
                                   value_wish=self._wish_violations()))
        return parameters

    def _date(self):
        return self._metric_source.date(*self.__product_id())

    def _metric_source_urls(self):
        return self._metric_source.urls(*self.__product_id()) or []

    def __report_exists(self):
        """ Return whether a performance report exists for the product and version this metric reports on. """
        return self._metric_source.exists(*self.__product_id())

    def __nr_queries(self):
        """ Return the number of performance queries in the performance report for the product. """
        return self._metric_source.queries(*self.__product_id())

    def __product_id(self):
        """ Return the performance report id and version of the product. """
        return self._metric_source_id, self._subject.product_version()

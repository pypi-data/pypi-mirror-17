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

import datetime
import unittest

from qualitylib import metric, domain, metric_source


class FakeNCover(object):
    """ Fake NCover. """
    url = 'http://ncover'

    @staticmethod
    def statement_coverage(ncover_id):  # pylint: disable=unused-argument
        """ Return the ART coverage. """
        return 98

    branch_coverage = statement_coverage

    @staticmethod
    def coverage_date(ncover_id):  # pylint: disable=unused-argument
        """ Return a fake date. """
        return datetime.datetime.today() - datetime.timedelta(days=4)


class FakeJaCoCo(FakeNCover):
    """ Fake JaCoCo. """
    url = 'http://jacoco'


class FakeSubject(object):
    """ Provide for a fake subject. """
    def __init__(self, version='', art='', metric_source_ids=None):
        self.__version = version
        self.__art = art
        self.__metric_source_ids = metric_source_ids or dict()

    @staticmethod
    def name():
        """ Return the name of the subject. """
        return 'FakeSubject'

    def product_version(self):
        """ Return the version of the subject. """
        return self.__version

    def metric_source_id(self, the_metric_source):
        """ Return the id of the subject for the metric source. """
        return self.__metric_source_ids.get(the_metric_source)


class ARTStatementCoverageJacocoTest(unittest.TestCase):
    """ Unit tests for the ART coverage metric. """
    def setUp(self):
        self.__jacoco = FakeJaCoCo()
        self.__subject = FakeSubject(metric_source_ids={self.__jacoco: 'http://jacoco'}, version='1.1')
        self.__project = domain.Project(metric_sources={metric_source.CoverageReport: self.__jacoco})
        self.__metric = metric.ARTStatementCoverage(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that value of the metric equals the coverage as reported by Jacoco. """
        self.assertEqual(self.__jacoco.statement_coverage(None), self.__metric.value())

    def test_url(self):
        """ Test that the url is correct. """
        self.assertEqual(dict(CoverageReport='http://jacoco'), self.__metric.url())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertTrue(self.__metric.report().startswith('FakeSubject ART statement coverage is 98%'))


class ARTStatementCoverageNCoverTest(unittest.TestCase):
    """ Unit tests for the ART statement coverage metric. """
    def setUp(self):
        self.__ncover = FakeNCover()
        self.__subject = FakeSubject(metric_source_ids={self.__ncover: 'http://ncover'})
        self.__project = domain.Project(metric_sources={metric_source.CoverageReport: self.__ncover})
        self.__metric = metric.ARTStatementCoverage(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that value of the metric equals the coverage as reported by NCover. """
        self.assertEqual(self.__ncover.statement_coverage(None), self.__metric.value())

    def test_url(self):
        """ Test that the url is correct. """
        self.assertEqual(dict(CoverageReport='http://ncover'), self.__metric.url())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertTrue(self.__metric.report().startswith('FakeSubject ART statement coverage is 98%'))


class ARTBranchCoverageJacocoTest(unittest.TestCase):
    """ Unit tests for the ART branch metric. """
    def setUp(self):
        self.__jacoco = FakeJaCoCo()
        self.__subject = FakeSubject(metric_source_ids={self.__jacoco: 'http://jacoco'}, version='1.1')
        self.__project = domain.Project(metric_sources={metric_source.CoverageReport: self.__jacoco})
        self.__metric = metric.ARTBranchCoverage(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that value of the metric equals the coverage as reported by Jacoco. """
        self.assertEqual(self.__jacoco.branch_coverage(None), self.__metric.value())

    def test_url(self):
        """ Test that the url is correct. """
        self.assertEqual(dict(CoverageReport='http://jacoco'), self.__metric.url())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertTrue(self.__metric.report().startswith('FakeSubject ART branch coverage is 98%'))


class ARTBranchCoverageNCoverTest(unittest.TestCase):
    """ Unit tests for the ART branch coverage metric. """
    def setUp(self):
        self.__ncover = FakeNCover()
        self.__subject = FakeSubject(metric_source_ids={self.__ncover: 'http://ncover'})
        self.__project = domain.Project(metric_sources={metric_source.CoverageReport: self.__ncover})
        self.__metric = metric.ARTBranchCoverage(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that value of the metric equals the coverage as reported by NCover. """
        self.assertEqual(self.__ncover.branch_coverage(None), self.__metric.value())

    def test_url(self):
        """ Test that the url is correct. """
        self.assertEqual(dict(CoverageReport='http://ncover'), self.__metric.url())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertTrue(self.__metric.report().startswith('FakeSubject ART branch coverage is 98%'))


class FakeJenkinsTestReport(object):
    """ Fake a Jenkins test report instance for unit test purposes. """
    def __init__(self):
        self.passed = 14

    @staticmethod
    def failed_tests(*args):  # pylint: disable=unused-argument
        """ Return the number of failing tests for the job. """
        return 4

    @staticmethod
    def skipped_tests(*args):  # pylint: disable=unused-argument
        """ Return the number of skipped tests for the job. """
        return 2

    def passed_tests(self, *args):  # pylint: disable=unused-argument
        """ Return the number of passed tests for the job. """
        return self.passed

    def report_datetime(self, *args):  # pylint: disable=unused-argument
        """ Return the number of passed tests for the job. """
        return datetime.datetime.min if self.passed < 0 else datetime.datetime(2016, 1, 1, 12, 0, 0)


class FailingRegressionTestsTest(unittest.TestCase):
    """ Unit tests for the failing regression tests metric. """
    def setUp(self):
        self.__jenkins = FakeJenkinsTestReport()
        self.__subject = FakeSubject(metric_source_ids={self.__jenkins: 'jenkins_job'})
        self.__project = domain.Project(metric_sources={metric_source.TestReport: self.__jenkins})
        self.__metric = metric.FailingRegressionTests(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that value of the metric equals the failing tests as reported by Jenkins. """
        self.assertEqual(self.__jenkins.failed_tests('jenkins_job') + self.__jenkins.skipped_tests('jenkins_job'),
                         self.__metric.value())

    def test_value_multiple_jobs(self):
        """ Test that the value of the metric equals to total number of failing tests if there are multiple
            test reports. """
        subject = FakeSubject(metric_source_ids={self.__jenkins: ['a', 'b']})
        failing_tests = metric.FailingRegressionTests(subject=subject, project=self.__project)
        expected = self.__jenkins.failed_tests('a', 'b') + self.__jenkins.skipped_tests('a', 'b')
        self.assertEqual(expected, failing_tests.value())

    def test_value_when_missing(self):
        """ Test that the value is negative when the test report is missing. """
        self.__jenkins.passed = -1
        self.failUnless(self.__metric.value() < 0)

    def test_report(self):
        """ Test that the report for the metric is correct. """
        self.assertEqual('6 van de 20 regressietesten van FakeSubject slagen niet.', self.__metric.report())

    def test_url(self):
        """ Test that the url points to the Jenkins job. """
        self.assertEqual({'Test report': 'jenkins_job'}, self.__metric.url())

    def test_url_multiple_jobs(self):
        """ Test that the url points to the Jenkins jobs. """
        subject = FakeSubject(metric_source_ids={self.__jenkins: ['a', 'b']})
        failing_tests = metric.FailingRegressionTests(subject=subject, project=self.__project)
        self.assertEqual({'Test report (1/2)': 'a', 'Test report (2/2)': 'b'}, failing_tests.url())


class RegressionTestAgeTest(unittest.TestCase):
    """ Unit tests for the regression test age metric. """
    def setUp(self):
        self.__jenkins = FakeJenkinsTestReport()
        self.__subject = FakeSubject(metric_source_ids={self.__jenkins: 'jenkins_job'})
        self.__project = domain.Project(metric_sources={metric_source.TestReport: self.__jenkins})
        self.__metric = metric.RegressionTestAge(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that value of the metric equals the report date as reported by Jenkins. """
        expected = (datetime.datetime.now() - self.__jenkins.report_datetime('jenkins_job')).days
        self.assertEqual(expected, self.__metric.value())

    def test_value_multiple_jobs(self):
        """ Test that the value of the metric equals to minimum report age if there are multiple
            test reports. """
        subject = FakeSubject(metric_source_ids={self.__jenkins: ['a', 'b']})
        age = metric.RegressionTestAge(subject=subject, project=self.__project)
        expected = (datetime.datetime.now() - self.__jenkins.report_datetime('a', 'b')).days
        self.assertEqual(expected, age.value())

    def test_value_when_missing(self):
        """ Test that the value is negative when the test report is missing. """
        self.__jenkins.passed = -1
        self.failUnless(self.__metric.value() < 0)

    def test_report(self):
        """ Test that the report for the metric is correct. """
        days = (datetime.datetime.now() - self.__jenkins.report_datetime()).days
        self.assertEqual('De regressietest van FakeSubject is {} dagen geleden gedraaid.'.format(days),
                         self.__metric.report())

    def test_url(self):
        """ Test that the url points to the Jenkins job. """
        self.assertEqual({'Test report': 'jenkins_job'}, self.__metric.url())

    def test_url_multiple_jobs(self):
        """ Test that the url points to the Jenkins jobs. """
        subject = FakeSubject(metric_source_ids={self.__jenkins: ['a', 'b']})
        failing_tests = metric.RegressionTestAge(subject=subject, project=self.__project)
        self.assertEqual({'Test report (1/2)': 'a', 'Test report (2/2)': 'b'}, failing_tests.url())

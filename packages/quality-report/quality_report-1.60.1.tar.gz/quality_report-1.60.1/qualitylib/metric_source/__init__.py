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


# Test report
from .abstract.test_report import TestReport
from .test_report.jenkins_test_report import JenkinsTestReport
from .test_report.junit_test_report import JunitTestReport

# Coverage report
from .abstract.coverage_report import CoverageReport
from .coverage_report.jacoco import JaCoCo
from .coverage_report.ncover import NCover

# Performance report
from .abstract.performance_report import PerformanceReport
from .performance_report.jmeter import JMeter
from .performance_report.silkperformer import SilkPerformer

# Archive system
from .abstract.archive_system import ArchiveSystem
from .archive_system.nexus import Nexus

# Version control system
from .abstract.version_control_system import VersionControlSystem
from .version_control_system.git import Git
from .version_control_system.subversion import Subversion

# OWASP dependency report
from .abstract.owasp_dependency_report import OWASPDependencyReport
from .owasp_dependency_report.jenkins_owasp_dependency_plugin import JenkinsOWASPDependencyReport
from .owasp_dependency_report.owasp_dependency_xml_report import OWASPDependencyXMLReport

# Other metric sources
from .ansible_config_report import AnsibleConfigReport
from .birt import Birt
from .dependencies import Dependencies
from .history import History
from .holiday_planner import HolidayPlanner
from .jenkins import Jenkins
from .jira import Jira
from .maven import Maven
from .open_vas_scan_report import OpenVASScanReport
from .pom import Pom
from .release_candidates import ReleaseCandidates
from .sonar import Sonar
from .trello import TrelloBoard, TrelloActionsBoard, TrelloRiskBoard
from .wiki import Wiki
from .open_vas_scan_report import OpenVASScanReport
from .zap_scan_report import ZAPScanReport
from .url_opener import UrlOpener

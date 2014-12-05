__author__ = 'Shridhar'

import dominate
from dominate.tags import *
from os import path,makedirs
from shutil import copytree, rmtree
from datetime import datetime
import urllib
import pickle

class Report():
    _current_dir = path.realpath(__file__)[0:path.realpath(__file__).rfind(path.sep)]
    _default_reports_dir = path.join(_current_dir, "reports")
    _results = []
    _reports_dir = "" # Initialized in constructor.
    _resources = path.join(_current_dir, "resources")
    _COLLECTOR_URL = "http://collector.bonzai.mobi/rec?"

    def __init__(self, reports_dir=_default_reports_dir):
        """
        :return: none
        """
        self._reports_dir = reports_dir
        if path.exists(self._reports_dir):
            rmtree(self._reports_dir)
        makedirs(self._reports_dir)

    def _copy_resources(self, dest=None):
        if None is dest:
            dest = self._reports_dir
        else:
            dest = path.join(self._reports_dir, dest)
        copytree(self._resources, path.join(dest, "resources"))

    def _validate_all_requests(self, test, requests):
        test['requests'] = requests
        test["impressions_validations_failed"] = 0
        test['tracker'] = ""

        for imp in test["expected_impressions"]:
            params = {}
            for req in requests:
                print req
                url = req["request"]["url"]
                if url.startswith(self._COLLECTOR_URL) and imp["pattern"] in url:
                    params = dict(s.split("=") for s in url.replace("http://collector.bonzai.mobi/rec?", "").split("&"))
                    break
            if len(params) is 0:
                imp['result'] = "Not found"
            else:
                imp['result'] = "found"
                imp['raw_impression'] = req["request"]
                imp['raw_url'] = url
                imp['params'] = params
                if test['tracker'] == "":
                    test['tracker'] = params['tk']
                for exp in imp['expected_params']:
                    if exp['expected_value'] == "[today]":
                        exp['actual_value'] = urllib.unquote(params[exp['pattern']]).decode('utf8')
                        now = datetime.now()
                        exp['expected_value'] = now.strftime("%a %b %Y %H")
                        if exp['actual_value'].startswith(exp['expected_value']):
                            exp['result'] = "pass"
                        else:
                            exp['result'] = "fail"
                    else:
                        exp['actual_value'] = params[exp['pattern']]
                        if exp['expected_value'] == exp['actual_value']:
                            exp['result'] = "pass"
                        else:
                            exp['result'] = "fail"

        impressions_found = 0
        test["result"] = "unknown"
        for imp in test["expected_impressions"]:
            if imp["result"] == "found":
                impressions_found = impressions_found + 1
            validations_failed = 0
            for exp in imp['expected_params']:
                if exp["result"] == "fail":
                    validations_failed = validations_failed + 1
            imp["validations_failed"] = validations_failed
            if validations_failed > 0 :
                test["impressions_validations_failed"] = test["impressions_validations_failed"] + 1
        test["impressions_found"] = impressions_found
        if impressions_found < len(test["expected_impressions"]) and test["impressions_validations_failed"] > 0:
            test["result"] = "fail"
        else:
            test["result"] = "pass"



    def update_result(self, test, requests):
        """

        :param test:
        :param requests:
        :return: None
        """
        self._validate_all_requests(test, requests)
        self._results.append(test)

    def dump(self):
        pick_file= open("results.pickle", "w")
        pickle.dump(self._results, pick_file)
        pick_file.close()

    def load_pickle(self):
        pick_file= open("results.pickle", "r")
        self._results = pickle.load(pick_file)
        pick_file.close()

    def create_report(self):
        self.create_summary_report()
        for test in self._results:
            self.create_test_report(test)


    def create_summary_report(self):

        _noscript = "Javascript was not detected. Please enable Javascript in this page to access the data in this report."

        OutputFile = open(path.join(self._reports_dir,"Index.html"), 'w')

        doc = dominate.document(title='Test results')
        doc.body['id']='body-summary'

        with doc.head:
            meta(http_equiv='Content-Type', content='text/html; charset=UTF-8')
            link(rel='shortcut icon', href='resources/images/favicon_auto.ico')
            link(rel='stylesheet', href='resources/style.css?ver=2', type='text/css')
            script(type='text/javascript', src='resources/reports.js?ver=2')
            script(type='text/javascript', src='resources/navigation.js')

        with doc:
            doc.add(noscript(div(_noscript, id='noscript')))
            with div(id='main-report'):
                div('Main Menu', id='returntomenu', cls='floating')
                div('Next Report', id='nextbutton', cls='floating')
                div('Previous Report', id='backbutton', cls='floating')
                iframe(id='report-iframe', src='', frameborder='0', seamless='true')
            with div(id='main-menu', cls='main'):
                with div(cls='header'):
                    with div(cls='logo'):
                        with div(cls='hdr-title'):
                            link('www.talentica.com', href='http://www.talentica.com', target='_BLANK')
                div(cls='clear')
                with div(cls='body-content'):
                    h1('Summary Report')
                    with div(cls='content'):
                        result_tbl = table(cls='tbl', cellspacing='0', cellpadding='10', border='0')
                        with result_tbl.add(thead()):
                            th('#', width='35')
                            th('Name', width='250')
                            th('Expected Impressions')
                            th('Impressions found')
                            th('Status', width='150')

                        with result_tbl.add(tbody()):
                            for i, test in enumerate(self._results):
                                r = tr()
                                r += td(str(i))
                                r += td(span(test["name"], href=test["name"] + "/index.html"))
                                r += td(len(test['expected_impressions']))
                                r += td(test['impressions_found'])
                                if test["result"] == 'pass':
                                    class_name = 'icon ok'
                                else:
                                    class_name = 'icon failed'
                                r += td(span(test["result"], cls=class_name))



        # print doc
        OutputFile.writelines(doc.__str__())
        self._copy_resources(self._reports_dir)

    def create_test_report(self, test):
        _noscript = "Javascript was not detected. Please enable Javascript in this page to access the data in this report."
        testfolder = path.join(self._reports_dir, test["name"])

        if not path.exists(testfolder):
            makedirs(testfolder)
        OutputFile = open(path.join(testfolder, "Index.html"), 'w')
        doc = dominate.document(title='Report :'+test["name"])

        with doc.head:
            meta(http_equiv='Content-Type', content='text/html; charset=UTF-8')
            link(rel='shortcut icon', href='resources/images/favicon_auto.ico')
            link(rel='stylesheet', href='resources/style.css?ver=2', type='text/css')
            script(type='text/javascript', src='resources/reports.js?ver=2')
        with doc:
            doc.add(noscript(div(_noscript, id='noscript')))
            with div( cls='main'):
                with div(cls='header'):
                    div(cls='logo')
                    with div(cls='hdr-title'):
                        link('www.talentica.com', href='http://www.talentica.com', target='_BLANK')
                div(cls='clear')
                with div(cls='body-content'):
                    h1('Test report : '+test['name'])
                    with div(cls='content'):
                        with div(cls='left-panel'):
                            with ul(id='report-bar-ul'):
                                with li(cls='selected'):
                                    span(cls='icon summary-s')
                                    span("Test Execution Summary", cls='txt')
                                    span(cls='right-arrow')
                                for i, imp in enumerate(test['expected_impressions']):
                                    with li(title=imp['name']):
                                        if imp['result'] == "found":
                                            span(cls='icon ok')
                                        else:
                                            span(cls="icon failed")
                                        span(i, cls='nmbr')
                                        span(imp["pattern"], cls="txt")
                                        span(cls='right-arrow')
                        with div(cls='right-panel'):

                            with div(cls='results'):
                                h1(span(cls='icon summary-m'))
                                with div(cls='status'):
                                    span("Passed", cls='icon ok')
                                div(dominate.util.unescape(dominate.util.unescape('&')+'nbsp;'), style='height: 20px')
                                sum_table = table(cls='tbl inner', cellspacing='0', cellpadding='5')
                                with sum_table.add(tbody()):
                                    tr1 = tr()
                                    tr1.add(td('Html File:', width='125px'))
                                    tr1.add(td('ab.html'))

                                    tr2 = tr()
                                    tr2.add(td('Analytics Unique Tracker ID:'))
                                    tr2.add(td(test['tracker']))

                                    tr3 = tr()
                                    tr3.add(td('# Impresssions found (Expected)'))
                                    tr3.add(td(str(test['impressions_found'])+"("+str(len(test['expected_impressions']))+")"))

                            for i, imp in enumerate(test['expected_impressions']):

                                with div(cls='results'):
                                    with ul(cls='sub-tabs'):
                                        li('Results', cls='selected')
                                        li('Debug')
                                    with div(cls='sub-results', style='display:block'):
                                        with h1(imp["name"]):
                                            div(imp["description"], cls='desc')
                                        param_tbl = table(cls='tbl', cellspacing='0', cellpadding='10', border='0')
                                        with param_tbl.add(thead()):
                                            th("#")
                                            th("name",width="30%")
                                            th("expected value", width = "20%")
                                            th("actual value", width= "20%")
                                            th("result")
                                        with param_tbl.add(tbody()):
                                            for j, param in enumerate(imp["expected_params"]):
                                                r = tr()
                                                r += td(str(j))
                                                r += td(param["name"])
                                                r += td(param["expected_value"])
                                                r += td(param["actual_value"])
                                                if param["result"] == 'pass':
                                                    r += td(span(param["result"], cls='icon ok'))
                                                else:
                                                    r += td(span(param["result"], cls='icon failed'))
                                    with div(cls='sub-results'):
                                        h1("All Parameters")
                                        param_tbl1 = table(cls='tbl', cellspacing='0', cellpadding='10', border='0')
                                        with param_tbl1.add(thead()):
                                            th("name")
                                            th("value")
                                        with param_tbl1.add(tbody()):
                                            for p in imp['params'].keys():
                                                tr3 = tr()
                                                tr3.add(td(p))
                                                tr3.add(td(imp['params'][p]))
        self._copy_resources(testfolder)
        OutputFile.writelines(doc.__str__())

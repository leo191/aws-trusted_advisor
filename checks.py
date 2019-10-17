from __future__ import print_function
import os
import boto3
import traceback
from collections import OrderedDict



try:
    support_client = boto3.client('support', region_name='us-east-1')
    ta_checks = support_client.describe_trusted_advisor_checks(language='en')
    checks_list = {ctgs: [] for ctgs in list(set([checks['category'] for checks in ta_checks['checks']]))}
    for checks in ta_checks['checks']:
        print('Getting check:' + checks['name'])
        try:
            check_summary = support_client.describe_trusted_advisor_check_summaries(
                            checkIds=[checks['id']])['summaries'][0]
            if check_summary['status'] != 'not_available':
                checks_list[checks['category']].append(
                    [checks['name'], check_summary['status'],
                    str(check_summary['resourcesSummary']['resourcesProcessed']),
                    str(check_summary['resourcesSummary']['resourcesFlagged']),
                    str(check_summary['resourcesSummary']['resourcesSuppressed']),
                    str(check_summary['resourcesSummary']['resourcesIgnored'])])
        except:
            print('Failed to get check: ' + checks['id'] + ' --- ' + checks['name'])
            traceback.print_exc()
            continue
    # print(checks_list

    for catg, chks in OrderedDict(sorted(checks_list.items())).iteritems():
        first_item = True
        for rit in chks:
            if first_item:
                print(catg)
                # email_content += "<tr><th rowspan=" + str(len(checks_list[catg])) + "><a href=\"" \
                #                  + url_path + catg.replace("_", "-") + "\">" + catg.replace("_", " ").title() \
                #                  + "</a></th>"
                first_item = False
            else:
                for i in range(6):
                    print(rit[i])
    # print(email_content)
except:
    print('Failed! Debug further.')
    traceback.print_exc()
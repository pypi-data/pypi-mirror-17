#!/usr/bin/env python
import os
import json
import argparse
from chado import ChadoAuth, ChadoInstance
from tripal import TripalAuth, TripalAnalysis, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads InterPro results into Tripal (requires tripal_analysis_interpro module)')
    TripalAuth(parser)
    TripalAnalysis(parser)
    parser.add_argument('interpro', help='Path to the InterProScan file to load (single XML file, or directory containing multiple XML files)')
    parser.add_argument('--interpro-parameters', help='InterProScan parameters used to produce these results')
    parser.add_argument('--parse-go', action='store_true', help='Load GO terms to the database')
    parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.')
    parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
    parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    params = ti.analysis.getBasePayload(args)

    params.update({
        'type': 'chado_analysis_interpro',
        'interprofile': args.interpro,
        'parsego': 1, # no reason to not launch a job
        'interproparameters': args.interpro_parameters,
        'query_re': args.query_re,
        'query_type': args.query_type,
        'query_uniquename': args.query_uniquename,
    })

    res = ti.analysis.addAnalysis(params)

    print "New Interpro analysis created with ID: %s" % res['nid']

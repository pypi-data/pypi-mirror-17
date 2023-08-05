#!/usr/bin/env python
import os
import json
import argparse
from chado import ChadoAuth, ChadoInstance, Organism, Analysis
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads a fasta file into Tripal')
    TripalAuth(parser)
    parser.add_argument('fasta', help='Path to the fasta file to load')
    parser.add_argument('--job-name', help='Name of the job (default=\'Import FASTA file: <fasta_file_name>\')')
    parser.add_argument('--organism', required=True, help='Organism common name')
    parser.add_argument('--analysis', required=True, help='Analysis name')
    parser.add_argument('--sequence-type', help='Sequence type (default: contig)', default='contig')
    parser.add_argument('--re-name', help='Regular expression for the name', default='')
    parser.add_argument('--re-uniquename', help='Regular expression for the unique name', default='')
    parser.add_argument('--db-ext-id', help='External DB ID', default='')
    parser.add_argument('--re-accession', help='Regular expression for the accession from external DB', default='')
    parser.add_argument('--rel-type', help='Relation type', choices=['part_of', 'derives_from'], default='')
    parser.add_argument('--rel-subject-re', help='Relation subject regular expression (used to extract id of related entity)', default='')
    parser.add_argument('--rel-subject-type', help='Relation subject type (must match already loaded data, e.g. mRNA)', default='')
    parser.add_argument('--method', help='Insertion method', choices=['Insert only', 'Update only', 'Insert and update'], default='Insert and update')
    parser.add_argument('--match-type', help='Match type for already loaded features (used for "Update only" or "Insert and update" methods)', choices=['Name', 'Unique name'], default='Unique name')

    ChadoAuth(parser)
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    ci = ChadoInstance(args.dbhost, args.dbname, args.dbuser, args.dbpass, args.dbschema, args.debug)
    ci.connect()

    # check if the organism exists and get its id
    resdb = ci.session.query(Organism).filter_by(common_name = args.organism)
    if not resdb.count():
        raise Exception("Could not find the organism %s in the database %s" % (args.organism, ci._engine.url))
    organism_id = resdb.one().organism_id

    # check if the analysis exists and get its id
    resdb = ci.session.query(Analysis).filter_by(name = args.analysis)
    if not resdb.count():
        raise Exception("Could not find the analysis %s in the database %s" % (args.analysis, ci._engine.url))
    analysis_id = resdb.one().analysis_id

    job_name = args.job_name
    if not job_name:
        job_name = 'Import FASTA file: %s' % os.path.basename(args.fasta)

    uid = 1 # user id is not really used by the loader, 1 is admin user

    job_args = [args.fasta, organism_id, args.sequence_type, args.re_name, args.re_uniquename, args.re_accession,
                args.db_ext_id, args.rel_type, args.rel_subject_re, args.rel_subject_type,
                args.method, uid, analysis_id, args.match_type]

    r = ti.jobs.addJob(job_name, 'tripal_feature', 'tripal_feature_load_fasta', job_args)
    print 'Load fasta job scheduled with id %s' % r['job_id']

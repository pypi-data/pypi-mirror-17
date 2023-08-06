#!/usr/bin/env python
# encoding: utf-8
'''
editing.filter_reads -- shortdesc

editing.filter_reads is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2016 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import re
from scipy.special import betainc

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2016-07-13'
__updated__ = '2016-07-13'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def rank_edits(alfa, beta, cov_margin, conf_min, eff_file, outfile):
    """
    Step 8: Score editing sites based on coverage and edit % 
    
    * Boyko's confidence scoring using an inverse probability model.
    """
    print("Ranking Editing Sites: {}".format(eff_file))
    def process(line):
        (chr, pos, dot, ref, alt, qual,
         filter, info, format, cond) = line.split("\t")[:10]

        if chr[0] == "#":
            print line,
            return
        
        # retrieve total number of reads mapping to position 
        infos = info.split(";")
        (dp, i16) = infos[:2]
    
        assert dp[:2] == "DP" 
        num_reads = int(dp[3:])    

        """
        # retrieve numbers of A's and G's on forward and reverse strand
        assert i16[:3] == "I16", i16
        (a_fwd, a_rev, g_fwd, g_rev) = (int(x) for x in i16[4:].split(",")[:4])
        print("warning: i16 not available")
        """
        
        dp4 = re.findall("DP4\=([\d\,]+)",info)[0]
    
    
        (a_fwd, a_rev, g_fwd, g_rev) = (int(x) for x in dp4.split(","))
            
        a = a_fwd + a_rev
        g = g_fwd + g_rev
        num_reads = a + g
        edit_frac = g / float(num_reads)
    
        # calc smoothed counts and confidence
        G = g + alfa
        A = a + beta
        theta = G / float(G + A)
    
        ########  MOST IMPORTANT LINE  ########
        # calculates the confidence of theta as
        # P( theta < cov_margin | A, G) ~ Beta_theta(G, A) 
        confidence = 1 - betainc(G, A, cov_margin)
    
        # retrieve genic region found by snpEff
        region = "NoRegion"
        if len(infos) > 2:
            eff = infos[-1]
            if eff[:3] == "EFF":
                regions = set([ region.split("(")[0] \
                               for region in eff[4:].split(",") \
                               if region.split("(")[0] != 'UPSTREAM' \
                               and region.split("(")[0] != 'DOWNSTREAM'] )
                # report only most interesting region for each site:
                priorities = ["SPLICE_SITE_ACCEPTOR", 
                              "SPLICE_SITE_DONOR", 
                              "NON_SYNONYMOUS_CODING", 
                              "SYNONYMOUS_CODING", 
                              "UTR_3_PRIME", 
                              "EXON", 
                              "INTRON", 
                              "UTR_5_PRIME"]
                for x in priorities:
                    if x in regions:
                        region = x
                        break
    
    
        # print line in CONF format
            
        return_string = ("\t".join([chr, pos, str(num_reads), ref, alt, ""]) + \
                        "\t".join(str(round(y,9)) for y in [confidence, theta, edit_frac]) + \
                        "\t".join(["", region, info, format, cond]) + \
                        "\n")
        return confidence, return_string
        
    o = open(outfile, 'w')
    with open(eff_file,'r') as f:
        for eff in f:
            if eff.startswith("\#\#") or eff.startswith("##"):
                pass
            elif eff.startswith("#CHROM"):    # ammend header of EFF file
                line = eff.split("\t")        # to contain extra numeric columns
                sys.stderr.write("\t".join(line))
                line[2] = "NUM_READS"
                line[5] = "EDIT%"
                line.insert(5, "POST_EDIT%")
                line.insert(5, "CONFIDENCE")
                o.write('\t'.join(line))
            else:
                conf, to_string = process(eff)
                if conf > conf_min:
                    o.write(to_string)
    o.close()        
    
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-i", "--input", dest="input_eff", help="variant eff(vcf) file for filtering", required = True)
        parser.add_argument("-o", "--output", dest="output_conf", help="output noSNP (vcf) file with known snps removed.", required = True)
        parser.add_argument("-c", "--cov_margin", dest="cov_margin", help="minimum edit fraction %", required = False, default = 0.01, type = float )
        parser.add_argument("-a", "--alpha", dest="alpha", help="alpha parameter", required = False, default = 0, type = int )
        parser.add_argument("-b", "--beta", dest="beta", help="beta parameter", required = False, default = 0, type = int )
        
        # Process arguments
        args = parser.parse_args()
        input_eff = args.input_eff
        outfile = args.output_conf
        cov_margin = args.cov_margin
        alpha = args.alpha
        beta = args.beta
        
        rank_edits(alpha, beta, cov_margin, 0, input_eff, outfile)
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'editing.filter_reads_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

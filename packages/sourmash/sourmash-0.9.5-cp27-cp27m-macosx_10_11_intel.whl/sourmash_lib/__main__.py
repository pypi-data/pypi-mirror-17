from __future__ import print_function
import sys
import os, os.path
import argparse
import csv

import screed
import sourmash_lib
from sourmash_lib import signature as sig
from sourmash_lib import fig as sourmash_fig

DEFAULT_K = 31
DEFAULT_N = 500


class SourmashCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='work with RNAseq signatures',
                                         usage='''sourmash <command> [<args>]

Commands can be:

   compute <filenames>         Compute signatures for sequences in these files.
   compare <filenames.sig>     Compute distance matrix for given signatures.
   search <query> <against>    Search for matching signatures.
   plot <matrix>               Plot a distance matrix made by 'compare'.

   import_csv                  Import signatures from a CSV file.
.
''')
        parser.add_argument('command')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)

        cmd = getattr(self, args.command)
        print('# running sourmash subcommand: %s' % args.command,
              file=sys.stderr)
        cmd(sys.argv[2:])

    def search(self, args):
        "Search a query sig against one or more signatures; report top match."
        parser = argparse.ArgumentParser()
        parser.add_argument('query')
        parser.add_argument('against', nargs='+')
        parser.add_argument('--threshold', default=0.08, type=float)
        parser.add_argument('-k', '--ksize', default=DEFAULT_K, type=int)
        parser.add_argument('-f', '--force', action='store_true')
        args = parser.parse_args(args)

        # get the query signature
        sl = sig.load_signatures(
            open(args.query, 'r'), select_ksize=args.ksize)
        if len(sl) != 1:
            raise Exception("%d query signatures; need exactly one" % len(sl))
        query = sl[0]

        # get the signatures to query
        print('loading db of signatures from %d files' % len(args.against),
              file=sys.stderr)
        against = []
        for filename in args.against:
            if filename == args.query and not args.force:
                print('excluding query from database (file %s)' % filename,
                      file=sys.stderr)
                continue

            sl = sig.load_signatures(
                open(filename, 'r'), select_ksize=args.ksize)
            for x in sl:
                against.append((x, filename))

        # compute query x db
        distances = []
        for (x, filename) in against:
            distance = query.similarity(x)
            if distance >= args.threshold:
                distances.append((distance, x, filename))

        # any matches? sort, show.
        if distances:
            distances.sort(reverse=True, key = lambda x: x[0])
            print('%d matches:' % len(distances))
            for distance, match, filename in distances[:3]:
                print('\t', match.name(), '\t', "%.3f" % distance,
                      '\t', filename)
        else:
            print('** no matches in %d signatures' % len(against),
                  file=sys.stderr)

    def compute(self, args):
        "Compute the signature for one or more files."
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='+')
        parser.add_argument('--protein', action='store_true')
        parser.add_argument('--input-is-protein', action='store_true')
        parser.add_argument('-k', '--ksizes',
                            default=str(DEFAULT_K),
                            help='comma-separated list of k-mer sizes')
        parser.add_argument('-n', '--num-hashes', type=int,
                            default=DEFAULT_N,
                            help='number of hashes to use in each sketch')
        parser.add_argument('-f', '--force', action='store_true')
        parser.add_argument('-o', '--output', type=argparse.FileType('wt'))
        parser.add_argument('--email', type=str, default='')
        args = parser.parse_args(args)

        print('computing signatures for files:', args.filenames,
              file=sys.stderr)

        # get list of k-mer sizes for which to compute sketches
        ksizes = args.ksizes
        if ',' in ksizes:
            ksizes = ksizes.split(',')
            ksizes = list(map(int, ksizes))
        else:
            ksizes = [int(ksizes)]

        print('Computing signature for ksizes: %s' % str(ksizes),
              file=sys.stderr)

        # for each file, load & compute sketch.
        for filename in args.filenames:
            sigfile = os.path.basename(filename) + '.sig'
            if not args.output and os.path.exists(sigfile) and not args.force:
                print('skipping', filename, '- already done',
                      file=sys.stderr)
                continue

            # one estimator for each ksize
            Elist = []
            for k in ksizes:
                E = sourmash_lib.Estimators(ksize=k, n=args.num_hashes,
                                            protein=args.protein)
                Elist.append(E)

            # consume & calculate signatures
            print('... reading sequences from', filename, file=sys.stderr)
            for n, record in enumerate(screed.open(filename)):
                if n % 10000 == 0 and n:
                    print('...', filename, n, file=sys.stderr)

                s = record.sequence
                for E in Elist:
                    if args.input_is_protein:
                        E.mh.add_protein(s)
                    else:
                        E.add_sequence(s, args.force)

            # convert into a signature
            siglist = [ sig.SourmashSignature(args.email, E,
                        filename=filename) for E in Elist ]

            # save!
            if args.output:
                data = sig.save_signatures(siglist, args.output)
            else:
                with open(sigfile, 'w') as fp:
                    data = sig.save_signatures(siglist, fp)

    def compare(self, args):
        "Compare multiple signature files and create a distance matrix."
        import numpy

        parser = argparse.ArgumentParser()
        parser.add_argument('signatures', nargs='+')
        parser.add_argument('-k', '--ksize', type=int, default=DEFAULT_K)
        parser.add_argument('-o', '--output')
        args = parser.parse_args(args)

        # load in the various signatures
        siglist = []
        for filename in args.signatures:
            print('loading', filename, file=sys.stderr)
            data = open(filename).read()
            loaded = sig.load_signatures(data, select_ksize=args.ksize)
            if not loaded:
                print('warning: no signatures loaded at given ksize from %s' %
                          filename, file=sys.stderr)
            siglist.extend(loaded)

        if len(siglist) == 0:
            print('no signatures!', file=sys.stderr)
            sys.exit(-1)

        # build the distance matrix
        D = numpy.zeros([len(siglist), len(siglist)])
        numpy.set_printoptions(precision=3, suppress=True)

        # do all-by-all calculation
        i = 0
        labeltext = []
        for i, E in enumerate(siglist):
            for j, E2 in enumerate(siglist):
                D[i][j] = E.similarity(E2)

            print('%d-%20s\t%s' % (i, E.name(), D[i, :, ],))
            labeltext.append(E.name())
            i += 1

        print('min similarity in matrix:', numpy.min(D), file=sys.stderr)

        # shall we output a matrix?
        if args.output:
            labeloutname = args.output + '.labels.txt'
            print('saving labels to:', labeloutname, file=sys.stderr)
            with open(labeloutname, 'w') as fp:
                fp.write("\n".join(labeltext))

            print('saving distance matrix to:', args.output,
                  file=sys.stderr)
            with open(args.output, 'wb') as fp:
                numpy.save(fp, D)


    def plot(self, args):
        "Produce a clustering and plot."
        import numpy
        import scipy
        import pylab
        import scipy.cluster.hierarchy as sch

        # set up cmd line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('distances', help="output from 'sourmash compare'")
        parser.add_argument('--pdf', action='store_true')
        parser.add_argument('--labels', action='store_true')
        parser.add_argument('--indices', action='store_false')
        parser.add_argument('--vmax', default=1.0, type=float)
        parser.add_argument('--vmin', default=0.0, type=float)
        args = parser.parse_args(args)

        # load files
        D_filename = args.distances
        labelfilename = D_filename + '.labels.txt'

        D = numpy.load(open(D_filename, 'rb'))
        labeltext = [ x.strip() for x in open(labelfilename) ]

        # build filenames, decide on PDF/PNG output
        dendrogram_out = os.path.basename(D_filename) + '.dendro'
        if args.pdf:
            dendrogram_out += '.pdf'
        else:
            dendrogram_out += '.png'

        matrix_out = os.path.basename(D_filename) + '.matrix'
        if args.pdf:
            matrix_out += '.pdf'
        else:
            matrix_out += '.png'

        ### make the dendrogram:
        fig = pylab.figure(figsize=(8,5))
        ax1 = fig.add_axes([0.1, 0.1, 0.7, 0.8])
        ax1.set_xticks([])
        ax1.set_yticks([])

        Y = sch.linkage(D, method='single') # cluster!
        Z1 = sch.dendrogram(Y, orientation='right', labels=labeltext)
        fig.savefig(dendrogram_out)
        print('wrote', dendrogram_out)

        ### make the dendrogram+matrix:
        fig = sourmash_fig.plot_composite_matrix(D, labeltext,
                                                 show_labels=args.labels,
                                                 show_indices=args.indices,
                                                 vmin=args.vmin,
                                                 vmax=args.vmax)
        fig.savefig(matrix_out)
        print('wrote', matrix_out)

        # print out sample numbering for FYI.
        for i, name in enumerate(labeltext):
            print(i, '\t', name)

    def import_csv(self, args):
        "Import a CSV file full of signatures/hashes."
        p = argparse.ArgumentParser()
        p.add_argument('mash_csvfile')
        p.add_argument('-o', '--output', type=argparse.FileType('wt'),
                       default=sys.stdout)
        p.add_argument('--email', type=str, default='')
        args = p.parse_args(args)

        with open(args.mash_csvfile, 'r') as fp:
            reader = csv.reader(fp)
            siglist = []
            for row in reader:
                hashfn = row[0]
                hashseed = int(row[1])

                # only support a limited import type, for now ;)
                assert hashfn == 'murmur64'
                assert hashseed == 42

                _, _, ksize, name, hashes = row
                ksize = int(ksize)

                hashes = hashes.strip()
                hashes = list(map(int, hashes.split(' ' )))

                e = sourmash_lib.Estimators(len(hashes), ksize)
                for h in hashes:
                    e.mh.add_hash(h)
                s = sig.SourmashSignature(args.email, e, filename=name)
                siglist.append(s)
                print('loaded signature:', name,
                      s.md5sum()[:8], file=sys.stderr)

            print('saving %d signatures to YAML' % (len(siglist),),
                  file=sys.stderr)
            sig.save_signatures(siglist, args.output)

    def dump(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='+')
        parser.add_argument('-k', '--ksize', type=int, default=DEFAULT_K)
        args = parser.parse_args(sys.argv[2:])

        for filename in args.filenames:
            data = open(filename).read()
            print('loading', filename)
            siglist = sig.load_signatures(data, select_ksize=args.ksize)
            assert len(siglist) == 1

            s = siglist[0]

            fp = open(filename + '.dump.txt', 'w')
            fp.write(" ".join((map(str, s.estimator.mh.get_mins()))))
            fp.close()


def main():
    SourmashCommands()
    return 0

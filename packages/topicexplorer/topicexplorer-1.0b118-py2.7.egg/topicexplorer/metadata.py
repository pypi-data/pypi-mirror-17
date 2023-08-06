from ConfigParser import RawConfigParser as ConfigParser

from codecs import open 
import csv
from unidecode import unidecode
from topicexplorer.lib.util import isint, is_valid_configfile, bool_prompt

from vsm.viewer.wrappers import doc_label_name

def parse_metadata_from_csvfile(filename):
    """
    Takes a csvfile where the first column in each row is the label.
    Returns a dictionary of dictionaries where each key is the label,
    and each value is a dictionary of field values.
    """
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        metadata = dict()
        for row in reader:
            metadata[row['article_label']] = row

    return metadata

def extract_metadata(corpus, ctx_type, filename, format='csv'):
    """
    Takes a corpus object, a context_type, and a filename to export
    all metadata to.
    """
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        ctx_index = corpus.context_types.index(ctx_type)

        ctx_data = corpus.context_data[ctx_index]
        writer.writerow(ctx_data.dtype.names)
        for row in ctx_data:
            writer.writerow(row)


def extract_labels(corpus, ctx_type, filename):
    """
    Creates a new csv where each row is a label in the corpus.
    """
    label_name = doc_label_name(ctx_type)
    labels = corpus.view_metadata(ctx_type)[label_name]

    with open(filename, 'w') as outfile:
        outfile.write(label_name + '\n')
        for label in labels:
            outfile.write(label + '\n')


def add_metadata(corpus, ctx_type, new_metadata, force=False):
    import vsm.corpus
    
    # get existing metadata
    i = corpus.context_types.index(ctx_type)
    md = corpus.context_data[i]
    fields = md.dtype.fields.keys()

    # sort new_metadata according to existing md order
    # n.b., this may raise a KeyError - in which case there's not md
    # for each entry - which is the desired error to throw.
    label_name = doc_label_name(ctx_type)
    labels = md[label_name]
    new_data = [new_metadata.get(id, dict()) for id in labels]

    # look for new fields
    new_fields = set()
    for vals in new_metadata.values():
        new_fields.update(vals.keys())

    # differentiate new and updated fields
    updated_fields = new_fields.intersection(fields)
    updated_fields.remove(label_name)
    new_fields = new_fields.difference(fields)
    if None in new_fields:
        new_fields.remove(None)

    # process new fields
    for field in new_fields:
        if force:
            data = [d.get(field, '') for d in new_data]
        else:
            data = [d[field] for d in new_data]
        corpus = vsm.corpus.add_metadata(corpus, ctx_type, field, data)

    # process existing fields
    for field in updated_fields:
        if force:
            data = [d.get(field, '') for d in new_data]
        else:
            data = [d[field] for d in new_data]
        corpus.context_data[i][field] = data

    return corpus


def main(args):
    from vsm.corpus import Corpus

    config = ConfigParser({"htrc": False,
        "sentences": "False"})
    config.read(args.config_file)
    
    args.corpus_path = config.get("main", "corpus_file")
    c = Corpus.load(args.corpus_path)
    
    context_type = config.get('main', 'context_type')

    if args.add:
        metadata = parse_metadata_from_csvfile(args.add)
        c = add_metadata(c, context_type, metadata, force=args.force)
        c.save(args.corpus_path)
    if args.list:
        extract_labels(c, context_type, args.list)
    if args.extract:
        extract_metadata(c, context_type, args.extract)


def populate_parser(parser):
    parser.add_argument("config_file", help="Path to Config",
        type=lambda x: is_valid_configfile(parser, x))
    parser.add_argument("-e", "--extract", help="Extract metadata to file")
    parser.add_argument("-a", "--add", help="Add metadata from file")
    parser.add_argument("-l", "--list", help="List all labels")
    parser.add_argument("-f", "--force", action='store_true', default=False,
        help="Force insertion of blank metadata")


if __name__ == '__main__':
    import argparse
    from argparse import ArgumentParser
    parser = ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    populate_parser(parser)
    args = parser.parse_args()
    
    main(args)


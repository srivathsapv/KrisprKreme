from score_sequence import get_score as score_ontarget
from cfd import calc_cfd as score_offtarget
import json


def parse_chr_name(fa_filepath):
    splits = fa_filepath.split('/')
    filename = splits[len(splits) - 1]
    return filename.split('.')[0]


def get_offtarget_scores(sgrna, putative_sites):
    sites_copy = putative_sites[:]
    for site in sites_copy:
        site['chr'] = parse_chr_name(site['chr_path'])
        site.pop('chr_path', None)

    scored_sites = []
    for dna_site in sites_copy:
        chr_neighbors = [s for s in sites_copy if s['chr'] == dna_site['chr'] and s['id'] != dna_site['id']]

        if len(chr_neighbors) == 0:
            dna_site['off_target'] = 0.0
        else:
            off_target = 0.0
            for neighbor in chr_neighbors:
                off_target += score_offtarget(sgrna, neighbor['sequence'])
            dna_site['off_target'] = round(off_target, 5)

    return sites_copy


def get_ontarget_scores(putative_sites):
    sites_copy = putative_sites[:]

    for site in sites_copy:
        site['on_target'] = score_ontarget(site['sequence'])

    return sites_copy


def rank_putative_sites(sgrna, putative_sites_file, n_sites=10):
    putative_sites = json.loads(open(putative_sites_file, 'r').read())

    sites = get_offtarget_scores(sgrna, putative_sites)
    sites = get_ontarget_scores(sites)

    sites.sort(key=lambda d: d['on_target'])
    return sites[::-1][:n_sites]

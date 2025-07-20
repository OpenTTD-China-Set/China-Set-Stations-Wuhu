#!/usr/bin/env python
import grf
import argparse
from station.lib.docgen import gen_docs
import station.stations.dovemere_1992
import station.stations.dovemere_2018
import station.stations.dovemere_1934
import station.stations.platforms
from station.lib.parameters import parameter_list
from station.lib.idmap import station_idmap

metastations = [
    station.stations.dovemere_2018.the_stations,
    station.stations.dovemere_1992.the_stations,
    station.stations.dovemere_1934.the_stations,
    station.stations.platforms.the_stations,
]


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("station/lang", default_lang_file="english-uk.lng")

    return s


def gen(args):
    s = get_string_manager()
    g = grf.NewGRF(
        grfid=b"\xe5\xbc\x8bs",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        version=19,
        min_compatible_version=14,
        id_map_file="station/id_map.json",
        sprite_cache_path="station/.cache",
        url="https://www.tt-forums.net/viewtopic.php?t=91092",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    parameter_list.add(g, s)
    for metastation in metastations:
        metastation.check_id_uniqueness()
        metastation.remap(station_idmap=station_idmap)
        g.add(metastation)

    g.write("station.grf")


def docs(args):
    gen_docs(get_string_manager(), metastations)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True)

    gen_parser = subparsers.add_parser("gen")
    gen_parser.set_defaults(func=gen)

    doc_parser = subparsers.add_parser("doc")
    doc_parser.set_defaults(func=docs)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

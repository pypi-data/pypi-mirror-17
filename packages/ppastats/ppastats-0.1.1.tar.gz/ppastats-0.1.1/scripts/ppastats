#!/usr/bin/env python
"""
Gets download stats for personal package archives (PPA) from Launchpad for Ubuntu
"""
from __future__ import print_function
import argparse
from launchpadlib.launchpad import Launchpad
from six import string_types

__AUTHOR__ = "Matthew Peveler"
__VERSION__ = "0.1.1"


def generate_parser():
    """
    Generate argument parser to be used by the ppastats library.
    :return: argument parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(prog='ppastats',
                                     description='Get statistics for personal package archives'
                                                 '(PPA) for any Ubuntu release/architecture')

    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + __VERSION__,
                        help='Display the version of ppastats')
    parser.add_argument('-r', '--release', nargs='+',
                        help='Releases to get PPA for. This is the first word of the release, such'
                             'as "trusty" or "vivid". Additionally, a version number can be given'
                             '(14.04) and this will be translated to the proper release name.'
                             'Defaults to trusty.', default='trusty')
    parser.add_argument('-a', '--arch', nargs='+',
                        help='Architecture to consider (amd64 or i386). Defaults to amd64.',
                        default='amd64')
    parser.add_argument('ppa', nargs='+', help='PPAs to get stats for. Should be in the format of '
                                               '"owner:package" (ex: ondrej:php).')
    return parser


def get_stats(releases, archs, ppas):
    """
    Prints out the stats for the ppa to the console
    :param releases:
    :param archs:
    :param ppas:
    :return:
    """
    lp_login = Launchpad.login_anonymously('ppastats', 'edge', "~/.launchpadlib/cache/",
                                           version='devel')  # Login into Launchpad Anoymously
    for ppa in ppas:
        ppa = ppa.split("/")
        ppa_owner = ppa[0]
        ppa_name = ppa[1]
        owner = lp_login.people[ppa_owner]  # PPA owner
        ppa_archive = owner.getPPAByName(name=ppa_name)  # PPA name
        for release in releases:
            for arch in archs:
                distro = 'https://api.launchpad.net/devel/ubuntu/' + release + '/' + arch
                print('Download stats for ' + str(ppa_owner) + '/' + str(ppa_name) + ' PPA')
                print('----------------------------------------------')
                print('')
                print(release + ' ' + arch + ' builds:')
                print('---------------')
                for archive in ppa_archive.getPublishedBinaries(status='Published',
                                                                distro_arch_series=distro):

                    # Write the package name, version and download count to the log file
                    print("{: <40}\t{: <40}\t{:d}".format(archive.binary_package_name,
                                                          archive.binary_package_version,
                                                          archive.getDownloadCount()))


def main():
    """
    Main program execution
    """
    parser = generate_parser()
    args = parser.parse_args()

    if isinstance(args.release, string_types):
        args.release = [args.release]
    if isinstance(args.arch, string_types):
        args.arch = [args.arch]
    get_stats(args.release, args.arch, args.ppa)

if __name__ == "__main__":
    main()

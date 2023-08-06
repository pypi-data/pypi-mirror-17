#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import division, unicode_literals
import argparse
import os
import re
import logging
import multiprocessing
import sys
import datetime
from collections import OrderedDict
import glob
import shutil
import subprocess
import itertools
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
from six.moves import input

from tabulate import tabulate, tabulate_formats

from monty.serialization import loadfn, dumpfn
from pymatgen import Structure, SETTINGS_FILE
from pymatgen.io.vasp import Outcar, Vasprun, Chgcar, Incar
from pymatgen.apps.borg.hive import SimpleVaspToComputedEntryDrone, \
    VaspToComputedEntryDrone
from pymatgen.apps.borg.queen import BorgQueen
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.io.vasp import Poscar
from pymatgen.io.cif import CifParser, CifWriter
from pymatgen.io.vasp.sets import MPRelaxSet, MITRelaxSet
from pymatgen.io.cssr import Cssr
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.alchemy.materials import TransformedStructure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

"""
A master convenience script with many tools for vasp and structure analysis.
"""

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "4.0"
__maintainer__ = "Shyue Ping Ong"
__email__ = "ongsp@ucsd.edu"
__date__ = "Aug 13 2016"


SAVE_FILE = "vasp_data.gz"


def configure(args):
    d = {}
    if os.path.exists(args.output_file):
        d = loadfn(args.output_file)
    toks = args.var_spec
    if len(toks) % 2 != 0:
        print("Bad variable specification!")
        sys.exit(-1)
    for i in range(int(len(toks) / 2)):
        d[toks[2 * i]] = toks[2 * i + 1]
    dumpfn(d, args.output_file, default_flow_style=False)


def get_energies(rootdir, reanalyze, verbose, detailed, sort, fmt):
    """
    Doc string.
    """
    if verbose:
        logformat = "%(relativeCreated)d msecs : %(message)s"
        logging.basicConfig(level=logging.INFO, format=logformat)

    if not detailed:
        drone = SimpleVaspToComputedEntryDrone(inc_structure=True)
    else:
        drone = VaspToComputedEntryDrone(inc_structure=True,
                                         data=["filename",
                                               "initial_structure"])

    ncpus = multiprocessing.cpu_count()
    logging.info("Detected {} cpus".format(ncpus))
    queen = BorgQueen(drone, number_of_drones=ncpus)
    if os.path.exists(SAVE_FILE) and not reanalyze:
        msg = "Using previously assimilated data from {}.".format(SAVE_FILE) \
            + " Use -r to force re-analysis."
        queen.load_data(SAVE_FILE)
    else:
        if ncpus > 1:
            queen.parallel_assimilate(rootdir)
        else:
            queen.serial_assimilate(rootdir)
        msg = "Analysis results saved to {} for faster ".format(SAVE_FILE) + \
              "subsequent loading."
        queen.save_data(SAVE_FILE)

    entries = queen.get_data()
    if sort == "energy_per_atom":
        entries = sorted(entries, key=lambda x: x.energy_per_atom)
    elif sort == "filename":
        entries = sorted(entries, key=lambda x: x.data["filename"])

    all_data = []
    for e in entries:
        if not detailed:
            delta_vol = "{:.2f}".format(e.data["delta_volume"] * 100)
        else:
            delta_vol = e.structure.volume / \
                e.data["initial_structure"].volume - 1
            delta_vol = "{:.2f}".format(delta_vol * 100)
        all_data.append((e.data["filename"].replace("./", ""),
                         re.sub("\s+", "", e.composition.formula),
                         "{:.5f}".format(e.energy),
                         "{:.5f}".format(e.energy_per_atom),
                         delta_vol))
    if len(all_data) > 0:
        headers = ("Directory", "Formula", "Energy", "E/Atom", "% vol chg")
        print(tabulate(all_data, headers=headers, tablefmt=fmt))
        print("")
        print(msg)
    else:
        print("No valid vasp run found.")


def get_magnetizations(mydir, ion_list):
    data = []
    max_row = 0
    for (parent, subdirs, files) in os.walk(mydir):
        for f in files:
            if re.match("OUTCAR*", f):
                try:
                    row = []
                    fullpath = os.path.join(parent, f)
                    outcar = Outcar(fullpath)
                    mags = outcar.magnetization
                    mags = [m["tot"] for m in mags]
                    all_ions = list(range(len(mags)))
                    row.append(fullpath.lstrip("./"))
                    if ion_list:
                        all_ions = ion_list
                    for ion in all_ions:
                        row.append(str(mags[ion]))
                    data.append(row)
                    if len(all_ions) > max_row:
                        max_row = len(all_ions)
                except:
                    pass

    for d in data:
        if len(d) < max_row + 1:
            d.extend([""] * (max_row + 1 - len(d)))
    headers = ["Filename"]
    for i in range(max_row):
        headers.append(str(i))
    print(tabulate(data, headers))


def plot_dos(args):
    v = Vasprun(args.filename[0])
    dos = v.complete_dos

    all_dos = OrderedDict()
    all_dos["Total"] = dos

    structure = v.final_structure

    if args.site:
        for i in range(len(structure)):
            site = structure[i]
            all_dos["Site " + str(i) + " " + site.specie.symbol] = \
                dos.get_site_dos(site)

    if args.element:
        syms = [tok.strip() for tok in args.element[0].split(",")]
        all_dos = {}
        for el, dos in dos.get_element_dos().items():
            if el.symbol in syms:
                all_dos[el] = dos
    if args.orbital:
        all_dos = dos.get_spd_dos()

    plotter = DosPlotter()
    plotter.add_dos_dict(all_dos)
    if args.file:
        plotter.get_plot().savefig(args.file[0])
    else:
        plotter.show()


def plot_chgint(args):
    chgcar = Chgcar.from_file(args.filename[0])
    s = chgcar.structure

    if args.inds:
        atom_ind = [int(i) for i in args.inds[0].split(",")]
    else:
        finder = SpacegroupAnalyzer(s, symprec=0.1)
        sites = [sites[0] for sites in
                 finder.get_symmetrized_structure().equivalent_sites]
        atom_ind = [s.sites.index(site) for site in sites]

    from pymatgen.util.plotting_utils import get_publication_quality_plot
    plt = get_publication_quality_plot(12, 8)
    for i in atom_ind:
        d = chgcar.get_integrated_diff(i, args.radius, 30)
        plt.plot(d[:, 0], d[:, 1],
                 label="Atom {} - {}".format(i, s[i].species_string))
    plt.legend(loc="upper left")
    plt.xlabel("Radius (A)")
    plt.ylabel("Integrated charge (e)")
    plt.tight_layout()
    plt.show()


def parse_vasp(args):

    default_energies = not (args.get_energies or args.ion_list)

    if args.get_energies or default_energies:
        for d in args.directories:
            get_energies(d, args.reanalyze, args.verbose,
                         args.detailed, args.sort[0], args.format)
    if args.ion_list:
        if args.ion_list[0] == "All":
            ion_list = None
        else:
            (start, end) = [int(i) for i in re.split("-", args.ion_list[0])]
            ion_list = list(range(start, end + 1))
        for d in args.directories:
            get_magnetizations(d, ion_list)


def convert_fmt(args):
    iformat = args.input_format[0]
    oformat = args.output_format[0]
    filename = args.input_filename[0]
    out_filename = args.output_filename[0]

    try:

        if iformat == "POSCAR":
            p = Poscar.from_file(filename)
            structure = p.structure
        elif iformat == "CIF":
            r = CifParser(filename)
            structure = r.get_structures()[0]
        elif iformat == "CONVENTIONAL_CIF":
            r = CifParser(filename)
            structure = r.get_structures(primitive=False)[0]
        elif iformat == "CSSR":
            structure = Cssr.from_file(filename).structure
        else:
            structure = Structure.from_file(filename)

        if oformat == "smart":
            structure.to(filename=out_filename)
        elif oformat == "POSCAR":
            p = Poscar(structure)
            p.write_file(out_filename)
        elif oformat == "CIF":
            w = CifWriter(structure)
            w.write_file(out_filename)
        elif oformat == "CSSR":
            c = Cssr(structure)
            c.write_file(out_filename)
        elif oformat == "VASP":
            ts = TransformedStructure(
                structure, [],
                history=[{"source": "file",
                          "datetime": str(datetime.datetime.now()),
                          "original_file": open(filename).read()}])
            ts.write_vasp_input(MPRelaxSet, output_dir=out_filename)
        elif oformat == "MITVASP":
            ts = TransformedStructure(
                structure, [],
                history=[{"source": "file",
                          "datetime": str(datetime.datetime.now()),
                          "original_file": open(filename).read()}])
            ts.write_vasp_input(MITRelaxSet, output_dir=out_filename)

    except Exception as ex:
        print("Error converting file. Are they in the right format?")
        print(str(ex))


def parse_symmetry(args):

    tolerance = float(args.tolerance[0])

    for filename in args.filenames:
        s = Structure.from_file(filename)
        if args.spacegroup:
            finder = SpacegroupAnalyzer(s, tolerance)
            dataset = finder.get_symmetry_dataset()
            print(filename)
            print("Spacegroup  : {}".format(dataset["international"]))
            print("Int number  : {}".format(dataset["number"]))
            print("Hall symbol : {}".format(dataset["hall"]))
            print("")


def analyze_structure(args):
    bonds = {}
    for bond in args.localenv:
        toks = bond.split("=")
        species = toks[0].split("-")
        bonds[(species[0], species[1])] = float(toks[1])
    for filename in args.filenames:
        print("Analyzing %s..." % filename)
        data = []
        s = Structure.from_file(filename)
        for i, site in enumerate(s):
            for species, dist in bonds.items():
                if species[0] in [sp.symbol
                                  for sp in site.species_and_occu.keys()]:
                    dists = [d for nn, d in s.get_neighbors(site, dist)
                             if species[1] in
                             [sp.symbol for sp in nn.species_and_occu.keys()]]
                    dists = ", ".join(["%.3f" % d for d in sorted(dists)])
                    data.append([i, species[0], species[1], dists])
        print(tabulate(data, headers=["#", "Center", "Ligand", "Dists"]))


def parse_view(args):
    from pymatgen.vis.structure_vtk import StructureVis
    excluded_bonding_elements = args.exclude_bonding[0].split(",") \
        if args.exclude_bonding else []
    s = Structure.from_file(args.filename[0])
    vis = StructureVis(excluded_bonding_elements=excluded_bonding_elements)
    vis.set_structure(s)
    vis.show()


def compare_structures(args):
    filenames = args.filenames
    if len(filenames) < 2:
        print("You need more than one structure to compare!")
        sys.exit(-1)
    try:
        structures = [Structure.from_file(fn) for fn in filenames]
    except Exception as ex:
        print("Error converting file. Are they in the right format?")
        print(str(ex))
        sys.exit(-1)

    from pymatgen.analysis.structure_matcher import StructureMatcher, \
        ElementComparator
    m = StructureMatcher() if args.oxi \
        else StructureMatcher(comparator=ElementComparator())
    for i, grp in enumerate(m.group_structures(structures)):
        print("Group {}: ".format(i))
        for s in grp:
            print("- {} ({})".format(filenames[structures.index(s)],
                                     s.formula))
        print()


def generate_files(args):
    from pymatgen.io.vasp.inputs import Potcar
    if args.symbols:
        try:
            p = Potcar(args.symbols, functional=args.functional)
            p.write_file("POTCAR")
        except Exception as ex:
            print("An error has occurred: {}".format(str(ex)))

    else:
        print("No valid options selected.")


def generate_diffraction_plot(args):
    s = Structure.from_file(args.filenames[0])
    c = XRDCalculator()
    if args.outfile:
        c.get_xrd_plot(s).savefig(args.outfile[0])
    else:
        c.show_xrd_plot(s)


def setup_potcars(pspdir, targetdir):
    try:
        os.makedirs(targetdir)
    except OSError:
        r = input("Destination directory exists. Continue (y/n)? ")
        if r != "y":
            print("Exiting ...")
            sys.exit(0)

    print("Generating pymatgen resources directory...")

    name_mappings = {
        "potpaw_PBE": "POT_GGA_PAW_PBE",
        "potpaw_PBE_52": "POT_GGA_PAW_PBE_52",
        "potpaw_PBE_54": "POT_GGA_PAW_PBE_54",
        "potpaw_PBE.52": "POT_GGA_PAW_PBE_52",
        "potpaw_PBE.54": "POT_GGA_PAW_PBE_54",
        "potpaw_LDA": "POT_LDA_PAW",
        "potpaw_LDA.52": "POT_LDA_PAW_52",
        "potpaw_LDA.54": "POT_LDA_PAW_54",
        "potpaw_LDA_52": "POT_LDA_PAW_52",
        "potpaw_LDA_54": "POT_LDA_PAW_54",
        "potUSPP_LDA": "POT_LDA_US",
        "potpaw_GGA": "POT_GGA_PAW_PW91",
        "potUSPP_GGA": "POT_GGA_US_PW91"
    }

    for (parent, subdirs, files) in os.walk(pspdir):
        basename = os.path.basename(parent)
        basename = name_mappings.get(basename, basename)
        for subdir in subdirs:
            filenames = glob.glob(os.path.join(parent, subdir, "POTCAR*"))
            if len(filenames) > 0:
                try:
                    basedir = os.path.join(targetdir, basename)
                    if not os.path.exists(basedir):
                        os.makedirs(basedir)
                    fname = filenames[0]
                    dest = os.path.join(basedir, os.path.basename(fname))
                    shutil.copy(fname, dest)
                    ext = fname.split(".")[-1]
                    if ext.upper() in ["Z", "GZ"]:
                        subprocess.Popen(["gunzip", dest]).communicate()
                    elif ext.upper() in ["BZ2"]:
                        subprocess.Popen(["bunzip2", dest]).communicate()
                    if subdir == "Osmium":
                        subdir = "Os"
                    dest = os.path.join(basedir, "POTCAR.{}".format(subdir))
                    shutil.move(os.path.join(basedir, "POTCAR"), dest)
                    subprocess.Popen(["gzip", "-f", dest]).communicate()
                except Exception as ex:
                    print("An error has occured. Message is %s. Trying to "
                          "continue... " % str(ex))

    print("")
    print("PSP resources directory generated. It is recommended that you "
          "run 'pmg config --add VASP_PSP_DIR %s'" % os.path.abspath(targetdir))
    print("Start a new terminal to ensure that your environment variables "
          "are properly set.")


def build_enum(fortran_command="gfortran"):
    currdir = os.getcwd()
    state = True
    try:
        subprocess.call(["git", "clone",
                         "https://github.com/msg-byu/enumlib.git"])
        subprocess.call(["git", "clone",
                         "https://github.com/msg-byu/symlib.git"])
        os.chdir(os.path.join(currdir, "symlib", "src"))
        os.environ["F90"] = fortran_command
        subprocess.call(["make"])
        enumpath = os.path.join(currdir, "enumlib", "src")
        os.chdir(enumpath)
        subprocess.call(["make"])
        for f in ["enum.x", "makestr.x"]:
            subprocess.call(["make", f])
            shutil.copy(f, os.path.join("..", ".."))
    except Exception as ex:
        print(str(ex))
        state = False
    finally:
        os.chdir(currdir)
        shutil.rmtree("enumlib")
        shutil.rmtree("symlib")
    return state


def build_bader(fortran_command="gfortran"):
    bader_url = "http://theory.cm.utexas.edu/henkelman/code/bader/download/bader.tar.gz"
    currdir = os.getcwd()
    state = True
    try:
        urlretrieve(bader_url, "bader.tar.gz")
        subprocess.call(["tar", "-zxf", "bader.tar.gz"])
        os.chdir("bader")
        subprocess.call(
            ["cp", "makefile.osx_" + fortran_command, "makefile"])
        subprocess.call(["make"])
        shutil.copy("bader", os.path.join("..", "bader_exe"))
        os.chdir("..")
        shutil.rmtree("bader")
        os.remove("bader.tar.gz")
        shutil.move("bader_exe", "bader")
    except Exception as ex:
        print(str(ex))
        state = False
    finally:
        os.chdir(currdir)
    return state


def setup_pmg(args):
    if args.potcar_dirs:
        pspdir, targetdir = [os.path.abspath(d) for d in args.potcar_dirs]
        setup_potcars(pspdir, targetdir)
    elif args.install:
        try:
            subprocess.call(["ifort", "--version"])
            print("Found ifort")
            fortran_command = "ifort"
        except:
            try:
                subprocess.call(["gfortran", "--version"])
                print("Found gfortran")
                fortran_command = "gfortran"
            except Exception as ex:
                print(str(ex))
                print("No fortran compiler found.")
                sys.exit(-1)

        enum = None
        bader = None
        if args.install == "enum":
            print("Building enumlib")
            enum = build_enum(fortran_command)
            print("")
        elif args.install == "bader":
            print("Building bader")
            bader = build_bader(fortran_command)
            print("")
        if bader or enum:
            print("Please add {} to your PATH or move the executables multinum.x, "
                  "makestr.x and/or bader to a location in your PATH."
                  .format(os.path.abspath(".")))
            print("")


def diff_incar(args):
    filepath1 = args.filenames[0]
    filepath2 = args.filenames[1]
    incar1 = Incar.from_file(filepath1)
    incar2 = Incar.from_file(filepath2)

    def format_lists(v):
        if isinstance(v, (tuple, list)):
            return " ".join(["%d*%.2f" % (len(tuple(group)), i)
                             for (i, group) in itertools.groupby(v)])
        return v

    d = incar1.diff(incar2)
    output = [['SAME PARAMS', '', ''], ['---------------', '', ''],
              ['', '', ''], ['DIFFERENT PARAMS', '', ''],
              ['----------------', '', '']]
    output.extend([(k, format_lists(d['Same'][k]), format_lists(d['Same'][k]))
                   for k in sorted(d['Same'].keys()) if k != "SYSTEM"])
    output.extend([(k, format_lists(d['Different'][k]['INCAR1']),
                    format_lists(d['Different'][k]['INCAR2']))
                   for k in sorted(d['Different'].keys()) if k != "SYSTEM"])
    print(tabulate(output, headers=['', filepath1, filepath2]))


def main():
    parser = argparse.ArgumentParser(description="""
    pmg is a convenient script that uses pymatgen to perform many
    analyses, plotting and format conversions. This script works based on
    several sub-commands with their own options. To see the options for the
    sub-commands, type "pmg sub-command -h".""",
                                     epilog="""
    Author: Shyue Ping Ong
    Version: {}
    Last updated: {}""".format(__version__, __date__))

    subparsers = parser.add_subparsers()

    parser_setup = subparsers.add_parser("setup", help="Setup pymatgen.")
    parser_setup.add_argument("-p", "--potcar",
                              dest="potcar_dirs", type=str, nargs=2,
                              help="Initial directory where downloaded VASP "
                                   "POTCARs are extracted to, and the "
                                   "output directory where the reorganized "
                                   "potcars will be stored. The input "
                                   "directory should be "
                                   "the parent directory that contains the "
                                   "POT_GGA_PAW_PBE or potpaw_PBE type "
                                   "subdirectories.")
    parser_setup.add_argument("-i", "--install",
                              dest="install", type=str,
                              choices=["enum", "bader"],
                              help="Install various optional command line "
                                   "tools needed for full functionality.")
    parser_setup.set_defaults(func=setup_pmg)

    parser_config = subparsers.add_parser("config", help="Tools for "
                                                        "configuration file "
                                                        ".pmgrc.yaml")
    parser_config.add_argument("-a", "--add",
                               dest="var_spec", type=str,
                               required=True, nargs="+",
                               help="Variables to add in the form of space "
                                    "separated key value pairs. E.g., "
                                    "VASP_PSP_DIR ~/psps")
    parser_config.add_argument("-o", "--output_file",
                               dest="output_file", type=str,
                               default=SETTINGS_FILE,
                               help="Output file to write the config to. "
                                    "Defaults to standard config file "
                                    "location in ~/.pmgrc.yaml. Use this if "
                                    "you just want to see the file first.")
    parser_config.set_defaults(func=configure)

    parser_vasp = subparsers.add_parser("analyze", help="Vasp run analysis.")
    parser_vasp.add_argument("directories", metavar="dir", default=".",
                             type=str, nargs="*",
                             help="directory to process (default to .)")
    parser_vasp.add_argument("-e", "--energies", dest="get_energies",
                             action="store_true", help="Print energies")
    parser_vasp.add_argument("-m", "--mag", dest="ion_list", type=str, nargs=1,
                             help="Print magmoms. ION LIST can be a range "
                             "(e.g., 1-2) or the string 'All' for all ions.")
    parser_vasp.add_argument("-r", "--reanalyze", dest="reanalyze",
                             action="store_true",
                             help="Force reanalysis. Typically, vasp_analyzer"
                             " will just reuse a vasp_analyzer_data.gz if "
                             "present. This forces the analyzer to reanalyze "
                             "the data.")
    parser_vasp.add_argument("-f", "--format", dest="format",
                             choices=tabulate_formats, default="simple",
                             type=str,
                             help="Format for table. Supports all options in "
                                  "tabulate package.")
    parser_vasp.add_argument("-v", "--verbose", dest="verbose",
                             action="store_true",
                             help="verbose mode. Provides detailed output on "
                             "progress.")
    parser_vasp.add_argument("-d", "--detailed", dest="detailed",
                             action="store_true",
                             help="Detailed mode. Parses vasprun.xml instead "
                             "of separate vasp input. Slower.")
    parser_vasp.add_argument("-s", "--sort", dest="sort", type=str, nargs=1,
                             default=["energy_per_atom"],
                             help="Sort criteria. Defaults to energy / atom.")
    parser_vasp.set_defaults(func=parse_vasp)

    parser_plot = subparsers.add_parser("plotdos", help="Plotting for dos.")
    parser_plot.add_argument("filename", metavar="filename", type=str, nargs=1,
                             help="vasprun.xml file to plot")
    parser_plot.add_argument("-s", "--site", dest="site", action="store_const",
                             const=True, help="Plot site projected DOS")
    parser_plot.add_argument("-e", "--element", dest="element", type=str,
                             nargs=1,
                             help="List of elements to plot as comma-separated"
                             " values e.g., Fe,Mn")
    parser_plot.add_argument("-o", "--orbital", dest="orbital",
                             action="store_const", const=True,
                             help="Plot orbital projected DOS")
    parser_plot.add_argument("-f", "--file", dest="file", type=str, nargs=1,
                             help="Save to file.")
    parser_plot.set_defaults(func=plot_dos)

    parser_plotchg = subparsers.add_parser("plotchgint",
                                           help="Plotting for the charge "
                                                "integration.")
    parser_plotchg.add_argument("filename", metavar="filename", type=str,
                                nargs=1, help="CHGCAR file to plot")
    parser_plotchg.add_argument("-i", "--indices", dest="inds", type=str,
                                nargs=1,
                                help="Comma-separated list of indices to plot"
                                     ", e.g., 1,2,3,4. If not provided, "
                                     "the code will plot the chgint for all "
                                     "symmetrically distinct atoms detected.")
    parser_plotchg.add_argument("-r", "--radius", dest="radius", type=float,
                                default=3,
                                help="Radius of integration.")
    parser_plotchg.set_defaults(func=plot_chgint)

    parser_convert = subparsers.add_parser(
        "convert", help="File format conversion tools.")
    parser_convert.add_argument("input_filename", metavar="input_filename",
                                type=str, nargs=1, help="Input filename.")
    parser_convert.add_argument("output_filename", metavar="output_filename",
                                type=str, nargs=1,
                                help="Output filename (for POSCAR/CIF/CSSR "
                                "output) / dirname (VASP output)")
    parser_convert.add_argument("-i", "--input", dest="input_format",
                                type=str.upper,
                                nargs=1,
                                choices=["POSCAR", "CIF", "CSSR", "smart",
                                         "CONVENTIONAL_CIF"],
                                default=["smart"],
                                help="Input file format. By default, smart is "
                                "selected, which guesses the format from the "
                                "filename. Other formats can be enforced as "
                                "needed. If CONVENTIONAL_CIF is chosen instead "
                                "of CIF, no primitive cell reduction is done.")

    parser_convert.add_argument("-o", "--output", dest="output_format",
                                type=str.upper, nargs=1,
                                choices=["POSCAR", "CIF", "CSSR", "VASP",
                                         "MITVASP",
                                         "smart"],
                                default=["smart"],
                                help="Output file format. By default, smart is"
                                " selected, which guesses the format from the "
                                "filename. Other formats can be enforced as "
                                "needed. VASP is a special output form, which "
                                "outputs a set of VASP input files to a "
                                "directory. MITVASP uses the MIT input set "
                                "instead of the default Materials project "
                                "input set.")
    parser_convert.set_defaults(func=convert_fmt)

    parser_symm = subparsers.add_parser("symm", help="Symmetry tools.")
    parser_symm.add_argument("filenames", metavar="filenames", type=str,
                             nargs="+",
                             help="Filenames to determine symmetry.")
    parser_symm.add_argument("-t", "--tolerance", dest="tolerance", type=float,
                             nargs=1, default=[0.1],
                             help="Tolerance for symmetry determination")
    parser_symm.add_argument("-s", "--spacegroup", dest="spacegroup",
                             action="store_true",
                             help="Determine symmetry")
    parser_symm.set_defaults(func=parse_symmetry)

    parser_view = subparsers.add_parser("view", help="Visualize structures")
    parser_view.add_argument("filename", metavar="filename", type=str,
                             nargs=1, help="Filename")
    parser_view.add_argument("-e", "--exclude_bonding", dest="exclude_bonding",
                             type=str, nargs=1,
                             help="List of elements to exclude from bonding "
                             "analysis. E.g., Li,Na")
    parser_view.set_defaults(func=parse_view)

    parser_cmp = subparsers.add_parser("compare", help="Compare structures")
    parser_cmp.add_argument("filenames", metavar="filenames", type=str,
                            nargs="*", help="List of filenames to compare.")
    parser_cmp.add_argument("-o", "--oxi", dest="oxi",
                            action="store_true",
                            help="Oxi mode means that different oxidation "
                                 "states will not match to each other, i.e.,"
                                 " Fe2+ amd Fe3+ will be treated as "
                                 "different species for the purposes of "
                                 "matching.")
    parser_cmp.set_defaults(func=compare_structures)

    parser_diffincar = subparsers.add_parser(
        "diff_incar", help="Helpful diffing tool for INCARs")
    parser_diffincar.add_argument("filenames", metavar="filenames", type=str,
                            nargs=2, help="List of INCARs to compare.")
    parser_diffincar.set_defaults(func=diff_incar)

    parser_generate = subparsers.add_parser("generate",
                                            help="Generate input files")
    parser_generate.add_argument("-f", "--functional", dest="functional",
                                 type=str,
                                 choices=["LDA", "PBE", "PW91", "LDA_US"],
                                 default="PBE",
                                 help="Functional to use. Unless otherwise "
                                      "stated (e.g., US), "
                                      "refers to PAW psuedopotential.")
    parser_generate.add_argument("-p", "--potcar", dest="symbols",
                                 type=str, nargs="+", required=True,
                                 help="List of POTCAR symbols. Use -f to set "
                                      "functional. Defaults to PBE.")
    parser_generate.set_defaults(func=generate_files)

    parser_structure = subparsers.add_parser(
        "structure",
        help="Structure analysis tools.")
    parser_structure.add_argument(
        "filenames", metavar="filenames", type=str, nargs="+",
        help="List of input structure files to analyze.")
    parser_structure.add_argument(
        "-l", "--localenv", dest="localenv", type=str, nargs="+",
        help="Local environment analysis. Provide bonds in the format of"
             "Center Species-Ligand Species=max_dist, e.g., H-O=0.5.")
    parser_structure.set_defaults(func=analyze_structure)

    parser_diffraction = subparsers.add_parser(
        "diffraction",
        help="Generate diffraction plots. Current supports XRD only.")
    parser_diffraction.add_argument(
        "filenames", metavar="filenames", type=str, nargs=1,
        help="List of input structure files to generate diffraction plot.")
    parser_diffraction.add_argument(
        "-o", "--output_filename", dest="outfile", type=str, nargs=1,
        help="Save to file given by filename.")
    parser_diffraction.set_defaults(func=generate_diffraction_plot)

    args = parser.parse_args()

    try:
        getattr(args, "func")
    except AttributeError:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()

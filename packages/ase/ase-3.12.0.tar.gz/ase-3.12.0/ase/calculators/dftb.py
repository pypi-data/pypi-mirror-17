"""This module defines an ASE interface to DftbPlus

http://http://www.dftb-plus.info//
http://www.dftb.org/

markus.kaukonen@iki.fi

The file 'geom.out.gen' contains the input and output geometry
and it will be updated during the dftb calculations.

If restart == None
                   it is assumed that a new input file 'dftb_hsd.in'
                   will be written by ase using default keywords
                   and the ones given by the user.

If restart != None
                   it is assumed that keywords are in file restart

The keywords are given, for instance, as follows::

    Hamiltonian_SCC ='YES',
    Hamiltonian_SCCTolerance = 1.0E-008,
    Hamiltonian_MaxAngularMomentum = '',
    Hamiltonian_MaxAngularMomentum_O = '"p"',
    Hamiltonian_MaxAngularMomentum_H = '"s"',
    Hamiltonian_InitialCharges_ = '',
    Hamiltonian_InitialCharges_AllAtomCharges_ = '',
    Hamiltonian_InitialCharges_AllAtomCharges_1 = -0.88081627,
    Hamiltonian_InitialCharges_AllAtomCharges_2 = 0.44040813,
    Hamiltonian_InitialCharges_AllAtomCharges_3 = 0.44040813,

"""

import os

import numpy as np

from ase.units import Hartree, Bohr
from ase.calculators.calculator import FileIOCalculator, kpts2mp


class Dftb(FileIOCalculator):
    """ A dftb+ calculator with ase-FileIOCalculator nomenclature
    """
    if 'DFTB_COMMAND' in os.environ:
        command = os.environ['DFTB_COMMAND'] + ' > PREFIX.out'
    else:
        command = 'dftb+ > PREFIX.out'

    implemented_properties = ['energy', 'forces', 'stress']

    def __init__(self, restart=None, ignore_bad_restart_file=False,
                 label='dftb', atoms=None, kpts=None,
                 run_manyDftb_steps=False,
                 **kwargs):
        """Construct a DFTB+ calculator.
        """

        from ase.dft.kpoints import monkhorst_pack

        if 'DFTB_PREFIX' in os.environ:
            slako_dir = os.environ['DFTB_PREFIX']
        else:
            slako_dir = './'

        # to run Dftb as energy and force calculator use
        # Driver_MaxSteps=0,
        if run_manyDftb_steps:
            # minimisation of molecular dynamics is run by native DFTB+
            self.default_parameters = dict(
                Hamiltonian_='DFTB',
                Hamiltonian_SlaterKosterFiles_='Type2FileNames',
                Hamiltonian_SlaterKosterFiles_Prefix=slako_dir,
                Hamiltonian_SlaterKosterFiles_Separator='"-"',
                Hamiltonian_SlaterKosterFiles_Suffix='".skf"'
                )
        else:
            # using ase to get forces and energy only
            # (single point calculation)
            self.default_parameters = dict(
                Hamiltonian_='DFTB',
                Driver_='ConjugateGradient',
                Driver_MaxForceComponent='1E-4',
                Driver_MaxSteps=0,
                Hamiltonian_SlaterKosterFiles_='Type2FileNames',
                Hamiltonian_SlaterKosterFiles_Prefix=slako_dir,
                Hamiltonian_SlaterKosterFiles_Separator='"-"',
                Hamiltonian_SlaterKosterFiles_Suffix='".skf"'
            )

        FileIOCalculator.__init__(self, restart, ignore_bad_restart_file,
                                  label, atoms, **kwargs)

        self.kpts = kpts
        # kpoint stuff by ase
        if self.kpts is not None:
            mpgrid = kpts2mp(atoms, self.kpts)
            mp = monkhorst_pack(mpgrid)
            initkey = 'Hamiltonian_KPointsAndWeights'
            self.parameters[initkey + '_'] = ''
            for i, imp in enumerate(mp):
                key = initkey + '_empty' + str(i)
                self.parameters[key] = str(mp[i]).strip('[]') + ' 1.0'

        # the input file written only once
        if restart is None:
            self.write_dftb_in()
        else:
            if os.path.exists(restart):
                os.system('cp ' + restart + ' dftb_in.hsd')
            if not os.path.exists('dftb_in.hsd'):
                raise IOError('No file "dftb_in.hsd", use restart=None')

        # indexes for the result file
        self.first_time = True
        self.index_energy = None
        self.index_force_begin = None
        self.index_force_end = None

    def write_dftb_in(self):
        """ Write the innput file for the dftb+ calculation.
            Geometry is taken always from the file 'geo_end.gen'.
        """

        outfile = open('dftb_in.hsd', 'w')
        outfile.write('Geometry = GenFormat { \n')
        outfile.write('    <<< "geo_end.gen" \n')
        outfile.write('} \n')
        outfile.write(' \n')

        # --------MAIN KEYWORDS-------
        previous_key = 'dummy_'
        myspace = ' '
        for key, value in sorted(self.parameters.items()):
            current_depth = key.rstrip('_').count('_')
            previous_depth = previous_key.rstrip('_').count('_')
            for my_backsclash in reversed(range(previous_depth -
                                                current_depth)):
                outfile.write(3 * (1 + my_backsclash) * myspace + '} \n')
            outfile.write(3 * current_depth * myspace)
            if key.endswith('_'):
                outfile.write(key.rstrip('_').rsplit('_')[-1] +
                              ' = ' + str(value) + '{ \n')
            elif key.count('_empty') == 1:
                outfile.write(str(value) + ' \n')
            else:
                outfile.write(key.rsplit('_')[-1] + ' = ' + str(value) + ' \n')
            previous_key = key
        current_depth = key.rstrip('_').count('_')
        for my_backsclash in reversed(range(current_depth)):
            outfile.write(3 * my_backsclash * myspace + '} \n')
        # output to 'results.tag' file (which has proper formatting)
        outfile.write('Options { \n')
        outfile.write('   WriteResultsTag = Yes  \n')
        outfile.write('} \n')
        outfile.close()

    def set(self, **kwargs):
        changed_parameters = FileIOCalculator.set(self, **kwargs)
        if changed_parameters:
            self.reset()
            self.write_dftb_in()

    def check_state(self, atoms):
        system_changes = FileIOCalculator.check_state(self, atoms)
        return system_changes

    def write_input(self, atoms, properties=None, system_changes=None):
        from ase.io import write
        FileIOCalculator.write_input(self, atoms, properties, system_changes)
        self.write_dftb_in()
        write('geo_end.gen', atoms)

    def read_results(self):
        """ all results are read from results.tag file
            It will be destroyed after it is read to avoid
            reading it once again after some runtime error """

        with open('results.tag', 'r') as myfile:
            self.lines = myfile.readlines()

        estring = 'total_energy'
        fstring = 'forces_calculated'
        sstring = 'stress'
        have_stress = False

        forces = list()
        stress = list()

        for iline, line in enumerate(self.lines):
            if estring in line:
                energy = float(self.lines[iline + 1].split()[0]) * Hartree
            elif fstring in line:
                start = iline + 3
                end = start + len(self.atoms)
                for i in range(start, end):
                    force = [float(x) for x in self.lines[i].split()]
                    forces.append(force)
            elif sstring in line:
                have_stress = True
                start = iline + 1
                end = start + 3
                for i in range(start, end):
                    cell = [float(x) for x in self.lines[i].split()]
                    stress.append(cell)

        forces = np.array(forces) * Hartree / Bohr
        if have_stress:
            stress = -np.array(stress) * Hartree / Bohr**3
        elif not have_stress:
            stress = np.zeros((3, 3))

        self.results['energy'] = energy
        self.results['forces'] = forces
        self.results['stress'] = stress
        os.remove('results.tag')

    def read_energy(self):
        """Read Energy from dftb output file (results.tag)."""

        # Energy:
        try:
            energy = float(self.lines[self.index_energy].split()[0]) * Hartree
            self.results['energy'] = energy
        except:
            raise RuntimeError('Problem in reading energy')

    def read_forces(self):
        """Read Forces from dftb output file (results.tag)."""

        try:
            gradients = []
            for j in range(self.index_force_begin, self.index_force_end):
                word = self.lines[j].split()
                gradients.append([float(word[k]) for k in range(0, 3)])

            self.results['forces'] = np.array(gradients) * Hartree / Bohr

        except:
            raise RuntimeError('Problem in reading forces')

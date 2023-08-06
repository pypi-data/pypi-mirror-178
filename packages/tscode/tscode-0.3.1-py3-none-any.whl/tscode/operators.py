# coding=utf-8
'''

TSCODE: Transition State Conformational Docker
Copyright (C) 2021-2022 Nicolò Tampellini

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''

import os
import pickle
import time
from subprocess import DEVNULL, STDOUT, check_call

import numpy as np
from networkx import connected_components

from tscode.clustered_csearch import csearch
from tscode.errors import InputError
from tscode.graph_manipulations import graphize
from tscode.hypermolecule_class import align_structures
from tscode.optimization_methods import _refine_structures, optimize
from tscode.pka import pka_routine
from tscode.settings import (CALCULATOR, DEFAULT_FF_LEVELS, DEFAULT_LEVELS,
                             FF_CALC, FF_OPT_BOOL, PROCS)
from tscode.utils import (get_scan_peak_index, read_xyz,
                          suppress_stdout_stderr, time_to_string, write_xyz)


def operate(input_string, embedder):
    '''
    Perform the operations according to the chosen
    operator and return the outname of the (new) .xyz
    file to read instead of the input one.
    '''
   
    filename = embedder._extract_filename(input_string)

    if 'confab>' in input_string:
        outname = confab_operator(filename,
                                    embedder.options,
                                    logfunction=embedder.log)

    elif 'csearch_opt>' in input_string:
        conf_name = csearch_operator(filename, embedder)
        outname = opt_operator(conf_name,
                                embedder,
                                logfunction=embedder.log)

    elif 'csearch>' in input_string:
        outname = csearch_operator(filename, embedder)

    elif 'opt>' in input_string:
        outname = opt_operator(filename,
                                embedder,
                                logfunction=embedder.log)

    elif 'csearch_hb>' in input_string:
        outname = csearch_operator(filename, embedder, keep_hb=True)
        
    elif 'rsearch>' in input_string:
        outname = csearch_operator(filename, embedder, mode=2)
  
    elif 'scan>' in input_string:
        scan_operator(filename, embedder)
        outname = filename

    elif 'neb>' in input_string:
        neb_operator(filename, embedder)
        embedder.normal_termination()

    elif 'run>' in input_string:
        outname = filename
        # this operator is accounted for in the OptionSetter
        # class of Options, set when the Embedder calls _set_options

    elif 'pka>' in input_string:
        pka_routine(filename, embedder)
        outname = filename

    else:
        op = input_string.split('>')[0]
        raise Exception(f'Operator {op} not recognized.')

    return outname

def confab_operator(filename, options, logfunction=None):
    '''
    '''

    if logfunction is not None:
        logfunction(f'--> Performing conformational search and optimization on {filename}')

    data = read_xyz(filename)

    if len(data.atomcoords) > 1:
        raise InputError(f'Requested conformational search on file {filename} that already contains more than one structure.')

    if len(tuple(connected_components(graphize(data.atomcoords[0], data.atomnos)))) > 1:
        raise InputError((f'Requested conformational search on a molecular complex (file {filename}). '
                           'Confab is not suited for this task, and using TSCoDe\'s csearch> operator '
                           'is a better idea.'))

    if len(set(data.atomnos) - {1,6,7,8,9,15,16,17,35,53}) != 0:
        raise InputError(('Requested conformational search on a molecule that contains atoms different '
                            'than the ones for which OpenBabel Force Fields are parametrized. Please '
                            'perform this conformational search through the more sophisticated and better '
                            'integrated csearch> operator, part of the TSCoDe program.'))
                                
    confname = filename[:-4] + '_confab.xyz'

    with suppress_stdout_stderr():
        check_call(f'obabel {filename} -O {confname} --confab --rcutoff 0.5 --original'.split(), stdout=DEVNULL, stderr=STDOUT)
        # running Confab through Openbabel

    data = read_xyz(confname)
    conformers = data.atomcoords
        
    # if len(conformers) > 10 and not options.let:
    #     conformers = conformers[0:10]
    #     logfunction(f'Will use only the best 10 conformers for TSCoDe embed.\n')

    os.remove(confname)
    with open(confname, 'w') as f:
        for i, conformer in enumerate(conformers):
            write_xyz(conformer, data.atomnos, f, title=f'Generated conformer {i}')

    return confname

def csearch_operator(filename, embedder, keep_hb=False, mode=1):
    '''
    '''

    s = f'--> Performing conformational search on {filename}'
    if keep_hb:
        s += ' (preserving current hydrogen bonds)'
    embedder.log(s)

    # t_start = time.perf_counter()

    data = read_xyz(filename)

    if len(data.atomcoords) > 1:
        embedder.log(f'Requested conformational search on multimolecular file - will do\n' +
                      'an individual search from each conformer (might be time-consuming).')
                                
    # calc, method, procs = _get_lowest_calc(embedder)
    conformers = []

    for i, coords in enumerate(data.atomcoords):

        # opt_coords = optimize(coords, data.atomnos, calculator=calc, method=method, procs=procs)[0] if embedder.options.optimization else coords
        opt_coords = coords
        # optimize starting structure before running csearch

        conf_batch = csearch(
                                opt_coords,
                                data.atomnos,
                                constrained_indexes=_get_internal_constraints(filename, embedder),
                                keep_hb=keep_hb,
                                mode=mode,
                                n_out=embedder.options.max_confs,
                                title=f'{filename}_conf{i}',
                                logfunction=embedder.log,
                                write_torsions=embedder.options.debug
                            )
        # generate the most diverse conformers starting from optimized geometry

        conformers.extend(conf_batch)

    conformers = np.concatenate(conformers)
    # batch_size = conformers.shape[1]

    conformers = conformers.reshape(-1, data.atomnos.shape[0], 3)
    # merging structures from each run in a single array

    # if embedder.embed is not None:
    #     embedder.log(f'\nSelected the most diverse {batch_size} out of {conformers.shape[0]} conformers for {filename} ({time_to_string(time.perf_counter()-t_start)})')
    #     conformers = most_diverse_conformers(batch_size, conformers)

    print(f'Writing conformers to file...{" "*10}', end='\r')

    confname = filename[:-4] + '_confs.xyz'
    with open(confname, 'w') as f:
        for i, conformer in enumerate(conformers):
            write_xyz(conformer, data.atomnos, f, title=f'Generated conformer {i}')

    print(f'{" "*30}', end='\r')

    # if len(conformers) > 10 and not embedder.options.let:
    #     s += f' Will use only the best 10 conformers for TSCoDe embed.'
    # embedder.log(s)

    embedder.log('\n')

    return confname

def opt_operator(filename, embedder, logfunction=None):
    '''
    '''

    mol = next((mol for mol in embedder.objects if mol.name == filename))
    # load molecule to be optimized from embedder

    if logfunction is not None:
        logfunction(f'--> Performing {embedder.options.calculator} {embedder.options.theory_level}' + (
                    f'{f"/{embedder.options.solvent}" if embedder.options.solvent is not None else ""} optimization on {filename} ({len(mol.atomcoords)} conformers)'))
                                
    energies = []
    lowest_calc = _get_lowest_calc(embedder)

    t_start = time.perf_counter()

    conformers, energies = _refine_structures(mol.atomcoords, mol.atomnos, *lowest_calc, loadstring='Optimizing conformer', logfunction=lambda s:embedder.log(s, p=False))

    energies, conformers = zip(*sorted(zip(energies, conformers), key=lambda x: x[0]))
    energies = np.array(energies) - np.min(energies)
    conformers = np.array(conformers)
    # sorting structures based on energy

    mask = energies < 20
    # getting the structures to reject (Rel Energy > 20 kcal/mol)

    if logfunction is not None:
        s = 's' if len(conformers) > 1 else ''
        s = f'Completed optimization on {len(conformers)} conformer{s}. ({time_to_string(time.perf_counter()-t_start)}, ~{time_to_string((time.perf_counter()-t_start)/len(conformers))} per structure).\n'

        if max(energies) > 20:
            s += f'Discarded {len(conformers)-np.count_nonzero(mask)}/{len(conformers)} unstable conformers (Rel. E. > 20 kcal/mol)\n'

    conformers, energies = conformers[mask], energies[mask]
    # applying the mask that rejects high energy confs

    optname = filename[:-4] + '_opt.xyz'
    with open(optname, 'w') as f:
        for i, conformer in enumerate(align_structures(conformers)):
            write_xyz(conformer, mol.atomnos, f, title=f'Optimized conformer {i} - Rel. E. = {round(energies[i], 3)} kcal/mol')

    logfunction(s+'\n')
    logfunction(f'Wrote {len(conformers)} optimized structures to {optname}\n')


    return optname

def neb_operator(filename, embedder):
    '''
    '''
    embedder.t_start_run = time.perf_counter()
    data = read_xyz(filename)
    n_str = len(data.atomcoords)
    assert (n_str in (2, 3) or n_str % 2 == 1), 'NEB calculations need a .xyz input file with two, three or an odd number of geometries.'

    if n_str == 2:
        reagents, products = data.atomcoords
        ts_guess = None
        embedder.log('--> Two structures as input: using them as start and end points.')

    elif n_str == 3:
        reagents, ts_guess, products = data.atomcoords
        embedder.log('--> Three structures as input: using them as start, TS guess and end points.')

    else:
        reagents, *_, products = data.atomcoords
        ts_guess = data.atomcoords[n_str//2]
        embedder.log(f'--> {n_str} structures as input: using first, middle and last as start, TS guess and end points.')

    from tscode.ase_manipulations import ase_neb, ase_popt 

    title = filename[:-4] + '_NEB'

    if embedder.options.neb.preopt:

        embedder.log(f'--> Performing NEB TS optimization. Preoptimizing structures from {filename}\n'
                     f'Theory level is {embedder.options.theory_level} via {embedder.options.calculator}')

        reagents, reag_energy, _ = optimize(
                                            reagents,
                                            data.atomnos,
                                            embedder.options.calculator,
                                            method=embedder.options.theory_level,
                                            procs=embedder.options.procs,
                                            solvent=embedder.options.solvent,
                                            title=f'reagents',
                                            logfunction=embedder.log,
                                            )

        products, prod_energy, _ = optimize(
                                            products,
                                            data.atomnos,
                                            embedder.options.calculator,
                                            method=embedder.options.theory_level,
                                            procs=embedder.options.procs,
                                            solvent=embedder.options.solvent,
                                            title=f'products',
                                            logfunction=embedder.log,
                                            )

    else:
        embedder.log(f'--> Performing NEB TS optimization. Structures from {filename}\n'
                     f'Theory level is {embedder.options.theory_level} via {embedder.options.calculator}')

        print('Getting start point energy...', end='\r')
        _, reag_energy, _ = ase_popt(embedder, reagents, data.atomnos, steps=0)

        print('Getting end point energy...', end='\r')
        _, prod_energy, _ = ase_popt(embedder, products, data.atomnos, steps=0)

    ts_coords, ts_energy, _ = ase_neb(
                                        embedder,
                                        reagents,
                                        products,
                                        data.atomnos,
                                        n_images=embedder.options.neb.images,
                                        ts_guess= ts_guess,
                                        title=title,
                                        logfunction=embedder.log,
                                        write_plot=True,
                                        verbose_print=True
                                    )

    e1 = ts_energy - reag_energy
    e2 = ts_energy - prod_energy

    embedder.log(f'NEB completed, relative energy from start/end points (not barrier heights):\n'
               f'  > E(TS)-E(start): {"+" if e1>=0 else "-"}{round(e1, 3)} kcal/mol\n'
               f'  > E(TS)-E(end)  : {"+" if e2>=0 else "-"}{round(e2, 3)} kcal/mol')

    if not (e1 > 0 and e2 > 0):
        embedder.log(f'\nNEB failed, TS energy is lower than both the start and end points.\n')

    with open(f'{title}_TS.xyz', 'w') as f:
        write_xyz(ts_coords, data.atomnos, f, title='NEB TS - see log for relative energies')

def scan_operator(filename, embedder):
    '''
    Thought to approach or separate two reactive atoms, looking for the energy maximum.
    Scan direction is inferred by the reactive index distance.
    '''
    embedder.t_start_run = time.perf_counter()
    mol_index, mol = next(((i, mol) for i, mol in enumerate(embedder.objects) if mol.name == filename))

    assert len(mol.atomcoords) == 1, 'The scan> operator works on a single .xyz geometry.'
    assert len(mol.reactive_indexes) == 2, 'The scan> operator needs two reactive indexes ' + (
                                          f'({len(mol.reactive_indexes)} were provided)')

    import matplotlib.pyplot as plt

    from tscode.algebra import norm_of
    from tscode.ase_manipulations import ase_popt
    from tscode.pt import pt

    t_start = time.perf_counter()

    # shorthands for clearer code
    i1, i2 = mol.reactive_indexes
    coords = mol.atomcoords[0]

    # getting the start distance between scan indexes and start energy
    d = norm_of(coords[i1]-coords[i2])

    # deciding if moving atoms closer or further apart based on distance
    bonds = list(graphize(coords, mol.atomnos).edges)
    step = 0.05 if (i1, i2) in bonds else -0.05

    # logging to file and terminal
    embedder.log(f'--> {mol.rootname} - Performing a distance scan {"approaching" if step < 0 else "separating"} indexes {i1} ' +
                 f'and {i2} - step size {round(step, 2)} A\n    Theory level is {embedder.options.theory_level} ' +
                 f'via {embedder.options.calculator}')

    # creating a dictionary that will hold results
    # and the structure output list
    dists, energies, structures = [], [], []

    # getting atomic symbols
    s1, s2 = mol.atomnos[[i1, i2]]

    # defining the maximum number of iterations
    if step < 0:
        smallest_d = 0.8*(pt[s1].covalent_radius+
                        pt[s2].covalent_radius)
        max_iterations = round((d-smallest_d) / abs(step))
        # so that atoms are never forced closer than
        # a proportionally small distance between those two atoms.

    else:
        max_d = 2*(pt[s1].covalent_radius+
                   pt[s2].covalent_radius)
        max_iterations = round((max_d-d) / abs(step))
        # so that atoms are never spaced too far apart

    for i in range(max_iterations):

        coords, energy, _ = ase_popt(embedder,
                                     coords,
                                     mol.atomnos,
                                     constrained_indexes=np.array([mol.reactive_indexes]),
                                     targets=(d,),
                                     safe=embedder.fix_angles_in_deformation if hasattr(embedder, 'fix_angles_in_deformation') else False,
                                     title=f'Step {i+1}/{max_iterations} - d={round(d, 2)} A -',
                                     logfunction=embedder.log,
                                     traj=f'{mol.title}_scanpoint_{i+1}.traj' if embedder.options.debug else None,
                                     )
        # optimizing the structure with a spring constraint


        if i == 0:
            e_0 = energy

        energies.append(energy - e_0)
        dists.append(d)
        structures.append(coords)
        # saving the structure, distance and relative energy

        d += step
        # modify the target distance and reiterate

    ### Start the plotting sequence

    fig = plt.figure()
    plt.plot(
        dists,
        energies,
        color='tab:red',
        label='Scan energy',
        linewidth=3,
    )

    # e_max = max(energies)
    id_max = get_scan_peak_index(energies)
    e_max = energies[id_max]

    # id_max = energies.index(e_max)
    d_opt = dists[id_max]

    plt.plot(
        d_opt,
        e_max,
        color='gold',
        label='Energy maximum (TS guess)',
        marker='o',
        markersize=3,
    )

    title = mol.rootname + ' distance scan'
    plt.legend()
    plt.title(title)
    plt.xlabel(f'Indexes {i1}-{i2} distance (A)')
    plt.gca().invert_xaxis()
    plt.ylabel('Rel. E. (kcal/mol)')
    plt.savefig(f'{title.replace(" ", "_")}_plt.svg')
    pickle.dump(fig, open(f'{title.replace(" ", "_")}_plt.pickle', 'wb'))

    ### Start structure writing 

    # print all scan structures
    with open(f'{mol.name[:-4]}_scan.xyz', 'w') as f:
        for i, (s, d, e) in enumerate(zip(structures, dists, energies)):
            write_xyz(s, mol.atomnos, f, title=f'Scan point {i+1}/{len(structures)} ' +
                      f'- d({i1}-{i2}) = {round(d, 3)} A - Rel. E = {round(e, 3)} kcal/mol')

    # print the maximum on another file for convienience
    with open(f'{mol.name[:-4]}_scan_max.xyz', 'w') as f:
        s = structures[id_max]
        d = dists[id_max]
        write_xyz(s, mol.atomnos, f, title=f'Scan point {id_max+1}/{len(structures)} ' +
                    f'- d({i1}-{i2}) = {round(d, 3)} A - Rel. E = {round(e_max, 3)} kcal/mol')

    embedder.log(f'\n--> Written {len(structures)} structures to {mol.name[:-4]}_scan.xyz ({time_to_string(time.perf_counter() - t_start)})')
    embedder.log(f'\n--> Written energy maximum to {mol.name[:-4]}_scan_max.xyz\n')

    # Log data to the embedder class
    embedder.objects[mol_index].scan_data = (dists, energies)

def _get_lowest_calc(embedder=None):
    '''
    Returns the values for calculator,
    method and processors for the lowest
    theory level available from embedder or settings.
    '''
    if embedder is None:
        if FF_OPT_BOOL:
            return (FF_CALC, DEFAULT_FF_LEVELS[FF_CALC], PROCS)
        return (CALCULATOR, DEFAULT_LEVELS[CALCULATOR], PROCS)

    if embedder.options.ff_opt:
        return (embedder.options.ff_calc, embedder.options.ff_level, embedder.options.procs)
    return (embedder.options.calculator, embedder.options.theory_level, embedder.options.procs)

def _get_internal_constraints(filename, embedder):
    '''
    '''
    mol_id = next((i for i, mol in enumerate(embedder.objects) if mol.name == filename))
    # get embedder,objects index of molecule to get internal constraints of

    out = []
    for _, tgt in embedder.pairings_dict[mol_id].items():
        if isinstance(tgt, tuple):
            out.append(tgt)

    return np.array(out)

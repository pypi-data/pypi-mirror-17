"""
Functions to calculate the downstream water surface elevation by minimizing the
difference between flows calculated via the Manning Formula for discharge and
the historical peak flood values.

(https://en.wikipedia.org/wiki/Manning_formula)
(https://en.wikipedia.org/wiki/Volumetric_flow_rate)


Author:
    Matthew A. Turner <maturner01@gmail.com>
Date:
    19 April 2016
"""
import numpy as np
import os
import shutil
import subprocess
import time

from collections import namedtuple
from scipy.optimize import minimize_scalar

from ripcas_dflow import ESRIAsc, Pol, ripcas, shear_mesh_to_asc, veg2n


class ModelRun(object):
    """
    A single coupled run. First DFLOW then RipCAS. CoupledRunSequence will
    encapsulate a series of coupled runs commencing with preparation of the
    initial vegetation map for DFLOW. For now, assume that the vegetation map
    is provided to the run_dflow method.
    """
    def __init__(self):  # , vegetation_ascii_path):

        # have the boundary conditions been found?
        self.bc_converged = False

        # has ripcas been run yet?
        self.vegetation_ascii = None
        self.ripcas_has_run = False
        self.ripcas_directory = None

        self.dflow_has_run = False
        self.dflow_run_directory = None
        self.dflow_shear_output = None

        self.upstream_bc = BoundaryCondition()
        self.downstream_bc = BoundaryCondition()
        self.bc_solution_info = BoundarySolutionInfo()

    def calculate_bc(self, target_streamflow,
                     dbc_geometry_file, streambed_roughness, slope):
        """

        Arguments:
            target_streamflow (float): historical or other streamflow that
                will be used to drive DFLOW model; this calculation recovers
                an estimate for the Water Surface elevation (WS) for this given
                streamflow.
            dbc_geometry_file (str): path to the stream's cross-sectional
                geometry xyz file
            streambed_roughness (float): Manning's n-value for the streambed
            slope (float): slope taken for the reach

        Returns:
            (BoundaryCondition, BoundaryCondition): tuple of upstream and
                downstream BoundaryCondition instances
        """
        dbc_geometry = Pol.from_river_geometry_file(dbc_geometry_file)

        bc_solver = BoundaryConditionSolver(
            target_streamflow, dbc_geometry, streambed_roughness, slope
        )

        bc_solution = bc_solver.solve()

        self.bc_solution_info = bc_solution

        self.bc_converged = bc_solution.success

        self.downstream_bc.amplitude = bc_solution.ws_elev

        self.upstream_bc.amplitude = bc_solution.streamflow

        return (self.upstream_bc, self.downstream_bc)

    def run_dflow(self, dflow_run_directory, vegetation_map,
                  veg_roughness_shearres_lookup, streambed_roughness,
                  clobber=True, pbs_script_name='dflow_mpi.pbs',
                  dflow_run_fun=None):
        """
        Both input and output dflow files will go into the dflow_run_directory,
        but in input/ and output/ subdirectories.

        Arguments:
            dflow_run_directory (str): directory where DFLOW files should be
                put and where the dflow_run_fun will be run from
            vegetation_map (str): path to the input vegetation.pol file. This
                function assumes this has already been generated in the proper
                format b/c this seems like the best separation of
                responsibilities.
            clobber (bool): whether or not to overwrite dflow_run_directory if
                it exists
            pbs_script_name (str): name of .pbs script w/o directory
            dflow_run_fun (function): argument-free function to run DFLOW.
                Ex. `dflow_run_fun=f` where `f` defined by
                `def f: subprocess.call(['qsub', 'dflow_mpi.pbs'])`

        Returns:
            None
        """
        if not self.bc_converged:
            raise RuntimeError(
                'Boundary conditions must be calculated before ' +
                'DFLOW can be run'
            )

        if self.dflow_has_run:
            raise RuntimeError(
                'DFLOW has already been run for this CoupledRun'
            )

        if os.path.exists(dflow_run_directory):

            if not clobber:
                raise RuntimeError(
                    'DFLOW has already been run for this CoupledRun'
                )

            shutil.rmtree(dflow_run_directory)

        self.dflow_run_directory = dflow_run_directory

        os.mkdir(dflow_run_directory)

        # write boundary conditions to file
        bc_up_path = os.path.join(dflow_run_directory,
                                  'boundriver_up_0001.cmp')

        bc_down_path = os.path.join(dflow_run_directory,
                                    'boundriverdown_0001.cmp')

        self.upstream_bc.write(bc_up_path)
        self.downstream_bc.write(bc_down_path)

        self.vegetation_ascii = ESRIAsc(vegetation_map)

        veg_path = os.path.join(dflow_run_directory, 'n.pol')

        Pol.from_ascii(
            veg2n(self.vegetation_ascii,
                  veg_roughness_shearres_lookup,
                  streambed_roughness)
        ).write(veg_path)

        oj = os.path.join

        pbs_path = oj(dflow_run_directory, pbs_script_name)
        mdu_path = oj(dflow_run_directory, 'base.mdu')
        net_path = oj(dflow_run_directory, 'base_net.nc')
        ext_path = oj(dflow_run_directory, 'base.ext')
        brd_path = oj(dflow_run_directory, 'boundriverdown.pli')
        bru_path = oj(dflow_run_directory, 'boundriver_up.pli')

        self.dflow_shear_output =\
            os.path.join(dflow_run_directory,
                         'DFM_OUTPUT_base',
                         'base_map.nc')

        with open(pbs_path, 'w') as f:
            p = _join_data_dir(oj('dflow_inputs', 'dflow_mpi.pbs'))
            s = open(p, 'r').read()
            f.write(s)

        with open(mdu_path, 'w') as f:
            p = _join_data_dir(oj('dflow_inputs', 'base.mdu'))
            s = open(p, 'r').read()
            f.write(s)

        with open(net_path, 'w') as f:
            p = _join_data_dir(oj('dflow_inputs', 'base_net.nc'))
            s = open(p, 'r').read()
            f.write(s)

        with open(ext_path, 'w') as f:
            p = _join_data_dir(oj('dflow_inputs', 'base.ext'))
            s = open(p, 'r').read()
            f.write(s)

        with open(brd_path, 'w') as f:
            p = _join_data_dir(oj('dflow_inputs', 'boundriverdown.pli'))
            s = open(p, 'r').read()
            f.write(s)

        with open(bru_path, 'w') as f:
            p = _join_data_dir(oj('dflow_inputs', 'boundriver_up.pli'))
            s = open(p, 'r').read()
            f.write(s)

        bkdir = os.getcwd()
        os.chdir(dflow_run_directory)

        if dflow_run_fun is None:

            print '\n*****\nDry Run of DFLOW\n*****\n'

            os.chdir(bkdir)
            example_shear_path = 'jemez_r02_map.nc'
            if os.path.exists(example_shear_path):
                os.makedirs(os.path.dirname(self.dflow_shear_output))
                shutil.copyfile(example_shear_path, self.dflow_shear_output)

            else:
                print 'Get you a copy of a DFLOW output, yo! ' +\
                      'Can\'t run RipCAS without it!'

                with open('not_actually_output.nc', 'w') as f:
                    f.write('A FAKE NETCDF!!!')

            self.dflow_has_run = True

        else:

            # in the case of running a process on CARC, the ret is a Popen inst
            ret = dflow_run_fun()

            os.chdir(bkdir)
            self.dflow_has_run = True

            return ret

    def run_ripcas(self, zone_map_path, ripcas_required_data_path,
                   ripcas_directory, shear_asc=None, clobber=True):

        if not self.dflow_has_run:
            raise RuntimeError(
                'DFLOW must run before ripcas can be run'
            )

        if os.path.exists(ripcas_directory):

            if not clobber:
                raise RuntimeError(
                    'DFLOW has already been run for this CoupledRun'
                )

            shutil.rmtree(ripcas_directory)

        self.ripcas_directory = ripcas_directory

        os.mkdir(ripcas_directory)

        hdr = self.vegetation_ascii.header_dict()

        if shear_asc is None:
            shear_asc = shear_mesh_to_asc(self.dflow_shear_output, hdr)
        else:
            assert isinstance(shear_asc, ESRIAsc),\
                'shear_asc must be of type ESRIAsc if provided'

        shear_asc.write(
            os.path.join(self.dflow_run_directory, 'shear_out.asc')
        )

        output_veg_ascii = ripcas(
            self.vegetation_ascii, zone_map_path,
            shear_asc, ripcas_required_data_path
        )

        output_vegetation_path = os.path.join(
            ripcas_directory, 'vegetation.asc'
        )
        output_veg_ascii.write(output_vegetation_path)

        self.ripcas_has_run = True

        return output_veg_ascii


BoundarySolutionInfo = namedtuple(
    'BoundarySolutionInfo', ['ws_elev', 'streamflow', 'error', 'success']
)
BoundarySolutionInfo.__new__.__defaults__ = (None, None, None, None)


class BoundaryConditionSolver:

    def __init__(self,
                 historical_streamflow,
                 dbc_geometry,
                 streambed_roughness,
                 slope):

        self.q_hist = historical_streamflow
        self.geom = dbc_geometry
        self.n = streambed_roughness
        self.slope = slope

    def solve(self):

        def _streamflow_error(ws_elev):

            calc =\
                _calculate_streamflow(self.geom, self.n, ws_elev, self.slope)

            return abs(calc - self.q_hist)

        # generate initial guesses with wide-spaced points
        result = minimize_scalar(_streamflow_error,
                                 bounds=(self.geom.z.min(), self.geom.z.max()),
                                 method='bounded',
                                 options={'xatol': 1e-6, 'maxiter': 1000})

        return BoundarySolutionInfo(
            result.x,
            _calculate_streamflow(self.geom, self.n, result.x, self.slope),
            result.fun,
            result.success
        )


StreamflowTuple = namedtuple('StreamflowTuple', ['ws_elev', 'streamflow'])


def _calculate_streamflow(dbc_geometry, streambed_roughness,
                          water_surface_elevation, slope):
    # have N points; get N-1 distances and
    # N-1 Max/Min over those distances
    x = dbc_geometry.x
    y = dbc_geometry.y
    z = dbc_geometry.z

    dx = np.diff(x)
    dy = np.diff(y)

    xydist = np.sqrt(np.square(dx) + np.square(dy))
    # station = np.cumsum(xydist)

    zmax_by_segment = np.array(
        [max(z[i], z[i+1]) for i in range(len(z)-1)]
    )

    zmin_by_segment = np.array(
        [min(z[i], z[i+1]) for i in range(len(z)-1)]
    )

    # get N-1 vector taken from S = ('below', 'triangle', 'trap')
    # for the three possible positions of the water surface and
    # commensurate calculation methods for wetted perimeter
    ws_location = np.array(
        [
            _get_ws_location(water_surface_elevation, _z[0], _z[1])
            for _z in zip(zmax_by_segment, zmin_by_segment)
        ]
    )

    # calculate the cross-sectional area of the stream
    # at the lower bound
    area_vec = np.zeros(len(ws_location))
    # wetted perimeter
    wp_vec = np.zeros(len(ws_location))

    ws_elev = water_surface_elevation
    for idx, loc in enumerate(ws_location):

        if loc == 'triangle':

            zmin = zmin_by_segment[idx]
            zmax = zmax_by_segment[idx]
            xy = xydist[idx]

            # calculate area
            area_vec[idx] = 0.5 * (ws_elev - zmin) * xy

            # calculate wetted perimeter
            _da = ((ws_elev - zmin)/(zmax - zmin)) * xy
            _db = ws_elev - zmin

            wp_vec[idx] = np.sqrt(_da**2.0 + _db**2.0)

        elif loc == 'trapezoid':

            zmin = zmin_by_segment[idx]
            zmax = zmax_by_segment[idx]
            xy = xydist[idx]

            area_vec[idx] = 0.5 * xy * (2*ws_elev - zmax - zmin)

            wp_vec[idx] = np.sqrt(xy**2.0 + (zmax - zmin)**2.0)

    area_sum = sum(area_vec)
    wp_sum = sum(wp_vec)

    n_inv = (1.0/streambed_roughness)

    Q = n_inv * area_sum * (pow((area_sum/wp_sum), 2/3.0)) * np.sqrt(slope)

    return Q


def _get_ws_location(water_surface_elev, zmax, zmin):
    """
    Return one of three values depending on the location of the water surface
    relative to the elevations of the discretized cross-section points.
    Vectorized below.

    Returns:
        (str) one of the following: 'below' if above zmax (and automatically
            zmin), 'triangle' if between zmax and zmin, and 'trapezoid'
            if below zmin. This corresponds to the geometry that will be used
            to calculate the wetted perimeter and area of the induced polygon.
    """

    if water_surface_elev > zmax:
        return 'trapezoid'
    elif water_surface_elev <= zmax and water_surface_elev > zmin:
        return 'triangle'
    else:
        return 'below'


class BoundaryCondition:

    def __init__(self,
                 period=0.0,  # (minutes)
                 amplitude=0.0,  # (ISO)
                 phase=0.0):  # (deg)

        self.period = period
        self.amplitude = amplitude
        self.phase = phase

    def write(self, out_path):

        with open(out_path, 'w') as f:
            f.write(self.__repr__())

    def __repr__(self):
        return '\n'.join([
                '* COLUMN=3',
                '* COLUMN1=Period (min) or Astronomical Componentname',
                '* COLUMN2=Amplitude (ISO)',
                '* COLUMN3=Phase (deg)',
                '{0}  {1}  {2}'.format(self.period, self.amplitude, self.phase)
            ])


def mr_log(log_f, msg):

    ta = time.asctime
    log_f.write('[{0}] '.format(ta()) + msg)
    log_f.flush()
    os.fsync(log_f.fileno())


def modelrun_series(data_dir, initial_vegetation_map, vegzone_map,
                    veg_roughness_shearres_lookup, peak_flows_file,
                    geometry_file, streambed_roughness,
                    streambed_floodplain_roughness, streambed_slope,
                    dflow_run_fun=None, log_f=None, debug=False):
    '''
    Run a series of flow and succession models with peak flows given in
    peak_flows_file.

    Arguments:
        data_dir (str): write directory for modelrun series. Must exist
        initial_vegetation_map (str): location of year zero veg map
        vegzone_map (str): vegetation zone map location
        veg_roughness_shearres_lookup (str): Excel spreadsheet containing
            conversion from vegetation code to roughness value and vegetation
            code to shear stress resistance
        peak_flow_file (str): location of text file record of peak flows in
            cubic meters per second
        geometry_file (str): location of channel geometry at the downstream
            location for calculating streamflow
        streambed_roughness (float): streambed roughness in channel only; used
            when converting vegetation map to roughness map
        streambed_floodplain_roughness (float): an average roughness of
            stream channel and floodplain used in calculation of downstream
            boundary condition for DFLOW
        streambed_slope (float): rise over run of the channel used in
            calculation of downstream boundary condition for DFLOW
        dflow_run_fun (function): function delegate for the user to provide a
            custom way to run DFLOW. If none is given, defaults to
            submitting a PBS job as is done on CARC systems
        log_f (str): log file. if none is given, defaults to `data_dir`.log
            with dashes replacing slashes
        debug (bool): whether or not to run in debug mode. If running in debug
            mode, each DFLOW run returns fake data and
            each RipCAS run takes cord/data/shear_out.asc as input

        returns:
            None
    '''

    if dflow_run_fun is None:

        def dflow_fun():

            import subprocess

            return subprocess.Popen(
                'qsub dflow_mpi.pbs', shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

    if log_f is None:

        first_char = data_dir[0]
        root_log_f = first_char if first_char != '/' else ''
        root_log_f += data_dir[1:].replace('/', '-')

        log_f = open(root_log_f + '.log', 'w')

    else:
        log_f = open(log_f, 'w')

    with open(peak_flows_file, 'r') as f:
        l0 = f.readline().strip()
        assert l0 == 'Peak.Flood', '{} not Peak.Flood'.format(l0)
        peak_flows = [float(l.strip()) for l in f.readlines()]

    inputs_dir = os.path.join(data_dir, 'inputs')
    if os.path.isdir(inputs_dir):
        shutil.rmtree(inputs_dir)
    os.mkdir(inputs_dir)

    shutil.copy(initial_vegetation_map, inputs_dir)
    shutil.copy(vegzone_map, inputs_dir)
    shutil.copy(veg_roughness_shearres_lookup, inputs_dir)
    shutil.copy(peak_flows_file, inputs_dir)
    shutil.copy(geometry_file, inputs_dir)

    roughness_slope_path = os.path.join(inputs_dir, 'roughness_slope.txt')

    with open(roughness_slope_path, 'w') as f:
        f.write('roughness\tslope\n')
        f.write('%s\t%s\n' % (streambed_roughness, streambed_slope))

    for flow_idx, flow in enumerate(peak_flows):

        mr = ModelRun()

        mr.calculate_bc(
            flow, geometry_file,
            streambed_floodplain_roughness, streambed_slope
        )

        mr_log(
            log_f, 'Boundary conditions for flow index {0} finished\n'.format(
                flow_idx
            )
        )

        dflow_dir = os.path.join(data_dir, 'dflow-' + str(flow_idx))

        if flow_idx == 0:
            veg_file = initial_vegetation_map
        else:
            veg_file = os.path.join(
                data_dir, 'ripcas-' + str(flow_idx - 1), 'vegetation.asc'
            )

        if debug:
            mr.run_dflow(dflow_dir, veg_file,
                         veg_roughness_shearres_lookup, streambed_roughness)
            job_id = 'debug'

        else:
            p_ref = mr.run_dflow(dflow_dir, veg_file,
                                 veg_roughness_shearres_lookup,
                                 streambed_roughness,
                                 dflow_run_fun=dflow_fun)

            job_id = p_ref.communicate()[0].split('.')[0]

        mr_log(log_f, 'Job ID {0} submitted for DFLOW run {1}\n'.format(
                job_id, flow_idx
            )
        )

        # check the status of the job by querying qstat; break loop when
        # job no longer exists, giving nonzero poll() value
        job_not_finished = True
        while job_not_finished:

            mr_log(
                log_f,
                'Job ID {0} not yet finished for DFLOW run {1}\n'.format(
                    job_id, flow_idx
                )
            )

            if debug:
                job_not_finished = False

            else:
                p = subprocess.Popen(
                    'qstat ' + job_id, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

                p.communicate()

                poll = p.poll()
                job_not_finished = poll == 0

                time.sleep(600)
        mr_log(
            log_f, 'DFLOW run {0} finished, starting RipCAS\n'.format(
                flow_idx
            )
        )

        ripcas_dir = os.path.join(data_dir, 'ripcas-' + str(flow_idx))

        if debug:
            p = _join_data_dir('shear_out.asc')
            mr.run_ripcas(vegzone_map, veg_roughness_shearres_lookup,
                          ripcas_dir, shear_asc=ESRIAsc(p))

        mr_log(log_f, 'RipCAS run {0} finished\n'.format(flow_idx))

    log_f.close()


if __name__ == '__main__':

    import sys

    help_msg = '''
modelrun.py

Author: Matthew Turner

Usage:
    python ripcas_dflow/modelrun.py data_dir initial_vegetation vegzone_map veg_roughness_shearres_lookup\
            peak_flows_file geometry_file streambed_roughness streambed_slope

    data_dir: directory to hold each time step of the model run
    initial_vegetation: .asc file with initial vegetation map
    vegzone_map: .asc file with vegetation zone information
    veg_roughness_shearres_lookup: .xlsx file with veg type-to-n and shear resistance-per-veg type information
    peak_flows_file: file with a column of peak flood flow in cubic meters per second
    geometry_file: xyz file representing geometry of downstream cross section for boundary conditions calculation
    streambed_roughness: floating point number for the roughness value of the streambed
    streambed_slope: floating point number for the slope of the stream geography
'''
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print help_msg
        sys.exit(0)

    if len(sys.argv) != 9:
        print help_msg
        sys.exit(1)

    data_dir = sys.argv[1]
    initial_vegetation_map = sys.argv[2]
    vegzone_map = sys.argv[3]
    veg_roughness_shearres_lookup = sys.argv[4]
    peak_flows_file = sys.argv[5]
    geometry_file = sys.argv[6]
    streambed_roughness = float(sys.argv[7])
    streambed_slope = float(sys.argv[8])

    modelrun_series(data_dir, initial_vegetation_map, vegzone_map,
                     veg_roughness_shearres_lookup, peak_flows_file, geometry_file,
                     streambed_roughness, streambed_slope, dflow_run_fun=None,
                     log_f=None)


def _join_data_dir(f):
    '''
    Join the filename, f, to the default data directory
    '''
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    return os.path.join(data_dir, f)

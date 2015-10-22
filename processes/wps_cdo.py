"""
Processes with cdo commands
"""

from malleefowl.process import WPSProcess

from cdo import Cdo

from malleefowl import wpslogging as logging
logger = logging.getLogger(__name__)

class CDOOperation(WPSProcess):
    """This process calls cdo with operation on netcdf file"""
    def __init__(self):
        WPSProcess.__init__(
            self,
            identifier = "cdo_operation",
            title = "CDO Operation",
            version = "0.1",
            metadata=[
                {"title":"CDO","href":"https://code.zmaw.de/projects/cdo"},
                ],
            abstract="Apply CDO Operation like monmax on NetCDF File.",
            )

        self.netcdf_file = self.addComplexInput(
            identifier="netcdf_file",
            title="NetCDF File",
            abstract="NetCDF File",
            minOccurs=1,
            maxOccurs=100,
            maxmegabites=5000,
            formats=[{"mimeType":"application/x-netcdf"}],
            )

        self.operator = self.addLiteralInput(
            identifier="operator",
            title="CDO Operator",
            abstract="Choose a CDO Operator",
            default="monmax",
            type=type(''),
            minOccurs=1,
            maxOccurs=1,
            allowedValues=['merge', 'dayavg', 'daymax', 'daymean', 'daymin','daysum', 'dayvar',    'daystd', 'monmax', 'monmin', 'monmean', 'monavg', 'monsum', 'monvar', 'monstd', 'ymonmin', 'ymonmax', 'ymonsum', 'ymonmean', 'ymonavg', 'ymonvar', 'ymonstd', 'yearavg', 'yearmax', 'yearmean', 'yearmin', 'yearsum', 'yearvar', 'yearstd', 'yseasvar']
            )

        self.output = self.addComplexOutput(
            identifier="output",
            title="NetCDF Output",
            abstract="NetCDF Output",
            metadata=[],
            formats=[{"mimeType":"application/x-netcdf"}],
            asReference=True,
            )

    def execute(self):
        self.show_status("starting cdo operator", 10)

        nc_files = self.getInputValues(identifier='netcdf_file')
        operator = self.operator.getValue()

        cdo = Cdo()
        cdo_op = getattr(cdo, operator)

        outfile = self.mktempfile(suffix='.nc')
        cdo_op(input= " ".join(nc_files), output=outfile)
        
        self.show_status("cdo operator done", 90)
        self.output.setValue( outfile )


class CDOInfo(WPSProcess):
    """This process calls cdo sinfo on netcdf file"""

    def __init__(self):
        WPSProcess.__init__(
            self,
            identifier = "cdo_sinfo",
            title = "CDO sinfo",
            version = "0.1",
            metadata=[
                {"title":"CDO","href":"https://code.zmaw.de/projects/cdo"},
                ],
            abstract="Apply CDO sinfo on NetCDF File.",
            )

        self.netcdf_file = self.addComplexInput(
            identifier="netcdf_file",
            title="NetCDF File",
            abstract="NetCDF File",
            minOccurs=1,
            maxOccurs=100,
            maxmegabites=5000,
            formats=[{"mimeType":"application/x-netcdf"}],
            )

        self.output = self.addComplexOutput(
            identifier="output",
            title="CDO sinfo result",
            abstract="CDO sinfo result",
            metadata=[],
            formats=[{"mimeType":"text/plain"}],
            asReference=True,
            )

    def execute(self):
        self.show_status("starting cdo sinfo", 0)

        cdo = Cdo()

        nc_files = self.getInputValues(identifier='netcdf_file')

        outfile = self.mktempfile(suffix='.txt')
        with open(outfile, 'w') as fp: 
            for nc_file in nc_files:
                sinfo = cdo.sinfo(input=nc_file, output=outfile)
                for line in sinfo:
                    fp.write(line + '\n')
                fp.write('\n\n')

        self.show_status("cdo sinfo done", 90)

        self.output.setValue( outfile )


class CdoIntvert(WPSProcess):
    """Vertical interpolation"""
    def __init__(self):
        WPSProcess.__init__(
            self,
            identifier = 'cdo_intvert',
            title = 'CDO 2.12.5 INTVERT - Vertical interpolation',
            abstract = 'Interpolate 3D variables on hybrid model levels to pressure or height levels.',
            metadata = [{'title': 'CDO', 'href': 'https://code.zmaw.de/projects/cdo'}],
            version = '1.0', # Can this be ommited?
            )

        self.netcdf_file = self.addComplexInput(
            identifier = 'netcdf_file',
            title = 'NetCDF File',
            abstract = 'NetCDF File',
            formats = [{'mimeType': 'application/x-netcdf'}],
            )

        self.operator = self.addLiteralInput(
            identifier = 'operator',
            title = 'CDO Operator',
            abstract = 'Choose a CDO Operator',
            type = type(''),
            allowedValues = ['ml2pl', 'ml2hl'],
            )

        self.levels = self.addLiteralInput(
            identifier = 'levels',
            title = 'p/h levels',
            abstract = 'Float; Pressure levels in pascal / Height levels in meter',
            type = type(''),
            maxOccurs = 100,
            )

        self.output = self.addComplexOutput(
            identifier = 'output',
            title = 'NetCDF Output',
            abstract = 'NetCDF Output',
            formats = [{'mimeType': 'application/x-netcdf'}],
            asReference = True,
            )

    def execute(self):
        self.show_status('starting cdo operattion', 10)

        operator = self.getInputValue('operator')
        nc_file = self.getInputValue('netcdf_file')
        levels = self.getInputValue('levels')

        cdo = Cdo()
        cdo_op = getattr(cdo, operator)

        outfile = self.mktempfile(suffix='.nc')
        cdo_op(*levels, input=nc_file, output=outfile)

        self.show_status('cdo operation done', 90)
        self.output.setValue(outfile)

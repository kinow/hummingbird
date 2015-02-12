from malleefowl import config

from hummingbird.process import ESMValToolProcess
from hummingbird import esmvaltool

from malleefowl import wpslogging as logging
logger = logging.getLogger(__name__)

class ESMValToolOverviewProcess(ESMValToolProcess):
    def __init__(self):
        ESMValToolProcess.__init__(self,
            identifier = "surfconplot",
            title = "ESMValTool: surface contour plot for precipitation",
            version = "0.1",
            abstract="Tutorial contour plot used in the doc/overview.pdf")

        ## self.variable = self.addLiteralInput(
        ##     identifier="variable",
        ##     title="Variable",
        ##     abstract="",
        ##     default="pr",
        ##     type=type(''),
        ##     minOccurs=1,
        ##     maxOccurs=1,
        ##     allowedValues=['pr']
        ##     )

    def execute(self):
        self.show_status("starting", 0)

        # TODO: configure distrib, replica, limit
        
        out, namelist_file, log_file = esmvaltool.run_on_esgf(
            diag='surfconplot',
            credentials=self.credentials.getValue(),
            project="CMIP5",
            models=self.getInputValues(identifier='model'),
            variable='pr',
            cmor_table=self.cmor_table.getValue(),
            experiment=self.experiment.getValue(),
            ensemble=self.ensemble.getValue(),
            distrib=True,
            replica=False,
            limit=100,
            start_year=self.start_year.getValue(),
            end_year=self.end_year.getValue(),
            output_format=self.output_format.getValue(),
            monitor=self.show_status  )
        
        self.show_status("done", 100)

        self.namelist.setValue(namelist_file)
        self.log.setValue( log_file )
        self.output.setValue(out)
        

 
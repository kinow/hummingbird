import os
import shutil
import tarfile
import glob
from subprocess import check_output, CalledProcessError, STDOUT

from pywps.Process import WPSProcess
import logging
logger = logging.getLogger(__name__)

def qa_checker(filename, project):
    cmd = ["qa-dkrz", "-P", project, filename]
    try:
        output = check_output(cmd, stderr=STDOUT)
    except CalledProcessError as e:
        msg = "qa checker failed: %s" % (e.output)
        logger.error(msg)
        raise Exception(msg)


class QualityChecker(WPSProcess):
    def __init__(self):
        WPSProcess.__init__(self,
            identifier = "qa_checker",
            title = "Quality Assurance Checker by DKRZ",
            version = "0.5.13",
            abstract="Project specific qualtiy checks for CORDEX, CMIP5, ...",
            metadata= [ {"title": "Documentation" , "href": "http://qa-dkrz.readthedocs.io/en/latest/"} ],
            statusSupported=True,
            storeSupported=True
            )

        self.dataset = self.addComplexInput(
            identifier="dataset",
            title="Dataset (NetCDF)",
            abstract="NetCDF files to be checked.",
            minOccurs=1,
            maxOccurs=1000,
            maxmegabites=10000,
            formats=[{"mimeType":"application/x-netcdf"}],
            )

        self.project = self.addLiteralInput(
            identifier="project",
            title="Project",
            default="CORDEX",
            type=type(''),
            minOccurs=1,
            maxOccurs=1,
            allowedValues=['CORDEX', 'CMIP5'])

        self.output = self.addComplexOutput(
            identifier="output",
            title="Quality Checker Report",
            abstract="Qualtiy checker results as tar archive.",
            formats=[{"mimeType":"application/x-tar-gz"}],
            asReference=True,
            )

        self.logfile = self.addComplexOutput(
            identifier="logfile",
            title="Quality Checker Logfile",
            abstract="Qualtiy checker summary logfile",
            formats=[{"mimeType":"text/yaml"}],
            asReference=True,
            )

    def execute(self):
        self.status.set("starting qa checker ...", 0)

        datasets = self.getInputValues(identifier='dataset')
        for idx,ds in enumerate(datasets):
            progress = idx * 100 / len(datasets)
            self.status.set("checking %s" % ds, progress)
            qa_checker(ds, project=self.project.getValue())

        results_path = os.path.join("QA_Results", "check_logs")
        if not os.path.isdir(results_path):
            raise Exception("QA results are missing.")

        # output tar archive
        outfile = 'output.tar.gz'
        self.output.setValue( outfile )
        tar = tarfile.open(outfile, "w:gz")
        tar.add(results_path)
        tar.close()

        # output logfile
        logs = glob.glob(os.path.join(results_path, "*.log"))
        if not logs:
            logs = glob.glob(os.path.join(results_path, ".*.log"))
        if logs:
            # use .txt extension
            filename = logs[0][:-4] + '.txt'
            os.link(logs[0], filename)
            self.logfile.setValue(filename)
        else:
            raise Exception("could not find log file.")

        self.status.set("qa checker: done", 100)


        

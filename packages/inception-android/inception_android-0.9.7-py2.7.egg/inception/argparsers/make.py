from inception.argparsers.argparser import InceptionArgParser
from inception.argparsers.exceptions import InceptionArgParserException
from inception.constants import InceptionConstants
from inception.config import ConfigTreeParser, DotIdentifierResolver
from inception.common.configsyncer import ConfigSyncer
from inception.common.filetools import FileTools
import sys
import os, shutil, logging, tempfile

logger = logging.getLogger(__name__)

class MakeArgParser(InceptionArgParser):

    def __init__(self, description = "Make mode cmd"):
        super(MakeArgParser, self).__init__(description = description)

        targetOpts = self.add_mutually_exclusive_group(required = True)
        targetOpts.add_argument('-v', '--variant',action = "store", help="variant config code to use, in the format A.B.C")
        targetOpts.add_argument('-c', '--config', action= 'store', help = "Explicit path to config to use instead of passing variant code, requires --output")

        optionalOpts = self.add_argument_group("Optional opts")
        optionalOpts.add_argument("-o", "--output", action="store", help = "Override default output path")
        optionalOpts.add_argument("-k", "--keep-work", action="store_true", help="Don't delete work dir when finished")
        optionalOpts.add_argument('--learn-settings', action="store_true",
                                  help= "Learn settings from a connected device, and use in generated update package")

        self.deviceDir = InceptionConstants.VARIANTS_DIR
        self.baseDir = InceptionConstants.BASE_DIR
        identifierResolver = DotIdentifierResolver([self.deviceDir, self.baseDir])
        self.configTreeParser = ConfigTreeParser(identifierResolver)

    def process(self):
        super(MakeArgParser, self).process()

        code = self.args["variant"]
        outDir = self.args["output"]
        if code:
            self.config = self.configTreeParser.parseJSON(code)

            try:
                a, b, c= code.split('.')
            except ValueError as e:
                raise InceptionArgParserException(
                    "Code must me in the format vendor.model.variant"
                )

            self.setWorkDir(os.path.join(InceptionConstants.WORK_DIR,
                a,
                b,
                c)
            )
        else:
            configPath = self.args["config"]
            if not outDir:
                print("Must set --output when using --config")
                sys.exit(1)
            self.config = self.configTreeParser.parseJSONFile(configPath)
            self.setWorkDir(tempfile.mkdtemp())

        if self.config.get("__abstract__", False, directOnly=True):
            print("Won't make abstract config %s" % code)
            sys.exit(1)
        if self.config.get("__config__") is None:
            sys.stderr.write("You are using an outdated config tree. Please run 'incept sync -v VARIANT_CODE' or set __config__ (see https://goo.gl/aFWPby)\n")
            sys.exit(1)


        if outDir:
            self.config.setOutPath(outDir)
        else:
            outDir = self.config.getOutPath()

        self.workDir = self.getWorkDir()
        self.configDir = os.path.dirname(self.config.getSource())

        logger.info("Cleaning work dir " + self.workDir)
        if os.path.exists(self.workDir):
            shutil.rmtree(self.workDir)
        os.makedirs(self.workDir)

        if self.args["learn_settings"]:
            syncer = ConfigSyncer(self.config)
            syncer.applyDiff(syncer.pullAndDiff())

        self.config.make(self.workDir)

        if not self.args["keep_work"]:
            logger.info("Cleaning up work dir")
            shutil.rmtree(self.getWorkDir())

        return True



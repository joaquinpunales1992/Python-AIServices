from watson_developer_cloud import ToneAnalyzerV3
import json
import os as os
import config
from watson_developer_cloud import WatsonException

class Tono():
    def __init__(self):
        self.vTone_analyzer = ToneAnalyzerV3(
                                        username=config.WTAusername,
                                        password=config.WTApass,
                                        version=config.WTAversion)



    def invocarWToneAnalyzer(self, pRutaArhivo):
        vError = 0
        vTonoResultado = ''
        err = ''
        try:
            with open(os.path.join(os.path.dirname(__file__), pRutaArhivo)) as vArchivo:
                vTonoResultado = self.vTone_analyzer.tone(
                                                            text=str(vArchivo)
                                                         )
                return [vTonoResultado, vError, err]

        except WatsonException as err:
            vError = 1
            return [vTonoResultado, vError, err]



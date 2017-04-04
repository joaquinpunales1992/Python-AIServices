from watson_developer_cloud import ToneAnalyzerV3
import json
import os as os
import config


class Tono():
    def __init__(self):
        self.vTone_analyzer = ToneAnalyzerV3(
                                        username=config.WTAusername,
                                        password=config.WTApass,
                                        version=config.WTAversion)



    def invocarWToneAnalyzer(self, pRutaArhivo):
        with open(os.path.join(os.path.dirname(__file__), pRutaArhivo)) as vArchivo:
            vTonoResultado = self.vTone_analyzer.tone(
                                                        text=str(vArchivo)
                                                     )
            return vTonoResultado
            print(json.dumps(vTonoResultado, indent=2))



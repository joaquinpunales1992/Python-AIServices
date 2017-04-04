from watson_developer_cloud import PersonalityInsightsV3 as PersonalityInsightsV3
import os as os
import config
from watson_developer_cloud import WatsonException

class Personalidad():
    def __init__(self):
        self.personalidad = PersonalityInsightsV3(
                                              version=config.WPIversion,
                                              username=config.WPIusername,
                                              password=config.WPIpass
                                            )


        # profile(text, content_type='text/plain', content_language=None,
        #   accept='application/json', accept_language=None, raw_scores=False,
        #   consumption_preferences=False, csv_headers=False)

    def invocarWatsonPI(self, pRutaArhivo):
        vError = 0
        profile = ''
        err = ''
        try:
            with open(os.path.join(os.path.dirname(__file__), pRutaArhivo)) as profile_json:
                profile = self.personalidad.profile(
                                                  profile_json.read(),
                                                  content_type='text/plain;charset=utf-8', #application/json
                                                  raw_scores=True,
                                                  consumption_preferences=True,
                                                  accept_language="es",
                                                  )

                return [profile, vError, err]
        except WatsonException as err:
            vError = 1
            return [profile, vError, err]






from IPython import get_ipython
import sys
import time
import numpy as np
from openpyxl import load_workbook
import xlwings as xw
import MK_GMS_Pro_Modules as mod
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class InputHandler:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def load_decision_data(self, game_id, team, period):
        query = text("""
        SELECT
            inputSolidVerkaufspreisInland,
            inputSolidVerkaufspreisAusland,
            inputSolidFETechnik,
            inputSolidFEHaptik,
            inputSolidProduktwerbungInland,
            inputSolidProduktwerbungAusland,
            inputSolidLiefermengeAusland,
            selectIdealMarktbericht,
            inputSolidLiefermengeSondermarkt,

            inputIdealVerkaufspreisInland,
            inputIdealVerkaufspreisAusland,
            inputIdealFETechnik,
            inputIdealFEHaptik,
            inputIdealProduktwerbungInland,
            inputIdealProduktwerbungAusland,
            inputIdealLiefermengeAusland,
            selectSolidMarktbericht,

            sumPR,
            sumVertriebspersonalInland,
            sumVertriebspersonalAusland,
            selectBranchenbericht,

            inputSolidFertigungsmengen,
            inputSolidHilfsstoffe,
            inputSolidMaterialS,

            inputIdealFertigungsmengen,
            inputIdealHilfsstoffe,
            inputMaterialI,

            selectNeuAnlagenWerkstaette01,
            selectNeuAnlagenWerkstaette08,

            selectAltAnlagenWerkstaette01,
            selectAltAnlagenWerkstaette08,

            gesamtFertigungspersonal,
            gesamtPersonalentwicklung,
            gesamtGehaltsaufschlag,
            gesamtInvestitionenBGA,

            inputDarlehenS,
            inputDarlehenM,
            inputDarlehenL,
            inputFestgeldDarlehen,
            inputDividenden
        FROM turns
        WHERE game_id = :game_id AND team_name = :team AND turn_number = :period
        """)

        result = self.session.execute(query, {'game_id': game_id, 'team': team, 'period': period}).fetchone()
        self.session.close()

        if result:
            # Assign the results to the respective variables
            mDec_SOLID = result[:9]
            mDec_IDEAL = result[9:17]
            mDec_GESAMT = result[17:21]
            pDec_SOLID = result[21:24]
            pDec_IDEAL = result[24:27]
            pAll_TA_neu = result[27:29]
            pAll_TA_alt = result[29:31]
            pDec_HR = result[31:35]
            fDec_FIN = result[35:40]

            return mDec_SOLID, mDec_IDEAL, mDec_GESAMT, pDec_SOLID, pDec_IDEAL, pAll_TA_neu, pAll_TA_alt, pDec_HR, fDec_FIN
        else:
            return None, None, None, None, None, None, None, None, None

# Example usage
db_url = 'mysql+pymysql://root@localhost/gamesimulationdb'
input_handler = InputHandler(db_url)
game_id = 13
team = 'testTeam'
period = 0
mDec_SOLID, mDec_IDEAL, mDec_GESAMT, pDec_SOLID, pDec_IDEAL, pAll_TA_neu, pAll_TA_alt, pDec_HR, fDec_FIN = input_handler.load_decision_data(game_id, team, period)

# Print the returned data
print("mDec_SOLID:", mDec_SOLID)
print("mDec_IDEAL:", mDec_IDEAL)
print("mDec_GESAMT:", mDec_GESAMT)
print("pDec_SOLID:", pDec_SOLID)
print("pDec_IDEAL:", pDec_IDEAL)
print("pAll_TA_neu:", pAll_TA_neu)
print("pAll_TA_alt:", pAll_TA_alt)
print("pDec_HR:", pDec_HR)
print("fDec_FIN:", fDec_FIN)


class DataProcessor:
    def __init__(self):
        # Initialization code here
        pass

    def process_decisions(self, decisions):
        # Code to process the decisions
        pass

    # Additional methods for different processing tasks


class OutputHandler:
    def __init__(self):
        # Initialization code here
        pass

    def write_results(self, data, file_path):
        # Code to write results to Excel files
        pass
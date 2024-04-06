#--------##--------##--------##--------##--------##--------##--------##--------#
# General Management Simulation MK_GMS_Pro
# Auswertungsprogramm: Unternehmenssimulation - Grafiken
#                      2. Fertigung / HR / Finanzen
#--------##--------##--------##--------##--------##--------##--------##--------#

#--------##--------##--------##--------##--------##--------##--------##--------#
# Simulationsumgebung
#--------##--------##--------##--------##--------##--------##--------##--------#
# IPython magic commands
from IPython import get_ipython
get_ipython().run_line_magic('clear','')
get_ipython().run_line_magic('reset', '-f')
# get_ipython().run_line_magic('precision', '%.4f')

#-- simulierte Periode
PERIOD = 1

#-- Name des Planspiels
GMS_NAME      = 'Pro021'
# GMS_NAME      = 'WPM21B'

#-- Version des Planspiels
GMS_VERSION   = 'GMS_Pro_2.1'

#-- Setup-Datei
SETUP_FILE    = 'MK_GMS_Pro-Setup.npz'

#-- Haupt-Verzeichnis des Planspiels
# MAIN_DIR      = 'C:/Users/MKalt/Documents/!PlanSpiele/'
MAIN_DIR      = 'C:/Users/Ich/Documents/!1 Vorlesungen/!PlanSpiele/'
#-- Unter-Verzeichnis für Planspiel-Ressourcen
SUB_DIR       = '!GMS_Versions'
#-- Unter-Verzeichnis für Planspiel-Szenario
SCEN_DIR      = 'Szenario'
#-- Ziel-Verzeichnis für Planspiel-Dateien
GMS_DIR       = '!GMS_Ordner'

#-- Planspiel-Verzeichnis
GMS_directory = MAIN_DIR + GMS_DIR + '/' + GMS_NAME+'/'
print('Planspiel-Verzeichnis')
print(GMS_directory)

#--------##--------##--------##--------#
#-- Lade Packages/Libraries/Module
import sys
version_dir = MAIN_DIR + SUB_DIR + '/' + GMS_VERSION + '/'
print(version_dir)
sys.path.append(version_dir)

# from openpyxl import load_workbook

import pandas   as pd
import numpy    as np
import plotnine as p9

np.set_printoptions(precision=4, suppress=True)

#--------##--------##--------##--------#
#-- Lade Setup-Daten
with np.load(GMS_directory + SETUP_FILE) as setup:
    gms_numbers = setup['gms_numbers']
    gms_files   = setup['gms_files']
del(setup)

#--------##--------##--------##--------#
#-- KONSTANTEN
#---- Anzahl Unternehmen
NUM_COMPANIES  = gms_numbers[0]
num_companies0 = NUM_COMPANIES

#---- Anzahl Perioden
# MAX_PERIODS    = 10
NUM_PERIODS    = gms_numbers[1]
#---- Perioden-Vorlauf
OFFSET         = gms_numbers[2]

#---- Anzahl Märkte
# Markt 0: SOLID - Inland
# Markt 1: SOLID - Ausland
# Markt 2: IDEAL - Inland
# Markt 3: IDEAL - Ausland
NUM_MARKETS    = gms_numbers[3]
#---- Periode der Marktaktivierung
MARKET_0       = gms_numbers[4]
MARKET_1       = gms_numbers[5]
IDEAL_RD       = gms_numbers[8]
MARKET_2       = gms_numbers[6]
MARKET_3       = gms_numbers[7]

#---- Anzahl Werkstätten (production cells) für Maschinen
NUM_CELLS      = gms_numbers[9]
#---- bilanzielle Nutzungsdauer (useful life) der Werkstätten-Plätze (cells)
UL_CELLS       = gms_numbers[10]

#---- Kosten für Branchen- und Marktberichte
COST_INDUSTRY_REPORT = gms_numbers[11]
COST_MARKET_REPORT = gms_numbers[12]
del(gms_numbers, NUM_MARKETS)
del(NUM_CELLS, UL_CELLS)
del(COST_INDUSTRY_REPORT, COST_MARKET_REPORT)

#--------##--------##--------##--------#
#-- Verzeichnisse
#---- Szenario-Verzeichnis
scenario_dir  = version_dir + SCEN_DIR + '/'

#---- Unter-Verzeichnisse des Planspiels für jedes Unternehmen
company_dir = []
for co in range(NUM_COMPANIES):
    company_dir.append(GMS_directory+f'U{co+1:0>2d}/')

#--------##--------##--------##--------#
#-- Dateien
#---- Szenario-Datei
SCENARIO_FILE    = gms_files[0]
#---- Unternehmens-Datei
COMPANY_FILE     = gms_files[1]
#-- Informations-Master-Datei (Konjunktur- und Marktberichte)
INFO_FILE        = gms_files[2]
del(gms_files)


#--------##--------##--------##--------##--------##--------##--------##--------#
# Lade Unternehmens-Daten
#--------##--------##--------##--------##--------##--------##--------##--------#
with np.load(GMS_directory + COMPANY_FILE, allow_pickle=True) as co_file:
    mDec_SOLID_h  = co_file['mDec_SOLID']
    mDec_IDEAL_h  = co_file['mDec_IDEAL']
    mDec_GESAMT_h = co_file['mDec_GESAMT']
    mMix_SOLID_h  = co_file['mMix_SOLID']
    cSat_SOLID_h  = co_file['cSat_SOLID']
    mMix_IDEAL_h  = co_file['mMix_IDEAL']
    cSat_IDEAL_h  = co_file['cSat_IDEAL']
    pDec_SOLID_h  = co_file['pDec_SOLID']
    pDec_IDEAL_h  = co_file['pDec_IDEAL']
    pRes_TA_h     = co_file['pRes_TA']
    pDec_HR_h     = co_file['pDec_HR']
    pRes_HR_h     = co_file['pRes_HR']
    pRes_costs_h  = co_file['pRes_costs']
    fDec_FIN_h    = co_file['fDec_FIN']
    fRes_COMP_h   = co_file['fRes_COMP']
del(co_file)


#--------##--------##--------##--------##--------##--------#
# Datenbereitstellung
#--------##--------##--------##--------##--------##--------#
# Querschnitt-Grafiken (cross sectional)
choice_CS = [0, 1, 2, 3, 4, 5, 13, 14, 17, 19, 20]
# choice_CS = []

if PERIOD < MARKET_2:
    try:
        choice_CS.remove(4)
    except:
        pass
    # else:
    #     choice_CS.remove(4)

    try:
        choice_CS.remove(5)
    except:
        pass
    # else:
    #     choice_CS.remove(5)

    try:
        choice_CS.remove(7)
    except:
        pass
    # else:
    #     choice_CS.remove(7)
        
# Längsschnitt-Grafiken (time series)
choice_TS = [10, 11, 14, 16, 17, 18]
choice_TS = []

# data frame: Produktion / HR / Finanzen
#  0 Technische Anlagen    - Auslastung
#  1 Fertigungsmitarbeiter - Auslastung
#  2 SOLID - Herstellkosten
#  3 SOLID - Selbstkosten
#  4 IDEAL - Herstellkosten
#  5 IDEAL - Selbstkosten
#  6 Fertigungsmenge SOLID (Ist - Plan)
#  7 Fertigungsmenge IDEAL (Ist - Plan)
#  8 Fertigungspersonal    (Ist - Plan)
#  9 Fertigungskapazität   (Ist)
# 10 Fertigungspersonal    (Ist)
# 11 Personalentwicklungsausgaben
# 12 Gehaltsaufschlag  (freiwillig)
# 13 Arbeitgeber-Image
# 14 Mitarbeitermotivation
# 15 Fluktuation/Fehlzeiten
# 16 Mitarbeiterproduktivität
# 17 Liquiditätssteuerung
# 18 Betriebsergebnis
# 19 Periodenergebnis
# 20 Eigenkapital
# 21 Rating: Zinsaufschlag

variable = np.array(
    [['Technische Anlagen    - Auslastung', '{:.2%}'  ],
     ['Fertigungsmitarbeiter - Auslastung', '{:.2%}'  ],
     ['SOLID - Herstellkosten            ', '{:.1f}'  ],
     ['SOLID - Selbstkosten              ', '{:.1f}'  ],
     ['IDEAL - Herstellkosten            ', '{:.1f}'  ],
     ['IDEAL - Selbstkosten              ', '{:.1f}'  ],
     ['Fertigungsmenge SOLID (Ist - Plan)', '{:+.0f}' ],
     ['Fertigungsmenge IDEAL (Ist - Plan)', '{:+.0f}' ],
     ['Fertigungspersonal    (Ist - Plan)', '{:+.0f}' ],
     ['Fertigungskapazität   (Ist)       ', '{:.0f}'  ],
     ['Fertigungspersonal    (Ist)       ', '{:.0f}'  ],
     ['Personalentwicklungsausgaben      ', '{:.0f}'  ],
     ['Gehaltsaufschlag  (freiwillig)    ', '{:.2%}'  ],
     ['Arbeitgeber-Image                 ', '{:+.2f}' ],
     ['Mitarbeitermotivation             ', '{:+.2f}' ],
     ['Fluktuation/Fehlzeiten            ', '{:.2%}'  ],
     ['Mitarbeiterproduktivität          ', '{:+.2%}' ],
     ['Liquidität/Kontokorrentkredit     ', '{:.0f}'  ],
     ['Betriebsergebnis                  ', '{:.0f}'  ],
     ['Periodenergebnis                  ', '{:.0f}'  ],
     ['Eigenkapital                      ', '{:.0f}'  ],
     ['Rating: Zinsaufschlag             ', '{:.2%}'  ]])

company = []
for co in range(NUM_COMPANIES):
    company.append(f'U{co+1:0>2d}')

data_ProdFin = np.stack((pRes_TA_h   [ 1, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_HR_h   [12, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_costs_h[ 0, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_costs_h[ 1, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_costs_h[ 2, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_costs_h[ 3, :, OFFSET:PERIOD+OFFSET+1],
                        (pDec_SOLID_h[ 3, :, OFFSET:PERIOD+OFFSET+1]
                       - pDec_SOLID_h[ 0, :, OFFSET:PERIOD+OFFSET+1]),
                        (pDec_IDEAL_h[ 3, :, OFFSET:PERIOD+OFFSET+1]
                       - pDec_IDEAL_h[ 0, :, OFFSET:PERIOD+OFFSET+1]),
                        (pRes_HR_h   [ 1, :, OFFSET:PERIOD+OFFSET+1]
                       - pDec_HR_h   [ 0, :, OFFSET:PERIOD+OFFSET+1]),
                         pRes_TA_h   [ 0, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_HR_h   [ 1, :, OFFSET:PERIOD+OFFSET+1],
                         pDec_HR_h   [ 1, :, OFFSET:PERIOD+OFFSET+1],
                         pDec_HR_h   [ 2, :, OFFSET:PERIOD+OFFSET+1],
                         pRes_HR_h   [16, :, OFFSET:PERIOD+OFFSET+1]-100,
                         pRes_HR_h   [17, :, OFFSET:PERIOD+OFFSET+1]-100,
                        (pRes_HR_h   [19, :, OFFSET:PERIOD+OFFSET+1]
                       + pRes_HR_h   [20, :, OFFSET:PERIOD+OFFSET+1]),
                         pRes_HR_h   [21, :, OFFSET:PERIOD+OFFSET+1]-1,
                        (fDec_FIN_h  [ 7, :, OFFSET:PERIOD+OFFSET+1]
                       - fDec_FIN_h  [ 6, :, OFFSET:PERIOD+OFFSET+1]),
                         fRes_COMP_h [ 0, :, OFFSET:PERIOD+OFFSET+1],
                         fRes_COMP_h [ 1, :, OFFSET:PERIOD+OFFSET+1],
                        (fRes_COMP_h [ 7, :, OFFSET:PERIOD+OFFSET+1]
                       - fRes_COMP_h [ 6, :, OFFSET:PERIOD+OFFSET+1]),
                         fRes_COMP_h [ 8, :, OFFSET:PERIOD+OFFSET+1]))


#--------##--------##--------##--------##--------##--------#
# Graphenerzeugung
#--------##--------##--------##--------##--------##--------#

#--------##--------##--------##--------#
# Querschnittdaten (cross sectional): Säulendiagramm
df_CS_ProdFin = pd.DataFrame(data_ProdFin[:, :, PERIOD].T, columns = variable[:, 0], index = company)
    
for c in choice_CS:
    gms_plot = (p9.ggplot(df_CS_ProdFin)
              + p9.aes(x='company', y=variable[c, 0], fill='company')
              + p9.geom_col()
              + p9.geom_text(mapping=p9.aes(label=variable[c, 0]), va='bottom', format_string=variable[c, 1])
              + p9.ggtitle(variable[c, 0])
              + p9.scale_fill_brewer(type='qual', palette='Set1')
              + p9.theme_grey()
              + p9.xlab('')
              + p9.ylab('')
              )
    print(gms_plot)

#--------##--------##--------##--------#
# Längsschnittdaten (tme series): Liniendiagramm
for c in choice_TS:
    if PERIOD>=2:
        df_TS_ProdFin = pd.DataFrame(data_ProdFin[c, :, :].T, columns = company)
        df_TS_ProdFin['period'] = df_TS_ProdFin.index
        df_TS_ProdFin = pd.melt(df_TS_ProdFin, id_vars='period')
        df_TS_ProdFin = df_TS_ProdFin.rename(columns={'variable': 'company'}) 
        
        gms_plot = (p9.ggplot(df_TS_ProdFin)
                  + p9.aes(x='period', y='value', colour='company')
                  + p9.geom_line(size=2)
                  + p9.ggtitle(variable[c, 0])
                  + p9.scale_colour_brewer(type='qual', palette='Set1')
                  + p9.theme_grey()
                  + p9.xlab('')
                  + p9.ylab('')
                  )
        print(gms_plot)
        del(df_TS_ProdFin)
    
# Lösche temporäre und nicht mehr benötigte  Variablen
del(version_dir, scenario_dir, company_dir)
del(mDec_SOLID_h, mMix_SOLID_h, cSat_SOLID_h, pDec_SOLID_h,
    mDec_IDEAL_h, mMix_IDEAL_h, cSat_IDEAL_h, pDec_IDEAL_h, mDec_GESAMT_h,
    pRes_TA_h, pDec_HR_h, pRes_HR_h, pRes_costs_h,
    fDec_FIN_h, fRes_COMP_h)
del(co, num_companies0)
del(data_ProdFin, variable, company,)
del(df_CS_ProdFin, choice_CS, choice_TS, c, gms_plot)
del(MARKET_0, MARKET_1, MARKET_2, MARKET_3, IDEAL_RD)

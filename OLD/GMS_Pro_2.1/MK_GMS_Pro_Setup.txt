#--------##--------##--------##--------##--------##--------#
# General Management Simulation MK_GM_Pro
# Vorprogramm: Einrichten der Unternehmenssimulation
#              Bereitstellung der Szenario-Dateien
#--------##--------##--------##--------##--------##--------#

#--------##--------##--------##--------##--------##--------##--------##--------#
# Simulationsumgebung
#--------##--------##--------##--------##--------##--------##--------##--------#
# IPython magic commands
from IPython import get_ipython
get_ipython().run_line_magic('clear','')
get_ipython().run_line_magic('reset', '-f')
# get_ipython().run_line_magic('precision', '%.4f')

#-- Name des Planspiels
GMS_NAME      = 'Pro021'
# GMS_NAME      = 'WPM21B'

#-- Anzahl Unternehmen
NUM_COMPANIES =  6

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
#-- KONSTANTEN
#---- Anzahl Perioden
MAX_PERIODS   = 10
NUM_PERIODS   =  8
#---- Perioden-Vorlauf
OFFSET        =  2

#---- Anzahl Märkte
# Markt 0: SOLID - Inland
# Markt 1: SOLID - Ausland
# Markt 2: IDEAL - Inland
# Markt 3: IDEAL - Ausland
NUM_MARKETS   =  4
#---- Periode der Marktaktivierung
MARKET_0      =  0
MARKET_1      =  3
IDEAL_RD      =  2
MARKET_2      =  4
MARKET_3      =  6

#---- Anzahl Werkstätten (production cells) für Maschinen
NUM_CELLS     =  8
#---- bilanzielle Nutzungsdauer (useful life) der Werkstätten-Plätze (cells)
UL_CELLS      = 25

#---- Kosten für Branchen- und Marktberichte
COST_INDUSTRY_REPORT = 200
COST_MARKET_REPORT   = 200

#--------##--------##--------##--------#
# Lade Packages/Libraries/Module
import sys
version_dir = MAIN_DIR + SUB_DIR + '/' + GMS_VERSION + '/'
sys.path.append(version_dir)

import os
import shutil

from openpyxl import load_workbook

import numpy              as np

import MK_GMS_Pro_Modules as mod

np.set_printoptions(precision=4, suppress=True)

#--------##--------##--------##--------#
#-- Verzeichnisse
#---- Szenario-Verzeichnis
scenario_dir  = version_dir + SCEN_DIR + '/'
print('Szenario-Verzeichnis')
print(scenario_dir)

#---- Entscheidungs-Verzeichnis
decision_dir  = GMS_directory + 'Decisions/'
print('Entscheidungs-Verzeichnis')
print(decision_dir)

#---- Unter-Verzeichnisse des Planspiels für jedes Unternehmen
company_dir = []
for comp in range(NUM_COMPANIES):
    company_dir.append(GMS_directory+f'U{comp+1:0>2d}/')
print('Unternehmens-Verzeichnisse')
print(company_dir)

#-- Erzeuge Verzeichnisse
try:
    #---- Planspiel-Verzeichnis
    os.mkdir(GMS_directory)
except:
    shutil.rmtree(GMS_directory)
    #---- Planspiel-Verzeichnis
    os.mkdir(GMS_directory)

#---- Entscheidungs-Verzeichnis
os.mkdir(decision_dir)

#---- Unter-Verzeichnisse des Planspiels für jedes Unternehmen
for comp in range(NUM_COMPANIES):
    os.mkdir(company_dir[comp])
del(comp)

#--------##--------##--------##--------#
#-- Dateien
#---- Szenario-Datei
SCENARIO_XLS_FILE = 'MK_GMS_Pro-Szenario.xlsx'
SCENARIO_FILE     = 'MK_GMS_Pro-Szenario.npz'

#-- Unternehmens-Datei
COMPANY_XLS_FILE  = 'MK_GMS_Pro-Unternehmen.xlsx'
COMPANY_FILE      = 'MK_GMS_Pro-Unternehmen.npz'

#-- Informations-Master-Datei (Konjunktur- und Marktberichte)
INFO_FILE         = 'MK_GMS_Pro-Informationen.xlsx'


#--------##--------##--------##--------##--------##--------##--------##--------#
# Speichere Planspiel-Setup
#--------##--------##--------##--------##--------##--------##--------##--------#
np.savez(GMS_directory + SETUP_FILE,
         gms_numbers = np.array([NUM_COMPANIES,
                                 NUM_PERIODS, OFFSET,
                                 NUM_MARKETS,
                                 MARKET_0, MARKET_1, MARKET_2, MARKET_3, IDEAL_RD,
                                 NUM_CELLS, UL_CELLS,
                                 COST_INDUSTRY_REPORT, COST_MARKET_REPORT]),
         gms_files   = np.array([SCENARIO_FILE, COMPANY_FILE, INFO_FILE]))
del(MARKET_0, MARKET_1, MARKET_2, MARKET_3, IDEAL_RD)
del(NUM_MARKETS, NUM_CELLS, UL_CELLS)
del(COST_INDUSTRY_REPORT, COST_MARKET_REPORT)


#--------##--------##--------##--------##--------##--------##--------##--------#
# Szenario-Daten
#--------##--------##--------##--------##--------##--------##--------##--------#
#-- Excel Zellen der Szenario-Daten
#-- 1. mehrzeilige Tabellen
#--------##--------##--------##--------#
# Worksheet:   'Volkswirtschaft'
# Finanzen:     Wechselkurs, Zahlungseingang, Ertragsteuersatz 
# Zinsen:       Festgeld, Kontokorrent, 'S'-Kredit, 'M'-Darlehen, 'L'-Darlehen
#--------##--------##--------##--------#
# Worksheet:   'Absatzmärkte'
# Sondermarkt:  Preis, Menge 
# Marktvol:     SOLID-Inland, SOLID-Ausland, IDEAL-Inland, IDEAL-Ausland 
#--------##--------##--------##--------#
# Worksheet:   'Vorräte'
# MengeHStoff:  Mengenstaffel Hilfsstoffe 'H'
# MengeMat1     Mengenstaffel Vorprodukt '1' (SOLID)
# MengeMat2     Mengenstaffel Vorprodukt '2' (IDEAL)
# PreisHStoff:  Preisstaffel  Hilfsstoffe 'H':
#                   Express, Staffel 1-4
# PreisMat1:    Preisstaffel  Vorprodukt '1' (SOLID):
#                   Express, Staffel 1-4
# PreisMat2:    Preisstaffel  Vorprodukt '2' (IDEAL):
#                   Express, Staffel 1-4
# LagerMat:     Lagerkosten-Vorprodukt:
#                   Hilfsstoffe 'H', Vorprodukt '1' (SOLID), Vorprodukt '2' (IDEAL)
# LagerFE:      Lagerkosten-Fertigerzeugnisse:
#                   SOLID-Inland, SOLID-Ausland, IDEAL-Inland, IDEAL-Ausland
# TransportFE:  Transportk.-Fertigerzeugnisse:
#                   SOLID-Inland, SOLID-Ausland, IDEAL-Inland, IDEAL-Ausland
#--------##--------##--------##--------#
# Worksheet:   'Fertigung'
# BedarfSOLID:  Hilfsstoffe 'H', Vorprodukt '1' (SOLID), Personal, Maschinen
# BedarfIDEAL:  Hilfsstoffe 'H', Vorprodukt '2' (IDEAL), Personal, Maschinen
#--------##--------##--------##--------#
# Worksheet:   'Personal'
# Gehalt:       Basisgehälter: Fertigung, Vertrieb, Verwaltung 
# LohnNK:       Nebenkosten(%), Ü-Obergrenze, Ü-Fixkosten, Ü-Aufschlag1, Ü-Aufschlag2,
#               EinstellMax, Einstellungskosten, EntlassMax, Entlassungskosten
# Gehalt:       Basisgehälter: Fertigung, Vertrieb, Verwaltung 
# eMA:          erwarteter Gehaltsaufschlag/Einstellungsquote (Konkurrenz)
#--------##--------##--------##--------#
# Worksheet:   'Materielles AV'
# AV_GG:        Grundstücke/Gebäude: Investitionen, Instandhaltung,
#                                    AK-Werkstätte
# AnlagenS:     TechAnlagen Typ S:   Anschaffungskosten, Instandhaltung,
#                                    Fixkosten, Kapazitäten, Verkauf,
#                                    Nutzungsdauer
# AnlagenM:     TechAnlagen Typ M:   Anschaffungskosten, Instandhaltung,
#                                    Fixkosten, Kapazitäten, Verkauf,
#                                    Nutzungsdauer
# AnlagenL:     TechAnlagen Typ L:   Anschaffungskosten, Instandhaltung,
#                                    Fixkosten, Kapazitäten, Verkauf,
#                                    Nutzungsdauer
info_list = [['Finanzen'   , 'Volkswirtschaft', 'F', 'R', 10, 12],
             ['Zinsen'     , 'Volkswirtschaft', 'F', 'R', 16, 21],
             ['Sondermarkt', 'Absatzmärkte'   , 'F', 'R',  5,  6],
             ['MarktVol'   , 'Absatzmärkte'   , 'F', 'R',  9, 24],
             ['PreisHStoff', 'Vorräte'        , 'F', 'R',  5,  9],
             ['PreisMat1'  , 'Vorräte'        , 'F', 'R', 11, 16],
             ['PreisMat2'  , 'Vorräte'        , 'F', 'R', 18, 23],
             ['LagerMat'   , 'Vorräte'        , 'F', 'R', 27, 29],
             ['LagerFE'    , 'Vorräte'        , 'F', 'R', 31, 34],
             ['TransportFE', 'Vorräte'        , 'F', 'R', 38, 47],
             ['BedarfSOLID', 'Fertigung'      , 'F', 'R',  5,  8],
             ['BedarfIDEAL', 'Fertigung'      , 'F', 'R', 11, 14],
             ['Gehalt'     , 'Personal'       , 'F', 'R',  5,  7],
             ['LohnNK'     , 'Personal'       , 'F', 'R', 12, 20],
             ['eMA'        , 'Personal'       , 'F', 'R', 23, 24],
             ['AV_GG'      , 'Materielles AV' , 'F', 'R',  5,  7],
             ['AnlagenS'   , 'Materielles AV' , 'F', 'R', 11, 16],
             ['AnlagenM'   , 'Materielles AV' , 'F', 'R', 18, 23],
             ['AnlagenL'   , 'Materielles AV' , 'F', 'R', 25, 30]]
szenario_bereiche = mod.xls_range_dict(info_list)

#-- Lade Szenario-Daten
xlsWB  = load_workbook(
    filename = scenario_dir + SCENARIO_XLS_FILE,
    data_only=True)

szenario = {}
for key in szenario_bereiche:
    xlsWS = xlsWB[szenario_bereiche[key][0]]
    cell_range = szenario_bereiche[key][1]
    cell_values = np.zeros((len(cell_range), MAX_PERIODS+OFFSET+1))
    for ndx in range(len(cell_range)):
        cell_values[ndx] = mod.read_XLS_range(cell_range[ndx], xlsWS)
    szenario[key] = cell_values
del(key, ndx)

#-- Excel Zellen der Szenario-Daten
#-- 2. einzeilige Tabellen
#--------##--------##--------##--------#
# Worksheet:   'Volkswirtschaft'
# Preisindex:   Preisindex
#--------##--------##--------##--------#
# Worksheet:   'Absatzmärkte'
# eQI_SOLID:    erwarteter Qualitätsindex (Konkurrenz)
# eQI_IDEAL:    erwarteter Qualitätsindex (Konkurrenz)
#--------##--------##--------##--------#
# Worksheet:   'Vorräte'
# MengeHStoff:  Mengenstaffel: Hilfsstoffe 'H'
# MengeMat1:    Mengenstaffel: Vorprodukt '1' (SOLID)
# MengeMat2:    Mengenstaffel: Vorprodukt '2' (IDEAL)
#--------##--------##--------##--------#
# Worksheet:   'Materielles AV'
# AV_BGA:       Betriebs-/Geschäftsausstattung: Investitionen
xlsWS = xlsWB['Volkswirtschaft']
cell_range = ('F9' , 'R9')
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['Preisindex'] = np.array(cell_values)

xlsWS = xlsWB['Absatzmärkte']
cell_range = ('F30', 'R30')
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['eQI_SOLID'] = np.array(cell_values)

cell_range = ('F38', 'R38')
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['eQI_IDEAL'] = np.array(cell_values)

xlsWS = xlsWB['Vorräte']
cell_range = ('D5' , 'D9' )
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['MengeHStoff'] = np.array(cell_values)

xlsWS = xlsWB['Vorräte']
cell_range = ('D11', 'D16')
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['MengeMat1'] = np.array(cell_values)

cell_range = ('D18', 'D23')
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['MengeMat2'] = np.array(cell_values)

xlsWS = xlsWB['Materielles AV']
cell_range = ('F33' , 'R33')
cell_values = mod.read_XLS_range(cell_range, xlsWS)
szenario['AV_BGA'] = np.array(cell_values)

#-- Speichere Szenario-Arrays in binary-Format
np.savez(GMS_directory + SCENARIO_FILE,
            Preisindex  = szenario['Preisindex'],
            Finanzen    = szenario['Finanzen'],
            Zinsen      = szenario['Zinsen'],
            Sondermarkt = szenario['Sondermarkt'],
            MarktVol    = szenario['MarktVol'],
            eQI_SOLID   = szenario['eQI_SOLID'],      
            eQI_IDEAL   = szenario['eQI_IDEAL'],        
            MengeHStoff = szenario['MengeHStoff'],
            PreisHStoff = szenario['PreisHStoff'],
            MengeMat1   = szenario['MengeMat1'],
            PreisMat1   = szenario['PreisMat1'],
            MengeMat2   = szenario['MengeMat2'],
            PreisMat2   = szenario['PreisMat2'],
            LagerMat    = szenario['LagerMat'],
            LagerFE     = szenario['LagerFE'],
            TransportFE = szenario['TransportFE'],
            BedarfSOLID = szenario['BedarfSOLID'],
            BedarfIDEAL = szenario['BedarfIDEAL'],
            Gehalt      = szenario['Gehalt'],
            LohnNK      = szenario['LohnNK'],
            eMA         = szenario['eMA'],
            AV_GG       = szenario['AV_GG'],
            AnlagenS    = szenario['AnlagenS'],
            AnlagenM    = szenario['AnlagenM'],
            AnlagenL    = szenario['AnlagenL'],
            AV_BGA      = szenario['AV_BGA'])
# for key in szenario:
#     print(key)
#     print(szenario[key])

#-- Lösche temporäre und nicht mehr benötigte  Variablen    
del(szenario_bereiche, xlsWB, xlsWS, cell_range, cell_values, szenario)
del(SCENARIO_XLS_FILE)


#--------##--------##--------##--------##--------##--------##--------##--------#
# Unternehmens-Daten
#--------##--------##--------##--------##--------##--------##--------##--------#
#-- Excel Zellen der Unternehmens-Daten (exemplarisch für Unternehmen U01)
#--------##--------##--------##--------#
# Worksheet:   'Marketing'
#-- mehrzeilige Tabellen
# mDec_SOLID:  Preis Inland, Preis Ausland, Technik, Haptik,
#              Werbung Inland, Werbung Ausland, Liefermenge Ausland,
#              Marktbericht, Liefermenge Sondermarkt
# mDec_IDEAL:  Preis Inland, Preis Ausland, Technik, Haptik,
#              Werbung Inland, Werbung Ausland, Liefermenge Ausland,
#              Marktbericht
# mDec_GESAMT: PR, Vertriebspersonal Inland,
#              Vertriebspersonal Ausland, Branchenbericht
# mMix_SOLID:  Marktgröße F&E-Technik, Marktgröße F&E-Haptik,
#              kum.F&E-Technik, kum.F&E-Haptik,
#              Index-Technik, Index-Haptik, Produkt-Index-SOLID
#              Werbewirkung - Inland, Werbewirkung - Ausland
#              Vertriebswirkung - Inland, Vertriebswirkung - Ausland
#              Markenmanagement (Wirkung),
#              Markenindex - Inland, Markenindex - Ausland
#              Lagerbestand - Inland, Lagerbestand - Ausland
# cSat_SOLID:  Preisstabilität - Inland,
#              Absatz - Inland, Nachfrage - Inland,
#              Zufriedenheit - Inland, CS-Index - Inland
#              Preisstabilität - Ausland,
#              Absatz - Ausland, Nachfrage - Ausland
#              Zufriedenheit - Ausland, CS-Index - Ausland
# mMix_IDEAL:  Marktgröße F&E-Technik, Marktgröße F&E-Haptik,
#              kum.F&E-Technik, kum.F&E-Haptik,
#              Index-Technik, Index-Haptik, Produkt-Index-IDEAL
#              Werbewirkung - Inland, Werbewirkung - Ausland
#              Vertriebswirkung - Inland, Vertriebswirkung - Ausland
#              Markenmanagement (Wirkung),
#              Markenindex - Inland, Markenindex - Ausland
#              Lagerbestand - Inland, Lagerbestand - Ausland
# cSat_IDEAL:  Preisstabilität - Inland,
#              Absatz - Inland, Nachfrage - Inland,
#              Zufriedenheit - Inland, CS-Index - Inland
#              Preisstabilität - Ausland,
#              Absatz - Ausland, Nachfrage - Ausland
#              Zufriedenheit - Ausland, CS-Index - Ausland
info_list = [['mDec_SOLID' , 'Marketing', 'D', 'P',  5, 13],
             ['mDec_IDEAL' , 'Marketing', 'D', 'P', 16, 23],
             ['mDec_GESAMT', 'Marketing', 'D', 'P', 26, 29],
             ['mMix_SOLID' , 'Marketing', 'D', 'P', 32, 47],
             ['cSat_SOLID' , 'Marketing', 'D', 'P', 50, 59],
             ['mMix_IDEAL' , 'Marketing', 'D', 'P', 62, 77],
             ['cSat_IDEAL' , 'Marketing', 'D', 'P', 80, 89]]
xls_bereiche = mod.xls_range_dict(info_list)

#-- Lade Unternehmens-Daten
xlsWB  = load_workbook(
    filename = scenario_dir + COMPANY_XLS_FILE,
    data_only=True)

comp_data = {}
for key in xls_bereiche:
    xlsWS = xlsWB[xls_bereiche[key][0]]
    cell_range = xls_bereiche[key][1]
    cell_values = np.empty((len(cell_range), MAX_PERIODS+OFFSET+1), dtype=object)
    for ndx in range(len(cell_range)):
        cell_values[ndx] = mod.read_XLS_range(cell_range[ndx], xlsWS)
    comp_data[key] = cell_values
del(key, ndx)

#-- Initialisiere Markt-Historie
mDec_SOLID_h  = np.zeros((
    comp_data['mDec_SOLID'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
mDec_IDEAL_h  = np.zeros((
    comp_data['mDec_IDEAL'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
mDec_GESAMT_h = np.zeros((
    comp_data['mDec_GESAMT'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
mMix_SOLID_h   = np.zeros((
    comp_data['mMix_SOLID'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
cSat_SOLID_h   = np.zeros((
    comp_data['cSat_SOLID'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
mMix_IDEAL_h   = np.zeros((
    comp_data['mMix_IDEAL'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
cSat_IDEAL_h   = np.zeros((
    comp_data['cSat_IDEAL'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))

#--------##--------##--------##--------#
# Worksheet:   'Fertigung' (production)
#-- mehrzeilige Tabellen
# pDec_SOLID:  Planmenge - SOLID, Hilfsstoffe 'H', Vorprodukt 'S' (SOLID),
#              Istmenge - SOLID
# pDec_IDEAL:  Planmenge - IDEAL, Hilfsstoffe 'H', Vorprodukt 'I' (IDEAL),
#              Istmenge - IDEAL
# pRes_TA:     Fertigungskapazität, TA-Auslastung, TA-Investitionen,
#              Anzahl TA - Typen S/M/L
# pDec_HR:     Fertigungspersonal  (Planbestand), Personalentwicklung,
#              Gehaltsaufschlag, Investitionen in die BGA,
# pRes_HR:     Entgeltpolitik-Faktor2,
#              Fertigungspersonal  (Ist-Bestand), Einst./Entl.
#              Einstellungspolitik-Faktor1 / -Faktor2
#              Personalbestand (Gesamt)
#              Arbeitsplatzausstattung-Faktor1 / -Faktor2,
#              Entgeltpolitik (Wirkung), Einstellungspolitik (Wirkung),
#              Personalentwicklung (Wirkung), Arbeitsplatzausstattung (Wirkung),
#              MA-Belastung, Arbeitsmarkt-Angebot, Arbeitsmarkt-Produktivität,
#              MA-Produktivität (PE), AG-Image, MA-Motivation,
#              MA-Produktivität (Motiv), MA-Fluktuation, MA-Fehlzeiten
# pRes_costs:  Herstell-/Selbstkosten - SOLID
#              Herstell-/Selbstkosten - IDEAL
info_list = [['pDec_SOLID' , 'Fertigung', 'D', 'P',  5,  8],
             ['pDec_IDEAL' , 'Fertigung', 'D', 'P', 11, 14],
             ['pRes_TA'    , 'Fertigung', 'D', 'P', 17, 19],
             ['pDec_HR'    , 'Fertigung', 'D', 'P', 22, 25],
             ['pRes_HR'    , 'Fertigung', 'D', 'P', 28, 49],
             ['pRes_costs' , 'Fertigung', 'D', 'P', 52, 55]]
xls_bereiche = mod.xls_range_dict(info_list)

#-- Lade Unternehmens-Daten
for key in xls_bereiche:
    xlsWS = xlsWB[xls_bereiche[key][0]]
    cell_range = xls_bereiche[key][1]
    cell_values = np.empty((len(cell_range), MAX_PERIODS+OFFSET+1), dtype=object)
    for ndx in range(len(cell_range)):
        cell_values[ndx] = mod.read_XLS_range(cell_range[ndx], xlsWS)
    comp_data[key] = cell_values
del(key, ndx)

#-- Initialisiere Fertigungs-Historie
pDec_SOLID_h = np.zeros((
    comp_data['pDec_SOLID'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
pDec_IDEAL_h = np.zeros((
    comp_data['pDec_IDEAL'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
pRes_TA_h    = np.zeros((
    comp_data['pRes_TA'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
pDec_HR_h    = np.zeros((
    comp_data['pDec_HR'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
pRes_HR_h    = np.zeros((
    comp_data['pRes_HR'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
pRes_costs_h = np.zeros((
    comp_data['pRes_costs'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))

#--------##--------##--------##--------#
# Worksheet:   'Finanzen'
#-- mehrzeilige Tabellen
# fDec_FIN:    'S'-Darlehen, 'M'-Darlehen, 'L'-Darlehen, Festgeldanlagen,
#              Dividendenausschüttung (Plan), Dividendenausschüttung (Ist),
#              Kontokorrentkredit, Kasse und Bankguthaben
# fRes_COMP:   Betriebsergebnis, Periodenergebnis, NOPAT, EVA, CFO,
#              Anlagevermögen, Fremdkapital, Gesamtkapital,
#              Zinsaufschlag, Rating
info_list = [['fDec_FIN'   , 'Finanzen' , 'D', 'P',  5, 12],
             ['fRes_COMP'  , 'Finanzen' , 'D', 'P', 15, 23]]
xls_bereiche = mod.xls_range_dict(info_list)

#-- Lade Unternehmens-Daten
for key in xls_bereiche:
    xlsWS = xlsWB[xls_bereiche[key][0]]
    cell_range = xls_bereiche[key][1]
    cell_values = np.empty((len(cell_range), MAX_PERIODS+OFFSET+1), dtype=object)
    for ndx in range(len(cell_range)):
        cell_values[ndx] = mod.read_XLS_range(cell_range[ndx], xlsWS)
    comp_data[key] = cell_values
del(key, ndx)

#-- Initialisiere Finanz-Historie
fDec_FIN_h  = np.zeros((
    comp_data['fDec_FIN'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))
fRes_COMP_h  = np.zeros((
    comp_data['fRes_COMP'].shape[0],
    NUM_COMPANIES,
    NUM_PERIODS+OFFSET+1))

#-- Übertrage Daten von U01 auf übrige Unternehmen
for per in range(OFFSET):
    for comp in range(NUM_COMPANIES):
        mDec_SOLID_h[:, comp , per] = \
            comp_data['mDec_SOLID'][:, per]
        mDec_IDEAL_h[:, comp , per] = \
            comp_data['mDec_IDEAL'][:, per]
        mDec_GESAMT_h[:, comp , per] = \
            comp_data['mDec_GESAMT'][:, per]
        mMix_SOLID_h[:, comp , per] = \
            comp_data['mMix_SOLID'][:, per]
        cSat_SOLID_h[:, comp , per] = \
            comp_data['cSat_SOLID'][:, per]
        mMix_IDEAL_h[:, comp , per] = \
            comp_data['mMix_IDEAL'][:, per]
        cSat_IDEAL_h[:, comp , per] = \
            comp_data['cSat_IDEAL'][:, per]

        pDec_SOLID_h[:, comp , per] = \
            comp_data['pDec_SOLID'][:, per]
        pDec_IDEAL_h[:, comp , per] = \
            comp_data['pDec_IDEAL'][:, per]
        pRes_TA_h[:, comp , per] = \
            comp_data['pRes_TA'][:, per]
        pDec_HR_h[:, comp , per] = \
            comp_data['pDec_HR'][:, per]
        pRes_HR_h[:, comp , per] = \
            comp_data['pRes_HR'][:, per]
        pRes_costs_h[:, comp , per] = \
            comp_data['pRes_costs'][:, per]
        
        fDec_FIN_h[:, comp , per] = \
            comp_data['fDec_FIN'][:, per]
        fRes_COMP_h[:, comp , per] = \
            comp_data['fRes_COMP'][:, per]
del(per, comp, comp_data)

#-- Speichere Unternehmens-Daten in binary-Format
np.savez(GMS_directory + COMPANY_FILE,
         # Marketing 
         mDec_SOLID  = mDec_SOLID_h,
         mDec_IDEAL  = mDec_IDEAL_h,
         mDec_GESAMT = mDec_GESAMT_h,
         mMix_SOLID  = mMix_SOLID_h,
         cSat_SOLID  = cSat_SOLID_h,
         mMix_IDEAL  = mMix_IDEAL_h,
         cSat_IDEAL  = cSat_IDEAL_h,
         # Fertigung / Personal / Beschaffung
         pDec_SOLID  = pDec_SOLID_h,  
         pDec_IDEAL  = pDec_IDEAL_h,
         pRes_TA     = pRes_TA_h,
         pDec_HR     = pDec_HR_h,
         pRes_HR     = pRes_HR_h,
         pRes_costs  = pRes_costs_h,
         # Finanzen / Rechnungswesen / Erfolg
         fDec_FIN    = fDec_FIN_h,
         fRes_COMP   = fRes_COMP_h)

#-- Lösche temporäre und nicht mehr benötigte  Variablen    
del(info_list, MAX_PERIODS)
del(xls_bereiche, xlsWB, xlsWS, cell_range, cell_values)
del(mDec_SOLID_h, mDec_IDEAL_h, mDec_GESAMT_h,
    mMix_SOLID_h, cSat_SOLID_h, mMix_IDEAL_h, cSat_IDEAL_h,
    pDec_SOLID_h, pDec_IDEAL_h, pRes_TA_h, pDec_HR_h, pRes_HR_h, pRes_costs_h,
    fDec_FIN_h, fRes_COMP_h)
del(COMPANY_XLS_FILE)
del(version_dir, scenario_dir, company_dir)


#--------##--------##--------##--------##--------##--------##--------##--------#
# Lade Unternehmens-Daten
#--------##--------##--------##--------##--------##--------##--------##--------#
# with np.load(GMS_directory + COMPANY_FILE, allow_pickle=True) as co_file:
#     mDec_SOLID_h  = co_file['mDec_SOLID']
#     mDec_IDEAL_h  = co_file['mDec_IDEAL']
#     mDec_GESAMT_h = co_file['mDec_GESAMT']
#     mMix_SOLID_h  = co_file['mMix_SOLID']
#     cSat_SOLID_h  = co_file['cSat_SOLID']
#     mMix_IDEAL_h  = co_file['mMix_IDEAL']
#     cSat_IDEAL_h  = co_file['cSat_IDEAL']
#     pDec_SOLID_h  = co_file['pDec_SOLID']
#     pDec_IDEAL_h  = co_file['pDec_IDEAL']
#     pRes_TA_h     = co_file['pRes_TA']
#     pDec_HR_h     = co_file['pDec_HR']
#     pRes_HR_h     = co_file['pRes_HR']
#     pRes_costs_h  = co_file['pRes_costs']
#     fDec_FIN_h    = co_file['fDec_FIN']
#     fRes_COMP_h   = co_file['fRes_COMP']


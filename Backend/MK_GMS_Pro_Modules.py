#--------##--------##--------##--------##--------##--------##--------##--------#
# General Management Simulation MK_GM_Pro
# Funktionen / Routinen und Parameter
#--------##--------##--------##--------##--------##--------##--------##--------#
# Lade Packages/Libraries/Module
import numpy  as np

#--------##--------##--------##--------##--------##--------##--------##--------#
# Hilfs-Funktionen
#--------##--------##--------##--------##--------##--------##--------##--------#
# Dictionaries für zu lesenden Excel-Bereiche (zeilenweise)
def xls_range_dict(info_list):
    """erzeuge Dictionary der zu lesenden Excel-Bereiche (zeilenweise)"""

    key_list = []
    value_list = []
    for ndx in range(len(info_list)):
        # Erzeuge dictionary-keys (Bereichsnamen)
        key_list.append(info_list[ndx][0])
        # Berechne Excel-Bereiche (zeilenweise)
        col_beg = info_list[ndx][2]
        col_end = info_list[ndx][3]
        row_beg = info_list[ndx][4]
        row_end = info_list[ndx][5]
        range_tpl = []
        for row in range(row_beg, row_end+1):
            range_tpl.append((col_beg + f'{row}', col_end + f'{row}'))
        range_tpl = tuple(range_tpl)
        # Erzeuge dictionary-values (Excel-Arbeitsblatt und Excel-Bereiche)
        value_list.append((info_list[ndx][1], range_tpl))
    # Erzeuge dictionary
    return {k:v for k,v in zip(key_list, value_list)}

# Moving-Average-Prozesse
def ma_value(val_array, ma_array):
    """berechnet Wert eines moving-average-Prozesses"""

    ma_val = 0
    for ndx in range(len(ma_array)):
        ma_val += ma_array[ndx] * val_array[ndx]
    return ma_val

# Lineare Interpolation der WirkungsFunktionen
def stepwise_linear_function(xyArr, xVal):
    """Stückweise Linearer Wirkungszusammenhang"""
    xArr = xyArr[0]
    yArr = xyArr[1]
    dxArr = np.diff(xArr)
    dyArr = np.diff(yArr)
    mArr = dyArr/dxArr
    xIndex = np.searchsorted(xArr, xVal)
    #
    lNDX = xIndex * (xIndex < xArr.size)
    bSEL = (lNDX != 0)
    lNDX -= 1
    #
    result = ((xVal - xArr[lNDX]) * mArr[lNDX] + yArr[lNDX]) * bSEL + (xIndex == 0) * yArr[0] + (xIndex == xArr.size) * yArr[-1]
    #
    return result


#--------##--------##--------##--------##--------##--------##--------##--------#
# openpyxl Interaktion mit xls-Dateien
#--------##--------##--------##--------##--------##--------##--------##--------#
def flatten_tuple(_tuple):
    """flatten_list: flatten tuple of tuples"""
    if isinstance(_tuple, tuple):
        for x in _tuple:
            yield from flatten_tuple(x)
    else:
        yield _tuple

def read_XLS_cells(cell_tuple, xlsWorkSheet):
    """openpyxl: read values from 1-dim cell tuple"""
    cell_values = []
    for ndx in range(len(cell_tuple)):
        cell_values.append(xlsWorkSheet[cell_tuple[ndx]].value)
    return cell_values

def write_XLS_cells(cell_tuple, cell_values, xlsWorkSheet):
    """openpyxl: write values to 1-dim cell tuple"""
    for ndx in range(len(cell_tuple)):
        xlsWorkSheet[cell_tuple[ndx]].value = cell_values[ndx]
    return

def read_XLS_range(cell_range, xlsWorkSheet):
    """openpyxl: read values from 1-dim cell range"""
    cells = xlsWorkSheet[cell_range[0]:cell_range[1]]
    cells = tuple(flatten_tuple(cells))
    cell_values = []
    for cell in cells:
        cell_values.append(cell.value)
    return cell_values

def write_XLS_range(cell_range, cell_values, xlsWorkSheet):
    """openpyxl: write values to 1-dim cell range"""
    cells = xlsWorkSheet[cell_range[0]:cell_range[1]]
    cells = tuple(flatten_tuple(cells))
    ndx = 0
    for cell in cells:
        cell.value = cell_values[ndx]
        ndx += 1
    return


#--------##--------##--------##--------##--------##--------##--------##--------#
# Marktmodell: Absatzmärkte
#--------##--------##--------##--------##--------##--------##--------##--------#
# Produktqualitäten
def product_quality(rd_inv, rd_hist):
    """Berechnung der Produktqualitäten aus F&E-Investitionen"""

    # benötigt: rd_inv(4x2) in Mio.EUR
    # mDec_SOLID_h[2:4, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]/1000
    # mDec_IDEAL_h[2:4, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]/1000
    
    # benötigt: rd_hist(8x2)
    # mMix_SOLID_h[0:4, co, PERIOD+OFFSET-2:PERIOD+OFFSET]
    # mMix_IDEAL_h[0:4, co, PERIOD+OFFSET-2:PERIOD+OFFSET]
        
    # berechnet: mMix_SOLID_h[0:7, co, PERIOD+OFFSET]
    # berechnet: mMix_IDEAL_h[0:7, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    #-- MA(2)-Parameter
    QUAL_AR1 = 0.5
    QUAL_MA1 = [0.25, 0.85]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Wirkung Technik-Investitionen
    IF_QUAL = np.array([[[  0.00 ,  0.25 ,  0.50 ,  0.75 ,  1.00 ,  1.40 ,  1.80 ,  2.20 ,  2.60 ,  3.00 ,  3.50 ,  4.00 ,  5.00 , 10.00 , 20.00 ],
                         [  0.000,  0.200,  0.375,  0.525,  0.650,  0.810,  0.954,  1.082,  1.194,  1.290,  1.390,  1.470,  1.610,  2.210,  3.210]],
    # Wirkung Haptik-Investitionen
                        [[  0.0  ,  0.2  ,  0.4  ,  0.6  ,  0.8  ,  1.0  ,  1.3  ,  1.6  ,  2.0  ,  2.4  ,  2.8  ,  3.4  ,  4.0  ,  8.0  , 16.0  ],
                         [  0.000,  0.160,  0.300,  0.420,  0.520,  0.600,  0.708,  0.804,  0.916,  1.012,  1.092,  1.188,  1.272,  1.752,  2.552]],
    # Technik-Index SOLID
                        [[   0.0 ,   4.0 ,   5.0 ,   8.0 ,  10.0 ,  11.8 ,  12.2 ,  16.8 ,  17.2 ,  20.0 ,  30.0 ,  40.0 ,  50.0 ,  80.0 , 120.0 ],
                         [  90.0 , 100.0 , 102.5 , 109.7 , 114.1 , 117.7 , 123.7 , 135.2 , 142.4 , 148.0 , 166.0 , 181.0 , 194.0 , 227.0 , 267.0 ]],
    # Haptik-Index SOLID/IDEAL
                        [[   0.0 ,   3.0 ,   6.0 ,   9.0 ,  12.0 ,  15.0 ,  18.0 ,  21.0 ,  24.0 ,  28.0 ,  32.0 ,  36.0 ,  50.0 ,  80.0 , 120.0 ],
                         [  92.5 , 100.0 , 107.5 , 114.7 , 121.6 , 128.2 , 134.5 , 140.5 , 146.2 , 153.4 , 160.2 , 166.6 , 187.6 , 223.6 , 263.6 ]],
    # Technik-Index IDEAL
                        [[   0.0 ,   4.0 ,   8.0 ,  12.0 ,  16.0 ,  20.0 ,  24.0 ,  28.0 ,  32.0 ,  36.0 ,  42.0 ,  50.0 ,  75.0 , 100.0 , 160.0 ],
                         [  90.0 , 100.0 , 110.0 , 119.6 , 128.8 , 137.6 , 146.0 , 154.0 , 161.6 , 168.8 , 179.0 , 191.8 , 229.3 , 259.3 , 319.3 ]],
    # Haptik-Index SOLID/IDEAL
                        [[   0.0 ,   3.0 ,   6.0 ,   9.0 ,  12.0 ,  15.0 ,  18.0 ,  21.0 ,  24.0 ,  28.0 ,  32.0 ,  36.0 ,  50.0 ,  80.0 , 120.0 ],
                         [  92.5 , 100.0 , 107.5 , 114.7 , 121.6 , 128.2 , 134.5 , 140.5 , 146.2 , 153.4 , 160.2 , 166.6 , 187.6 , 223.6 , 263.6 ]],
    # kombinierte Produktqualität: optimale Haptik für erreichte Technik
                        [[  90.0,  100.0 , 102.0 , 105.0 , 109.0 , 114.0 , 120.0 , 127.0 , 135.0 , 144.0 , 154.0 , 166.0 , 190.0 , 240.0 , 400.0 ],
                         [  92.5,  100.0 , 100.5 , 101.4 , 102.8 , 104.8 , 107.5 , 111.0 , 115.4 , 120.8 , 127.3 , 135.7 , 153.7 , 193.7 , 337.7 ]],
    # kombinierte Produktqualität: Abweichung Haptik-Index -> Anpassung Technik-Index
                        [[ -50.0,  -25.0 , -15.0 , -10.0 ,  -6.0 ,  -3.0 ,  -1.0 ,   0.0 ,   1.0 ,   3.0 ,   6.0 ,  10.0 ,  15.0 ,  25.0 ,  50.0 ],
                         [ -38.1,  -15.6 ,  -7.6 ,  -4.1 ,  -1.7 ,  -0.5 ,  -0.1 ,   0.0 ,   0.8 ,   1.6 ,   2.2 ,   2.8 ,   3.4 ,   4.5 ,   7.0 ]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # initialisiere Produktqualitäten
    qual = np.zeros((2, 7))
    rd_eff_total = np.zeros((2,2))
    rd_eff = np.zeros((2, 4))
    
    # F&E-Ausgaben
    rd_exp = rd_inv[0:2] + rd_inv[2:4]
    # # Marktüberbeanspruchung (Mio.EUR)
    rd_strain = rd_exp - rd_hist[0:2]
    rd_strain[:, 0] = np.amax(np.vstack((rd_strain[:, 0], np.zeros(2))), axis=0)
    rd_strain[:, 1] = np.amax(np.vstack((rd_strain[:, 1], np.zeros(2))), axis=0)
    
    # neue F&E-Marktvolumen
    qual[0, 0:2] = np.around(QUAL_AR1 * rd_hist[0:2, 1]
                             + (1-QUAL_AR1) * rd_exp[:, 1], 3)
    qual[1, 0:2] = qual[0, 0:2]
    
    # F&E-Wirkung (Mio.EUR)
    #-- features: f=0 Technik / f=1 Haptik
    for f in range(2):
        rd_eff_total[f] = np.around(rd_exp[f] + stepwise_linear_function(IF_QUAL[f], rd_strain[f]) - rd_strain[f], 3)
    
    # F&E-Wirkung produktspezifisch (Mio.EUR)
    rd_eff[:, 0:2] =  np.around(np.divide(rd_inv[0:2], rd_exp) * rd_eff_total, 3).T
    rd_eff[:, 2:4] = rd_eff_total.T - rd_eff[:, 0:2]
    #-- products: p=0 SOLID / p=1 IDEAL
    #-- features: f=0 Technik / f=1 Haptik
    for p in range(2):
        for f in range(2):
            i = 2+4*p+f
            j = 2*p+f
            # kum. F&E-Wirkungen (Mio.EUR)
            qual[p, 2+f] = round(rd_hist[i, 1] + ma_value(rd_eff[:, j], QUAL_MA1), 3)
            # Qualitäts-Indizes
            qual[p, 4+f] = round(stepwise_linear_function(IF_QUAL[2+j], qual[p, 2+f]), 2)
    
    #-- optimale Haptik für erreichten Technik-Index
    hapt_opt = np.around(stepwise_linear_function(IF_QUAL[6], qual[:, 4]), 2)
    # Haptik-Lücke des Produktes
    hapt_diff = qual[:, 5] - hapt_opt
    #-- Anpassung der (kombinierten) Produktqualität
    #   (Technical Equivalent Product)
    qual[:, 6] = np.around(qual[:, 4] + stepwise_linear_function(IF_QUAL[7], hapt_diff), 2)

    return qual


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Marketing-Mix-Wirkungen der Werbe- und Vertriebsmaßnahmen
def mMix_effects(mMix_means, mMix_effect0):
    """Berechnet Wirkung der Marketing-Mix-Maßnahmen in Werbung und Vertrieb"""

    # benötigt: mMix_means(4x2)
    # mDec_XXXXX_h[4:6, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]   (Werbung:      Inland/Ausland)
    # mDec_GESAMT_h[1:3, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]  (Vertriebs-MA: Inland/Ausland)
    
    # benötigt: mMix_effect0(4)
    # mMix_XXXXX_h[5:9, co, PERIOD+OFFSET-1]                   (Wirkungen VP)
    
    # berechnet: mMix_effect
    # mMix_XXXXX_h[5:9, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    #-- AR(1)-Parameter für Werbe- und Vertriebswirkung
    MMIX_AR     = np.array([0.2, 0.2, 0.25, 0.25])
    MMIX_AR_RED = np.array([0  , 0  , 0.25, 0.25])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # Marketing-Mix-Wirkungen der Werbe- und Vertriebsmaßnahmen (je Inland/Ausland)
    
    mMix_effect = np.around(
        mMix_effect0 * MMIX_AR + mMix_means[:, 1]*(1-MMIX_AR)
        + MMIX_AR_RED * np.amin(
            np.vstack(((mMix_means[:, 1] - mMix_means[:, 0]),
                        np.zeros(4))), axis=0), 2)
    
    return mMix_effect


#--------##--------##--------##--------##--------##--------##--------##--------#
# Kundenzufriedenheit-SOLID (Customer Satisfaction)
def cSAT_SOLID(preis, qual, cs_hist, bs_hist):
    """Berechnung der Kundenzufriedenheiten (customer satisfaction)"""

    # benötigt: preis(2 x 2)
    # mDec_SOLID_h[0:2, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]   
    
    # benötigt: qual(2)
    # [pp_SOLID_h[4, co, PERIOD+OFFSET], szenario['eQI_SOLID'][PERIOD+OFFSET]]
    
    # benötigt: cs_hist(2)
    # cs_SOLID_h[:, co, PERIOD+OFFSET-2:PERIOD+OFFSET]
    
    # benötigt: bs_hist
    # bs_SOLID_h[1, co, PERIOD+OFFSET-1]
        
    # berechnet: cs_SOLID_h[(0,3,4], co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    #-- MA(2)-Parameter für Preisstabilität
    CS_SOLID_MA2 = [0.22, 0.33 , 0.45]
    
    #-- ARMA(1,1)-Parameter für CS-Index
    CS_SOLID_AR1 = 0.1
    #   --  [0.20, 0.80] * (1 - 0.1)
    CS_SOLID_MA1 = [0.18, 0.72]
    
    #-- Gewichte für CS-Index
    CS_SOLID_W = [0.20, 0.20, 0.20, 0.20, 0.20]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Inland
    # Preis-Leistungs-Verhältnis (Inland)
    IF_CS_SOLID = np.array([[[   0.0,  10.0,  11.0,  12.0,  13.0,  13.5,  14.0,  14.5,  15.0,  16.0,  17.0,  18.0,  20.0,  25.0,  50.0],
                             [  31.0,  21.0,  19.0,  15.0,   9.0,   5.0,   0.0,  -5.0,  -9.0, -15.0, -19.0, -21.0, -23.0, -25.5, -30.5]],
    # Preis-Leistungs-Verhältnis (Ausland)
                            [[   0.0,   6.0,   7.0,   8.0,   9.0,   9.5,  10.0,  10.5,  11.0,  12.0,  13.0,  14.0,  15.0,  25.0,  50.0],
                             [  27.0,  21.0,  19.0,  15.0,   9.0,   5.0,   0.0,  -5.0,  -9.0, -15.0, -19.0, -21.0, -22.0, -27.0, -32.0]],
    # Produkt-Qualität
                            [[ -25  , -20  , -15  , -10  ,  -5  ,  -2  ,   0  ,   2  ,   5  ,  10  ,  15  ,  20  ,  25  ,  50  , 200  ],
                             [ -22.1, -19.6, -16.6, -12.6,  -7.6,  -4.0,   0.0,   4.0,   7.6,  12.6,  16.6,  19.6,  22.1,  32.1,  77.1]],
    # Preis-Stabilität
                            [[  0.00,  0.01,  0.02,  0.03,  0.04,  0.05,  0.06,  0.07,  0.08,  0.09,  0.10,  0.20,  0.40,  0.60,  1.00],
                             [ 12.0 ,  7.0 ,  3.0 ,  0.0 , -2.0 , -5.0 , -9.0 ,-12.0 ,-14.0 ,-15.5 ,-16.5 ,-21.5 ,-25.5 ,-27.5 ,-29.5 ]],
    # Angebotsdefizit
                            [[  0.00,  0.01,  0.02,  0.03,  0.04,  0.05,  0.06,  0.08,  0.10,  0.12,  0.15,  0.20,  0.25,  0.50,  1.00],
                             [  5.0 ,  3.0 ,  0.0 , -0.5 , -1.3 , -2.3 , -3.5 , -6.5 ,-10.5 ,-13.5 ,-17.1 ,-22.1 ,-26.1 ,-38.6 ,-48.6 ]],
    # Markenstärke
                            [[  50.0,  70.0,  80.0,  85.0,  90.0,  95.0,  98.0, 100.0, 102.5, 105.0, 110.0, 115.0, 120.0, 150.0, 200.0],
                             [ -27.4, -21.4, -17.4, -14.9, -11.9,  -8.4,  -6.0,  -4.0,   0.0,   5.0,  12.5,  17.5,  21.5,  36.5,  51.5]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # aktueller Zufriedenheitswert (Inland/Ausland)
    cust_sat_d = 100.0
    cust_sat_a = 100.0
    
    # Preis-Leistungs-Verhältnis (price-performance-ratio)
    # Inland
    factor = preis[0, 1]/qual[0] if preis[0, 1]!=0 else 14
    cust_sat_d += CS_SOLID_W[0]*round(stepwise_linear_function(
        IF_CS_SOLID[0], factor), 2)
    # Ausland
    factor = preis[1, 1]/qual[0] if preis[1, 1]!=0 else 10
    cust_sat_a += CS_SOLID_W[1]*round(stepwise_linear_function(
        IF_CS_SOLID[1], factor), 2)
    
    # Produkt-Qualität
    # Inland
    factor = qual[0]-qual[1]
    cust_sat_d += CS_SOLID_W[1]*round(stepwise_linear_function(
        IF_CS_SOLID[2], factor), 2)
    # Ausland
    cust_sat_a += CS_SOLID_W[1]*round(stepwise_linear_function(
        IF_CS_SOLID[2], factor), 2)
    
    # Preis-Stabilität
    # Inland
    var_d = preis[0, 1]/preis[0, 0]-1 if preis[0, 0]!=0 else 0.03
    var_d = round(var_d, 4) if var_d>=0 else -round(var_d/4, 4)
    temp = np.append(cs_hist[0, :], var_d)**2
    factor = np.sqrt(ma_value(temp, CS_SOLID_MA2))
    cust_sat_d += CS_SOLID_W[2]*round(stepwise_linear_function(
        IF_CS_SOLID[3], factor), 2)
    # Ausland
    var_a = preis[1, 1]/preis[1, 0]-1 if preis[1, 0]!=0 else 0.03
    var_a = round(var_a, 4) if var_a>=0 else -round(var_a/4, 4)
    temp = np.append(cs_hist[5, :], var_a)**2
    factor = np.sqrt(ma_value(temp, CS_SOLID_MA2))
    cust_sat_a += CS_SOLID_W[2]*round(stepwise_linear_function(
        IF_CS_SOLID[3], factor), 2)
    
    # Angebotsdefizit
    # Inland
    factor = 1-cs_hist[1, 1]/cs_hist[2, 1] if cs_hist[2, 1]!=0 else 0
    cust_sat_d += CS_SOLID_W[3]*round(stepwise_linear_function(
        IF_CS_SOLID[4], factor), 2)
    # Ausland
    factor = 1-cs_hist[6, 1]/cs_hist[7, 1] if cs_hist[7, 1]!=0 else 0
    cust_sat_a += CS_SOLID_W[3]*round(stepwise_linear_function(
        IF_CS_SOLID[4], factor), 2)
    
    # Markenstärke
    # Inland
    factor = bs_hist[0]
    cust_sat_d += CS_SOLID_W[4]*round(stepwise_linear_function(
        IF_CS_SOLID[5], factor), 2)
    # Ausland
    factor = bs_hist[1]
    cust_sat_a += CS_SOLID_W[4]*round(stepwise_linear_function(
        IF_CS_SOLID[5], factor), 2)
    
    # Gesamtindex
    # Inland
    temp = np.append(cs_hist[3, 1], cust_sat_d)
    cs_index_d = cs_hist[4, 1]*CS_SOLID_AR1 + ma_value(temp, CS_SOLID_MA1)
    cs_index_d = round(cs_index_d, 2)
    # Ausland
    temp = np.append(cs_hist[8, 1], cust_sat_a)
    cs_index_a = cs_hist[9, 1]*CS_SOLID_AR1 + ma_value(temp, CS_SOLID_MA1)
    cs_index_a = round(cs_index_a, 2)

    cust_sat_d = round(cust_sat_d, 2)
    cust_sat_a = round(cust_sat_a, 2)
    
    return [var_d, cust_sat_d, cs_index_d, var_a, cust_sat_a, cs_index_a]


#--------##--------##--------##--------##--------##--------##--------##--------#
# Kundenzufriedenheit-IDEAL (Customer Satisfaction)
def cSAT_IDEAL(preis, qual, cs_hist, bs_hist):
    """Berechnung der Kundenzufriedenheiten (customer satisfaction)"""

    # benötigt: preis(2 x 2)
    # mDec_IDEAL_h[0:2, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]   
    
    # benötigt: qual(2)
    # [pp_IDEAL_h[4, co, PERIOD+OFFSET], szenario['eQI_IDEAL'][PERIOD+OFFSET]]
    
    # benötigt: cs_hist(2)
    # cs_IDEAL_h[:, co, PERIOD+OFFSET-2:PERIOD+OFFSET]
    
    # benötigt: bs_hist
    # bs_IDEAL_h[1, co, PERIOD+OFFSET-1]
        
    # berechnet: cs_IDEAL_h[(0,3,4], co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    #-- MA(2)-Parameter für Preisstabilität
    CS_IDEAL_MA2 = [0.22, 0.33 , 0.45]
    
    #-- ARMA(1,1)-Parameter für CS-Index
    CS_IDEAL_AR1 = 0.1
    #   --  [0.20, 0.80] * (1 - 0.1)
    CS_IDEAL_MA1 = [0.18, 0.72]
    
    #-- Gewichte für CS-Index
    CS_IDEAL_W = [0.20, 0.20, 0.20, 0.20, 0.20]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Inland
    # Preis-Leistungs-Verhältnis (Inland)
    IF_CS_IDEAL = np.array([[[   0.0,  23.0,  24.0,  25.0,  26.0,  26.5,  27.0,  27.5,  28.0,  29.0,  30.0,  32.0,  35.0,  40.0,  50.0],
                             [  32.5,  21.0,  19.0,  15.0,   9.0,   5.0,   0.0,  -5.0,  -9.0, -15.0, -19.0, -23.0, -26.0, -28.5, -30.5]],
    # Preis-Leistungs-Verhältnis (Ausland)
                            [[   0.0,  14.0,  15.0,  16.0,  17.0,  17.5,  18.0,  18.5,  19.0,  20.0,  21.0,  22.0,  25.0,  35.0,  50.0],
                             [  35.0,  21.0,  19.0,  15.0,   9.0,   5.0,   0.0,  -5.0,  -9.0, -15.0, -19.0, -21.0, -24.0, -29.0, -32.0]],
    # Produkt-Qualität
                            [[ -25  , -20  , -15  , -10  ,  -5  ,  -2  ,   0  ,   2  ,   5  ,  10  ,  15  ,  20  ,  25  ,  50  , 200  ],
                             [ -22.1, -19.6, -16.6, -12.6,  -7.6,  -4.0,   0.0,   4.0,   7.6,  12.6,  16.6,  19.6,  22.1,  32.1,  77.1]],
    # Preis-Stabilität
                            [[  0.00,  0.01,  0.02,  0.03,  0.04,  0.05,  0.06,  0.07,  0.08,  0.09,  0.10,  0.20,  0.40,  0.60,  1.00],
                             [ 12.0 ,  7.0 ,  3.0 ,  0.0 , -2.0 , -5.0 , -9.0 ,-12.0 ,-14.0 ,-15.5 ,-16.5 ,-21.5 ,-25.5 ,-27.5 ,-29.5 ]],
    # Angebotsdefizit
                            [[  0.00,  0.01,  0.02,  0.03,  0.04,  0.05,  0.06,  0.08,  0.10,  0.12,  0.15,  0.20,  0.25,  0.50,  1.00],
                             [  5.0 ,  3.0 ,  0.0 , -0.5 , -1.3 , -2.3 , -3.5 , -6.5 ,-10.5 ,-13.5 ,-17.1 ,-22.1 ,-26.1 ,-38.6 ,-48.6 ]],
    # Markenstärke
                            [[  50.0,  70.0,  80.0,  85.0,  90.0,  95.0,  98.0, 100.0, 102.5, 105.0, 110.0, 115.0, 120.0, 150.0, 200.0],
                             [ -27.4, -21.4, -17.4, -14.9, -11.9,  -8.4,  -6.0,  -4.0,   0.0,   5.0,  12.5,  17.5,  21.5,  36.5,  51.5]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # aktueller Zufriedenheitswert (Inland/Ausland)
    cust_sat_d = 100.0
    cust_sat_a = 100.0
    
    # Preis-Leistungs-Verhältnis (price-performance-ratio)
    # Inland
    factor = preis[0, 1]/qual[0] if preis[0, 1]!=0 else 27
    cust_sat_d += CS_IDEAL_W[0]*round(stepwise_linear_function(
        IF_CS_IDEAL[0], factor), 2)
    # Ausland
    factor = preis[1, 1]/qual[0] if preis[1, 1]!=0 else 18
    cust_sat_a += CS_IDEAL_W[1]*round(stepwise_linear_function(
        IF_CS_IDEAL[1], factor), 2)
    
    # Produkt-Qualität
    # Inland
    factor = qual[0]-qual[1]
    cust_sat_d += CS_IDEAL_W[1]*round(stepwise_linear_function(
        IF_CS_IDEAL[2], factor), 2)
    # Ausland
    cust_sat_a += CS_IDEAL_W[1]*round(stepwise_linear_function(
        IF_CS_IDEAL[2], factor), 2)
    
    # Preis-Stabilität
    # Inland
    var_d = preis[0, 1]/preis[0, 0]-1 if preis[0, 0]!=0 else 0.03
    var_d = round(var_d, 4) if var_d>=0 else -round(var_d/4, 4)
    temp = np.append(cs_hist[0, :], var_d)**2
    factor = np.sqrt(ma_value(temp, CS_IDEAL_MA2))
    cust_sat_d += CS_IDEAL_W[2]*round(stepwise_linear_function(
        IF_CS_IDEAL[3], factor), 2)
    # Ausland
    var_a = preis[1, 1]/preis[1, 0]-1 if preis[1, 0]!=0 else 0.03
    var_a = round(var_a, 4) if var_a>=0 else -round(var_a/4, 4)
    temp = np.append(cs_hist[5, :], var_a)**2
    factor = np.sqrt(ma_value(temp, CS_IDEAL_MA2))
    cust_sat_a += CS_IDEAL_W[2]*round(stepwise_linear_function(
        IF_CS_IDEAL[3], factor), 2)
    
    # Angebotsdefizit
    # Inland
    factor = 1-cs_hist[1, 1]/cs_hist[2, 1] if cs_hist[2, 1]!=0 else 0
    cust_sat_d += CS_IDEAL_W[3]*round(stepwise_linear_function(
        IF_CS_IDEAL[4], factor), 2)
    # Ausland
    factor = 1-cs_hist[6, 1]/cs_hist[7, 1] if cs_hist[7, 1]!=0 else 0
    cust_sat_a += CS_IDEAL_W[3]*round(stepwise_linear_function(
        IF_CS_IDEAL[4], factor), 2)
    
    # Markenstärke
    # Inland
    factor = bs_hist[0]
    cust_sat_d += CS_IDEAL_W[4]*round(stepwise_linear_function(
        IF_CS_IDEAL[5], factor), 2)
    # Ausland
    factor = bs_hist[1]
    cust_sat_a += CS_IDEAL_W[4]*round(stepwise_linear_function(
        IF_CS_IDEAL[5], factor), 2)
    
    # Gesamtindex
    # Inland
    temp = np.append(cs_hist[3, 1], cust_sat_d)
    cs_index_d = cs_hist[4, 1]*CS_IDEAL_AR1 + ma_value(temp, CS_IDEAL_MA1)
    cs_index_d = round(cs_index_d, 2)
    # Ausland
    temp = np.append(cs_hist[8, 1], cust_sat_a)
    cs_index_a = cs_hist[9, 1]*CS_IDEAL_AR1 + ma_value(temp, CS_IDEAL_MA1)
    cs_index_a = round(cs_index_a, 2)

    cust_sat_d = round(cust_sat_d, 2)
    cust_sat_a = round(cust_sat_a, 2)
    
    return [var_d, cust_sat_d, cs_index_d, var_a, cust_sat_a, cs_index_a]


#--------##--------##--------##--------##--------##--------##--------##--------#
# Markenstärke (Brand Strength)
def brand_strength(pr_exp, cs_cur, pr_hist):
    """Berechnung der Markenstärke (brand strength)"""
    
    # benötigt: pr_exp(3)   (public relation expenditures)
    # mDec_GESAMT_h[0, co, PERIOD+OFFSET-2:PERIOD+OFFSET+1]   
    
    # benötigt: cs_cur(2)  (current customer sastisfaction)
    # cs_XXXXX_h[[4, 9], co, PERIOD+OFFSET]
        
    # benötigt: pr_hist  (geglättete PR-Ausgaben der Vorperiode)
    # bs_SOLID_h[0, co, PERIOD+OFFSET-1]
    
    # berechnet: bs_SOLID_h[:, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    #-- ARMA(1,2)-Parameter für BS-Index
    BS_SOLID_AR1 = 0.6
    #   --  [0.20, 0.50, 0.35] * (1 - 0.6)
    BS_SOLID_MA2 = [0.08, 0.20 , 0.14]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Markenstärke
    IF_BS_SOLID = np.array([[    0  ,  100  ,  200  ,  300  ,  400  ,  500  ,  700  ,  900  , 1100  , 1300  , 2000  , 4000  ,10000  ,20000  ,50000  ],
                            [   50.0,   65.0,   77.0,   87.0,   95.0,  100.0,  104.0,  107.0,  109.4,  111.4,  117.0,  131.0,  167.0,  217.0,  277.0]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # geglättete PR-Ausgaben (ARMA(1,2))
    pr_arma = pr_hist*BS_SOLID_AR1 + ma_value(pr_exp, BS_SOLID_MA2)
    
    # Korrektur der Markenstärke gemäß Kundenzufriedenheit
    cor = 10*(cs_cur-100) + 10*(cs_cur<100)*(cs_cur-100)
    
    # korrigierte und geglättete PR-Ausgaben
    pr_cor = pr_arma + cor
    
    # Markenstärke (brand strength index)
    bs_ind = np.around(stepwise_linear_function(
        IF_BS_SOLID, pr_cor), 2)

    return np.insert(bs_ind, 0, np.around(pr_arma, 2))


#--------##--------##--------##--------##--------##--------##--------##--------#
# Marktvolumen-Anpassung (sales market)
def sm_volume(comp_data, scen_data, market, arma0):
    """Berechnung des effektiven Marktvolumens (Nachfrage / market volume)"""

    # benötigt: comp_data (NUM_COMPANIES x 8)  (Unternehmensdaten)
    # prod_comp(NUM_COMPANIES x 1)  (Produktqualitäten)
    #-- mMix_XXXXX_h[ 6, :, PERIOD+OFFSET]
    # price_comp(NUM_COMPANIES x 2) (Verkaufspreise)
    #-- mDec_XXXXX_h[ 0, :, PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    # prom_comp(NUM_COMPANIES x 2)  (Produktwerbung)
    #-- mMix_XXXXX_h[ 7, :, PERIOD+OFFSET]
    # place_comp(NUM_COMPANIES x 2) (Vertriebs-MA)
    #-- mMix_XXXXX_h[ 9, :, PERIOD+OFFSET]
    # bs_comp(NUM_COMPANIES x 1)    (Markenstärken)
    #-- mMix_XXXXX_h[12, :, PERIOD+OFFSET]
    
    # benötigt: scen_data (6 x 2)  (Szenario-Daten) 
    # mv_scen(4 x 2)  (Marktvolumen)
    #-- szenario['MarktVol'][[0, 4, 8, 12], PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    # pi_scen(2)  (Preisindex)
    #-- szenario['Preisindex'][PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    # qual_exp  (erwartete Produktqualität)
    #-- szenario['eQI_XXXXX'][PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    
    # benötigt: market(1)  (Markt-Identifizierer)
    #-- market = 0/1/2/3
    
    # benötigt: arma0(3) (Startwerte für ARMA(1,1)-Prozesse)
    #-- szenario['MarktVol'][1:4, PERIOD+OFFSET-1]
    
    # berechnet: mv_cur  (aktuelles Markt-Nachfrage-Volumen)
    #            arma0   (aktualisierte Startwerte für ARMA(1,1)-Prozesse)
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Referenzwerte
    REF_PRICE = [1600, 1110, 2730, 1890]
    REF_PROM  = [0.055, 0.075, 0.08, 0.10]
    REF_PLACE = [1450, 1200]
        
    #-- ARMA(1,1)-Parameter für Preispolitik
    MV_PRICE_AR1 = 0.2
    #   --  [0.20, 0.80] * (1 - 0.2)
    MV_PRICE_MA1 = [0.16, 0.64]
    
    #-- ARMA(1,1)-Parameter für Kommunikationspolitik
    MV_PROM_AR1 = 0.2
    #   --  [0.25, 0.75] * (1 - 0.2)
    MV_PROM_MA1 = [0.20, 0.60]
    
    #-- ARMA(1,1)-Parameter für Distributionspolitik
    MV_PLACE_AR1 = 0.5
    #   --  [0.10, 0.90] * (1 - 0.5)
    MV_PLACE_MA1 = [0.05, 0.45]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Produktpolitik
    IF_MV = np.array([[[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  1.64 ],
                       [ -0.340, -0.215, -0.115, -0.090, -0.060, -0.035, -0.015,  0.000,  0.020,  0.045,  0.075,  0.110,  0.150,  0.250,  0.364]],
    # Preispolitik
                      [[ -1.00 , -0.40 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.40 ,  1.06 ],
                       [  0.340,  0.280,  0.160,  0.110,  0.070,  0.040,  0.020,  0.000, -0.020, -0.040, -0.070, -0.110, -0.160, -0.340, -1.000]],
    # Kommunikationspolitik SOLID-Inland
                      [[  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.04 ,  0.05 ,  0.055,  0.06 ,  0.065,  0.07 ,  0.08 ,  0.09 ,  0.10 ,  0.12 ,  0.40 ],
                       [ -0.108, -0.098, -0.086, -0.070, -0.050, -0.020,  0.000,  0.014,  0.026,  0.036,  0.052,  0.064,  0.074,  0.090,  0.202]],
    # Kommunikationspolitik SOLID-Ausland
                      [[  0.000,  0.010,  0.040,  0.050,  0.060,  0.070,  0.075,  0.080,  0.085,  0.090,  0.100,  0.110,  0.120,  0.140,  0.400],
                       [ -0.132, -0.122, -0.086, -0.070, -0.050, -0.020,  0.000,  0.014,  0.026,  0.036,  0.052,  0.064,  0.074,  0.090,  0.194]],
    # Kommunikationspolitik IDEAL-Inland
                      [[  0.000,  0.010,  0.050,  0.060,  0.070,  0.075,  0.080,  0.085,  0.090,  0.100,  0.110,  0.120,  0.130,  0.150,  0.400],
                       [ -0.130, -0.120, -0.070, -0.055, -0.035, -0.020,  0.000,  0.014,  0.026,  0.046,  0.062,  0.074,  0.084,  0.100,  0.200]],
    # Kommunikationspolitik IDEAL-Ausland
                      [[  0.000,  0.020,  0.060,  0.080,  0.090,  0.095,  0.100,  0.105,  0.110,  0.120,  0.130,  0.140,  0.150,  0.200,  0.400],
                       [ -0.135, -0.125, -0.085, -0.055, -0.035, -0.020,  0.000,  0.014,  0.026,  0.046,  0.062,  0.074,  0.084,  0.124,  0.204]],
    # Distributionspolitik
                      [[ -1.00 , -0.80 , -0.50 , -0.40 , -0.30 , -0.20 , -0.10 ,  0.00 ,  0.10 ,  0.20 ,  0.30 ,  0.50 ,  1.00 ,  2.50 , 20.00 ],
                       [ -0.430, -0.330, -0.150, -0.100, -0.060, -0.030, -0.010,  0.000,  0.012,  0.026,  0.042,  0.070,  0.120,  0.195,  0.545]],
    # Markenpolitik
                      [[ 50.0  , 70.0  , 80.0  , 90.0  , 95.0  ,100.0  ,102.5  ,105.0  ,110.0  ,115.0  ,120.0  ,130.0  ,150.0  ,200.0  ,250.0  ],
                       [ -0.097, -0.077, -0.057, -0.032, -0.017, -0.005,  0.000,  0.010,  0.025,  0.038,  0.048,  0.064,  0.084,  0.114,  0.124]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    place = market-2*(market//2)
    # Initialisiere Anpassungsfaktor des Marktvolumens
    mv_adj = 1.0
    
    prod_comp = comp_data[:, 0]
    price_comp = comp_data[:, 1:3]
    prom_comp = comp_data[:, 3:5]
    place_comp = comp_data[:, 5:7]
    bs_comp = comp_data[:, 7]
    
    mv_scen = scen_data[0:4]
    pi_ind = scen_data[4]
    qual_exp = scen_data[5][1]
    
    # Ermittle am Markt aktive Unternehmen
    comp_mask = np.array(price_comp[:, 1] > 0)
    
    # Beende Funktion, wenn kein Unternehmen am Markt aktiv ist
    if comp_mask.sum()==0:
        return 0, [0, REF_PROM[market], 0]
    
    # Produktpolitik
    prod_mean = prod_comp[comp_mask].mean(axis=0)
    deviation = (prod_mean - qual_exp)/100
    mv_adj *= 1 + round(stepwise_linear_function(
        IF_MV[0], deviation), 3)
    
    # Preispolitik
    price_mean = price_comp[comp_mask].mean(axis=0)
    deviation = 100*np.divide(price_mean, pi_ind)/REF_PRICE[market]-1
    if price_mean[0] == 0:
        deviation[0] = 0
    pp_arma = arma0[0]*MV_PRICE_AR1 + ma_value(deviation, MV_PRICE_MA1)
    pp_arma = round(pp_arma, 4)
    mv_adj *= 1 + round(stepwise_linear_function(
        IF_MV[1], pp_arma), 3)
        
    # Kommunikationspolitik (Werbung) NEU
    prom_mean = prom_comp[comp_mask].mean(axis=0)
    if mv_scen[market, 0] == 0:
        mv_scen[market, 0] = 1
        prom_mean[0] = REF_PROM[market]
    deviation = np.divide(prom_mean, mv_scen[market])
    if price_mean[0] == 0:
        deviation[0] = REF_PROM[market]
    kp_arma = arma0[1]*MV_PROM_AR1 + ma_value(deviation, MV_PROM_MA1)
    kp_arma = round(kp_arma, 4)
    mv_adj *= 1 + round(stepwise_linear_function(
        IF_MV[2+market], kp_arma), 3)
       
    # Distributionspolitik
    place_mean = place_comp[comp_mask].mean(axis=0)
    deviation = np.divide(place_mean, mv_scen[place]/REF_PLACE[place])-1
    if price_mean[0] == 0:
        deviation[0] = 0
    dp_arma = arma0[2]*MV_PLACE_AR1 + ma_value(deviation, MV_PLACE_MA1)
    dp_arma = round(dp_arma, 4)
    mv_adj *= 1 + round(stepwise_linear_function(
        IF_MV[6], dp_arma), 3)
    
    # Markenpolitik (Kommunikationspolitik II)
    bs_mean = bs_comp[comp_mask].mean(axis=0)
    mv_adj *= 1 + round(stepwise_linear_function(
        IF_MV[7], bs_mean), 3)
    
    mv_cur = round(mv_adj*mv_scen[market, 1],0)
      
    return mv_cur, [pp_arma, kp_arma, dp_arma]


#--------##--------##--------##--------##--------##--------##--------##--------#
# Marktnachfrage / Marktanteile (sales market share) -> potenzieller Absatz
def sm_share(comp_data, mv_cur):
    """Berechnung der Marktnachfrage (potenzieller Absatz)"""

    # benötigt: comp_data (6 x NUM_COMPANIES)  (Unternehmensdaten)
    # prod_comp(NUM_COMPANIES)  (Produktqualitäten)
    #-- mMix_SOLID_h[4, :, PERIOD+OFFSET]
    # price_comp(NUM_COMPANIES) (Verkaufspreise)
    #-- mDec_SOLID_h[0, :, PERIOD+OFFSET]
    # prom_comp(NUM_COMPANIES)  (Produktwerbung)
    #-- mMix_SOLID_h[5, :, PERIOD+OFFSET]
    # place_comp(NUM_COMPANIES) (Vertriebs-MA)
    #-- mMix_SOLID_h[7, :, PERIOD+OFFSET]
    # bs_comp(NUM_COMPANIES)    (Markenstärken)
    #-- mMix_SOLID_h[10, :, PERIOD+OFFSET]
    # cs_comp(NUM_COMPANIES)    (Kundenzufriedenheit)
    #-- cs_SOLID_h[4, :, PERIOD+OFFSET]
    
    # benötigt: mv_cur          (Marktvolumen (Nachfrage))
    
    # berechnet: demand_cur  (aktuelle Markt-Nachfrage = potenzieller Absatz)

    #--------##--------##--------##--------##--------##--------##--------#
    # Berechne Marktanteile nur für aktive Unternehmen (Verkaufspreis > 0)
    
    # Unternehmen mit Verkaufspreis > 0
    comp_mask = np.array(comp_data[1] > 0)
    # Anzahl Unternehmen
    num_companies = comp_data.shape[1]
    # Anzahl am Markt aktiver Unternehmen
    active_comp = comp_mask.sum()
    
    # Beende Funktion, wenn kein Unternehmen am Markt ist
    if active_comp==0:
        return np.zeros(num_companies)
    
    # Setze Preis der nicht aktiven Unternehmen auf 1 (Division durch 0!)
    comp_data[1, np.logical_not(comp_mask)] = 1
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # benötigte Wirkungsfunktionen (impact factor)
    # Produktpolitik
    IF_MS_SOLID = np.array([[[ -1.00  , -0.50  , -0.25  , -0.20  , -0.15  , -0.10  , -0.05  ,  0.00  ,  0.05  ,  0.10  ,  0.15  ,  0.20  ,  0.25  ,  0.50  ,  3.00 ],
                             [  0.180 ,  0.680 ,  0.880 ,  0.905 ,  0.925 ,  0.945 ,  0.970 ,  1.000 ,  1.020 ,  1.042 ,  1.062 ,  1.080 ,  1.095 ,  1.160 ,  1.660]],
    # Preispolitik
                            [[ -1.00  , -0.50  , -0.25  , -0.20  , -0.15  , -0.10  , -0.05  ,  0.00  ,  0.05  ,  0.10  ,  0.15  ,  0.20  ,  0.25  ,  0.50  ,  3.00 ],
                             [  2.720 ,  2.220 ,  1.720 ,  1.570 ,  1.370 ,  1.220 ,  1.100 ,  1.000 ,  0.920 ,  0.820 ,  0.700 ,  0.550 ,  0.430 ,  0.180 ,  0.055]],
    # Kommunikationspolitik
                            [[ -1.00  , -0.50  , -0.25  , -0.20  , -0.15  , -0.10  , -0.05  ,  0.00  ,  0.05  ,  0.10  ,  0.15  ,  0.20  ,  0.25  ,  0.50  ,  3.00 ],
                             [  0.506 ,  0.806 ,  0.931 ,  0.951 ,  0.963 ,  0.973 ,  0.985 ,  1.000 ,  1.015 ,  1.027 ,  1.037 ,  1.049 ,  1.069 ,  1.159 ,  1.909]],
    # Distributionspolitik
                            [[ -1.00  , -0.50  , -0.25  , -0.20  , -0.15  , -0.10  , -0.05  ,  0.00  ,  0.05  ,  0.10  ,  0.15  ,  0.20  ,  0.25  ,  0.50  ,  3.00 ],
                             [  0.189 ,  0.689 ,  0.889 ,  0.924 ,  0.954 ,  0.967 ,  0.982 ,  1.000 ,  1.015 ,  1.029 ,  1.044 ,  1.069 ,  1.104 ,  1.329 ,  1.829]],
    # Markenpolitik
                            [[ -1.00  , -0.50  , -0.25  , -0.20  , -0.15  , -0.10  , -0.05  ,  0.00  ,  0.05  ,  0.10  ,  0.15  ,  0.20  ,  0.25  ,  0.50  ,  3.00 ],
                             [  0.435 ,  0.685 ,  0.835 ,  0.870 ,  0.910 ,  0.945 ,  0.975 ,  1.000 ,  1.025 ,  1.055 ,  1.095 ,  1.145 ,  1.185 ,  1.335 ,  2.335]],
    # Kundenzufriedenheit
                            [[ -1.00  , -0.50  , -0.25  , -0.20  , -0.15  , -0.10  , -0.05  ,  0.00  ,  0.05  ,  0.10  ,  0.15  ,  0.20  ,  0.25  ,  0.50  ,  3.00 ],
                             [  0.175 ,  0.675 ,  0.875 ,  0.910 ,  0.940 ,  0.965 ,  0.985 ,  1.000 ,  1.010 ,  1.025 ,  1.045 ,  1.070 ,  1.100 ,  1.225 ,  1.725]]])

    #--------##--------##--------##--------##--------##--------##--------#
    # Initialisierung der Marktanteil-Abweichungen
    ms_dev = np.ones(num_companies)
    
    # Produktpolitik
    prod_comp = comp_data[0]
    deviation = (prod_comp - prod_comp[comp_mask].mean())/100
    ms_dev *= stepwise_linear_function(IF_MS_SOLID[0], deviation)
    
    # Preispolitik
    price_comp = comp_data[1]
    deviation = price_comp / price_comp[comp_mask].mean()-1
    ms_dev *= stepwise_linear_function(IF_MS_SOLID[1], deviation)
    
    # Kommunikationspolitik
    prom_comp = comp_data[2]
    deviation = prom_comp / prom_comp[comp_mask].mean()-1
    ms_dev *= stepwise_linear_function(IF_MS_SOLID[2], deviation)
    
    # Distributionspolitik
    place_comp = comp_data[3]
    deviation = place_comp / place_comp[comp_mask].mean()-1
    ms_dev *= stepwise_linear_function(IF_MS_SOLID[3], deviation)
    
    # Markenpolitik
    bs_comp = comp_data[4]
    deviation = (bs_comp - bs_comp[comp_mask].mean())/100
    ms_dev *= stepwise_linear_function(IF_MS_SOLID[4], deviation)
    
    # Kundenzufriedenheit
    cs_comp = comp_data[5]
    deviation = (cs_comp - cs_comp[comp_mask].mean())/100
    ms_dev *= stepwise_linear_function(IF_MS_SOLID[5], deviation)
 
    # Berechne Marktanteile
    ms_dev = 1/active_comp*ms_dev
    ms_dev[np.logical_not(comp_mask)] = 0
    ms_dev = ms_dev/ms_dev.sum()
    
    demand_cur = np.around(np.divide(1000*mv_cur*num_companies*ms_dev,
                            price_comp), 0).astype(int)

    return demand_cur


#--------##--------##--------##--------##--------##--------##--------##--------#
# Fertigungs-Modell: Absatzmarkt-Angebot je Unternehmen / Auslastungsgrade
def sm_supply(pPROD_plan, pPROD_cap, prod_scen):
    """Berechnung der tatsächlichen Fertigungs-Mengen (SOLID und IDEAL)"""
    
    # benötigt: pPROD_plan(2 x NUM_COMPANIES)
    # pPROD_plan = pDec_SOLID_h[0, :, PERIOD+OFFSET]  (Fertigungs-Plan: SOLID)
    #              pDec_IDEAL_h[0, :, PERIOD+OFFSET]  (Fertigungs-Plan: IDEAL)
    
    # benötigt: pPROD_cap(3 x NUM_COMPANIES)
    # pPROD_cap = pRes_HR_h[1 , :, PERIOD+OFFSET]     (Anzahl Fertigungs-MA)
    #             pRes_HR_h[21, :, PERIOD+OFFSET]     (MA-Produktivität)
    #             pRes_TA_h[8, :, PERIOD+OFFSET]      (TA-Kapazitäten)
    
    # benötigt: prod_scen(5)
    # prod_scen = pRes_HR_h[1 , :, PERIOD+OFFSET]     (Anzahl Fertigungs-MA)
    # prod_scen = szenario['LohnNK'][1, PERIOD+OFFSET]       (max. Überstunden)
    #             szenario['BedarfSOLID'][2, PERIOD+OFFSET]  (Kapazitätsbedarf SOLID: Fertigungs-MA)
    #             szenario['BedarfIDEAL'][2, PERIOD+OFFSET]  (Kapazitätsbedarf IDEAL: Fertigungs-MA)
    #             szenario['BedarfSOLID'][3, PERIOD+OFFSET]  (Kapazitätsbedarf SOLID: TA)
    #             szenario['BedarfIDEAL'][3, PERIOD+OFFSET]  (Kapazitätsbedarf IDEAL: TA)
    
    # berechnet:  prod_act         (tatsächliche Fertigungsmengen SOLID/IDEAL)
    #             cap_ut           (Auslastungsgrad Fertigungs-MA / TA)
    
    #--------##--------##--------##--------##--------##--------##--------#
    # Produktionsmöglichkeiten 1: Fertigungspersonal
    #-- Kapazitätsbedarf
    emp_prod_SOLID = np.divide(prod_scen[1], pPROD_cap[1])
    emp_prod_IDEAL = np.divide(prod_scen[2], pPROD_cap[1])
    
    # erforderliches Fertigungs-Personal
    emp_need_SOLID = pPROD_plan[0] / 1000 * emp_prod_SOLID / (1+prod_scen[0])
    emp_need_IDEAL = pPROD_plan[1] / 1000 * emp_prod_IDEAL / (1+prod_scen[0])
    emp_need = emp_need_SOLID + emp_need_IDEAL
    
    #---------##---------##---------##---------##--------##--------##--------#
    # Produktionsmöglichkeiten 2: Technische Anlagen und Maschinen
    #-- Kapazitätsbedarf
    ta_prod_SOLID = prod_scen[3]
    ta_prod_IDEAL = prod_scen[4]
    
    # erforderliche Anlagenkapazitäten
    ta_need_SOLID = pPROD_plan[0] / 1000 * ta_prod_SOLID
    ta_need_IDEAL = pPROD_plan[1] / 1000 * ta_prod_IDEAL
    ta_need = ta_need_SOLID + ta_need_IDEAL
    
    #---------##---------##---------##---------##--------##--------##--------#
    # Restriktionen (Engpass) 1: Fertigungspersonal
    emp_rest = np.divide(pPROD_cap[0], emp_need)
    
    # maximale Fertigungs-Mengen
    emp_max_IDEAL = np.floor(
        ta_need_IDEAL * emp_rest * 1000 / prod_scen[4]).astype(int)
    emp_max_SOLID = np.floor(
        (pPROD_cap[0] * (1+prod_scen[0])
         - emp_max_IDEAL / 1000 * emp_prod_IDEAL)
        * 1000 / emp_prod_SOLID).astype(int)
    
    #---------##---------##---------##---------##--------##--------##--------#
    # Restriktionen (Engpass) 2: Technische Anlagen und Maschinen
    ta_rest = np.divide(pPROD_cap[2], ta_need)
    
    # maximale Fertigungs-Mengen
    ta_max_IDEAL = np.floor(
        ta_need_IDEAL * ta_rest * 1000 / prod_scen[4]).astype(int)
    ta_max_SOLID = (pPROD_cap[2]
                    - prod_scen[4] / 1000 * ta_max_IDEAL).astype(int)
    
    #---------##---------##---------##---------##--------##--------##--------#
    # effektive Fertigungs-Mengen
    prod_SOLID = np.min(
        np.vstack((
            pPROD_plan[0],
            emp_max_SOLID,
            ta_max_SOLID)), axis = 0).astype(int)
    prod_IDEAL = np.min(
        np.vstack((
            pPROD_plan[1],
            emp_max_IDEAL,
            ta_max_IDEAL)), axis = 0).astype(int)
       
    #---------##---------##---------##---------##--------##--------##--------#
    # eingesetzte Fertigungs-Kapazitäten 1: Fertigungspersonal
    # Auslastung: capacity utilization
    emp_eff_SOLID = prod_SOLID / 1000 * emp_prod_SOLID
    emp_eff_IDEAL = prod_IDEAL / 1000 * emp_prod_IDEAL
    emp_eff = emp_eff_SOLID + emp_eff_IDEAL
    emp_cap_ut = emp_eff / pPROD_cap[0]
    
    #---------##---------##---------##---------##--------##--------##--------#
    # eingesetzte Fertigungs-Kapazitäten 2: Technische Anlagen und Maschinen
    # Auslastung: capacity utilization
    ta_eff_SOLID = prod_SOLID
    ta_eff_IDEAL = (prod_scen[4] / 1000 * prod_IDEAL).astype(int)
    ta_eff = ta_eff_SOLID + ta_eff_IDEAL
    ta_cap_ut = ta_eff / pPROD_cap[2]

    return (np.vstack((prod_SOLID, prod_IDEAL)), 
            np.around(np.vstack((emp_cap_ut, ta_cap_ut)), 4))


#--------##--------##--------##--------##--------##--------##--------##--------#
# Marktmodell: Arbeitsmarkt
#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Wirkung der HR-Maßnahmen
def pDec_effects(pHR_means,pHR_effect0):
    """Berechnet Wirkung der HR-Maßnahmen"""

    # benötigt: pHR_means(4x2)
    # pDec_HR_h[:, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    
    # benötigt: pHR_effect0(12x3)
    # pRes_HR_h[0:12, co, PERIOD+OFFSET-2:PERIOD+OFFSET+1]
    
    # berechnet: pDec_eff = [gp_eff, ep_eff, pe_eff, ap_eff]
    #            pHR_ar0   (aktualisierte Startwerte für AR1-Prozesse)
    # pRes_HR_h[8:12, co, PERIOD+OFFSET]
    # pRes_HR_h[[0, 3, 4, 6], co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Referenzwerte
    REF_ALTER_TA = 4.0
    
    #-- AR(1)-Parameter für Entgelt-/Gehaltspolitik (GP): Faktor 2: Gehaltskürzungen
    GP2_AR1 = 0.5
    #-- AR(1)-Parameter für Einstellungspolitik (EP): Faktor 2: Entlassungen
    EP2_AR1 = 0.5
    #-- ARMA(1,1)-Parameter für Personalentwicklung (PE)
    PE_AR1  = 0.2
    #   --  [0.10, 0.90] * (1 - 0.2)
    PE_MA1  = [0.08, 0.72]
    #-- ARMA(1,1)-Parameter für Arbeitsplatzausstattung (AP)
    AP_AR1  = 0.4
    #   --  [0.20, 0.80] * (1 - 0.4)
    AP_MA1  = [0.12, 0.48]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # Entgelt-/Gehaltspolitik-Wirkung (GP)
    f1_ar = pHR_means[2, 1]
    gp2_ar = pHR_effect0[0, 1]*GP2_AR1 + min(f1_ar-pHR_means[2, 0], 0)*(1-GP2_AR1)
    gp_eff = round(f1_ar + gp2_ar, 4)
    gp2_ar = round(gp2_ar, 4)
    
    # Einstellungspolitik (EP)
    ep1_ar = pHR_effect0[2, 1]/pHR_effect0[1, 0]
    ep2_ar = pHR_effect0[4, 1]*EP2_AR1 + min(f1_ar, 0)*(1-EP2_AR1)
    ep_eff = round(ep1_ar + ep2_ar, 4)
    ep1_ar = round(ep1_ar, 4)
    ep2_ar = round(ep2_ar, 4)
    
    # Personalentwicklung (PE)
    f1_ar = np.divide(1000*pHR_means[1, :], pHR_effect0[1, 0:2])
    pe_eff = round(pHR_effect0[10, 1]*PE_AR1 + ma_value(f1_ar, PE_MA1), 3)
    
    # Arbeitsplatzausstattung (AP)
    f1_ar = np.divide(1000*pHR_means[3, :], pHR_effect0[5, 0:2])
    ap1_ar = round(pHR_effect0[6, 1]*AP_AR1 + ma_value(f1_ar, AP_MA1), 3)
    f2_ar = 20*(REF_ALTER_TA-pHR_effect0[7, 1])
    ap_eff = ap1_ar + f2_ar
    ap1_ar = round(ap1_ar, 3)
    
    pDec_eff = [gp_eff, ep_eff, pe_eff, ap_eff]
    pHR_ar0  = [gp2_ar, ep1_ar, ep2_ar, ap1_ar]
    
    return pDec_eff, pHR_ar0


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Arbeitgeber-Image (brand strength: employer)
def bs_emp(pHR_input):
    """Berechnet Arbeitgeber-Image (brand strength: employer)"""

    # benötigt: pHR_input(11x2)
    # pRes_HR_h[8:12, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    # szenario['eMA'][:, PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    # fRes_COMP_h[[0, 4, 7, 8], co, PERIOD+OFFSET-2:PERIOD+OFFSET]
    # pRes_HR_h[16, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    
    # berechnet: bs_emp
    # pRes_HR_h[16, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Referenzwerte
    REF_CO_SUCC1 = 0.05
    REF_CO_SUCC2 = 0.07
    
    #-- AR(1)-Parameter für AG-Image
    BS_EMP_AR1 = 0.2
    
    #-- Gewichte für BS-Index
    BS_EMP_W = [0.40, 0.10, 0.25, 0.15, 0.025, 0.025, 0.05]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Entgelt-/Gehaltspolitik (vs. Szenario)
    IF_BS_EMP   = np.array([[[ -0.0250, -0.0150, -0.0100, -0.0075, -0.0050, -0.0025,  0.0000,  0.0050,  0.0100,  0.0150,  0.0200,  0.0300,  0.0400,  0.0500,  0.1000],
                             [ -5.80  , -3.80  , -2.70  , -2.10  , -1.45  , -0.75  ,  0.00  ,  0.60  ,  1.30  ,  2.10  ,  3.00  ,  5.00  ,  7.40  ,  8.60  , 11.60  ]],
    # Einstellungspolitik (vs. Szenario)
                            [[ -1.00  , -0.50  , -0.10  , -0.05  , -0.02  , -0.01  ,  0.00  ,  0.01  ,  0.02  ,  0.05  ,  0.10  ,  0.20  ,  0.50  ,  1.00  ,  3.00  ],
                             [-21.36  ,-11.36  , -2.56  , -1.36  , -0.58  , -0.30  ,  0.00  ,  0.20  ,  0.38  ,  0.86  ,  1.56  ,  2.76  ,  5.76  ,  9.76  , 21.76  ]],
    # Personalentwicklung
                            [[    0   ,  300   ,  600   ,  800   , 1000   , 1100   , 1200   , 1300   , 1400   , 1600   , 1800   , 2000   , 3000   , 5000   ,10000   ],
                             [  -17.4 ,  -14.4 ,  -10.2 ,   -6.2 ,   -2.6 ,   -1.2 ,    0.0 ,    2.4 ,    4.6 ,    8.6 ,   12.2 ,   15.4 ,   23.4 ,   31.4 ,   41.4 ]],
    # Arbeitsplatzausstattung
                            [[    0   ,  100   ,  200   ,  300   ,  400   ,  450   ,  500   ,  550   ,  600   ,  700   ,  800   ,  900   , 1000   , 2000   , 5000   ],
                             [   -9.5 ,   -6.5 ,   -4.1 ,   -2.1 ,   -0.7 ,   -0.2 ,    0.0 ,    0.7 ,    1.3 ,    2.3 ,    3.1 ,    3.7 ,    4.1 ,    6.1 ,    9.1 ]],
    # Unternehmenserfolg 1 (GK-Rendite VP)
                            [[ -0.50  , -0.20  , -0.10  , -0.05  , -0.03  , -0.02  , -0.01  ,  0.00  ,  0.01  ,  0.02  ,  0.03  ,  0.05  ,  0.10  ,  0.20  ,  0.50  ],
                             [-28.1   ,-16.1   , -9.1   , -5.1   , -3.3   , -2.3   , -1.2   ,  0.0   ,  1.2   ,  2.3   ,  3.3   ,  5.1   ,  9.1   , 16.1   , 28.1   ]],
    # Unternehmenserfolg 2 (CFO-Rendite VP)
                            [[ -0.50  , -0.20  , -0.10  , -0.05  , -0.03  , -0.02  , -0.01  ,  0.00  ,  0.01  ,  0.02  ,  0.03  ,  0.05  ,  0.10  ,  0.20  ,  0.50  ],
                             [-28.1   ,-16.1   , -9.1   , -5.1   , -3.3   , -2.3   , -1.2   ,  0.0   ,  1.2   ,  2.3   ,  3.3   ,  5.1   ,  9.1   , 16.1   , 28.1   ]],
    # Unternehmenserfolg 3 (Zinsaufschlag/Rating VP)
                            [[  0.0000,  0.0001,  0.0002,  0.0003,  0.0004,  0.0005,  0.0007,  0.0010,  0.0015,  0.0020,  0.0030,  0.0040,  0.0080,  0.0100,  0.0200],
                             [ 15.4   , 10.4   ,  7.4   ,  5.4   ,  3.9   ,  2.9   ,  1.5   ,  0.0   , -0.5   , -1.2   , -3.2   , -6.2   ,-14.2   ,-16.2   ,-24.2   ]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # aktuelles AG-Image (brand strength: employer)
    bs_emp = 100.0
    
    # Entgelt-/Gehaltspolitik (GP)
    factor = pHR_input[0, 1] - pHR_input[4, 1]
    bs_emp += BS_EMP_W[0]*round(stepwise_linear_function(
        IF_BS_EMP[0], factor), 2)
    
    # Einstellungspolitik (EP)
    factor = pHR_input[1, 1] - pHR_input[5, 1]
    bs_emp += BS_EMP_W[1]*round(stepwise_linear_function(
        IF_BS_EMP[1], factor), 2)
    
    # Personalentwicklung (PE)
    factor = pHR_input[2, 1]
    bs_emp += BS_EMP_W[2]*round(stepwise_linear_function(
        IF_BS_EMP[2], factor), 2)
    
    # Arbeitsplatzausstattung (AP)
    factor = pHR_input[3, 1]
    bs_emp += BS_EMP_W[3]*round(stepwise_linear_function(
        IF_BS_EMP[3], factor), 2)
    
    # Unternehmenserfolg 1 (GK-Rendite VP)
    factor = pHR_input[6, 1]/pHR_input[8, 0] - REF_CO_SUCC1
    bs_emp += BS_EMP_W[4]*round(stepwise_linear_function(
        IF_BS_EMP[4], factor), 2)
    
    # Unternehmenserfolg 2 (CFO-Rendite VP)
    factor = pHR_input[7, 1]/pHR_input[8, 0] - REF_CO_SUCC2
    bs_emp += BS_EMP_W[5]*round(stepwise_linear_function(
        IF_BS_EMP[5], factor), 2)
    
    # Unternehmenserfolg 3 (Zinsaufschlag/Rating VP)
    factor = pHR_input[9, 1]
    bs_emp += BS_EMP_W[6]*round(stepwise_linear_function(
        IF_BS_EMP[6], factor), 2)
    
    bs_emp = round(pHR_input[10, 0]*BS_EMP_AR1 + bs_emp*(1-BS_EMP_AR1), 2)

    return bs_emp


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Mitarbeiter-Produktivität (Personalentwicklung)
def pe_prod(pHR_pe):
    """Berechnung der Steigerung der Mitarbeiter-Produktivität durch Personalentwicklung"""

    # benötigt: pHR_pe(1)                   (Personalentwicklung)
    # pRes_HR_h[10, co, PERIOD+OFFSET]
    
    # berechnet: hr_prod_pe                 (MA-Produktivität)
    # pRes_HR_h[15, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # benötigte Wirkungsfunktionen (impact factor)
    IF_HR_DEV = np.array([[      0,    300,    600,    800,   1000,   1100,   1200,   1300,   1400,   1600,   1800,   2000,   3000,   5000,  20000],
                          [ 0.9780, 0.9846, 0.9906, 0.9942, 0.9974, 0.9988, 1.0000, 1.0010, 1.0022, 1.0050, 1.0082, 1.0106, 1.0186, 1.0266, 1.0566]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # Personalentwicklungspolitik (PE)
    hr_prod_pe = round(stepwise_linear_function(IF_HR_DEV, pHR_pe), 4)

    return hr_prod_pe


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Mitarbeiter-Motivation (employee motivation)
def emp_motivation(pHR_input):
    """Berechnet Mitarbeiter-Motivation (employee motivation) für alle Unternehmen"""

    # benötigt: pHR_input(7 x NUM_COMPANIES)
    # pRes_HR_h[8:12, :, PERIOD+OFFSET]       (HR-Politik Wirkungen)
    # pRes_HR_h[12, :, PERIOD+OFFSET-1]       (Auslastungsgrad VP)
    # pRes_HR_h[16, :, PERIOD+OFFSET]         (AG-Image)
    # pRes_HR_h[17, :, PERIOD+OFFSET-1]       (MA-Motivation VP)
    
    # berechnet: emp_mot
    # pRes_HR_h[17, :, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Anzahl Unternehmen
    NUM_COMPANIES = pHR_input.shape[1]
    
    # Referenzwerte
    REF_BS_EMP = 100
    
    #-- AR(1)-Parameter für AG-Image
    EMP_MOT_AR1 = 0.2
    
    #-- Gewichte für BS-Index
    EMP_MOT_W = [0.20, 0.07, 0.15, 0.10, 0.08, 0.40]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Entgelt-/Gehaltspolitik (vs. Konkurrenz)
    IF_EMP_MOT  = np.array([[[ -0.20 , -0.10 , -0.05 , -0.04 , -0.03 , -0.02 , -0.01 ,  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.04 ,  0.05 ,  0.10 ,  0.20 ],
                             [-14.0  , -8.0  , -4.0  , -3.0  , -2.1  , -1.3  , -0.6  ,  0.0  ,  0.5  ,  1.1  ,  1.8  ,  2.6  ,  3.5  ,  8.5  , 16.5  ]],
    # Einstellungspolitik
                            [[ -1.00 , -0.50 , -0.20 , -0.10 , -0.05 ,  0.00 ,  0.10 ,  0.20 ,  0.25 ,  0.30 ,  0.40 ,  0.50 ,  0.70 ,  1.00 ,  2.00 ],
                             [-46.5  ,-36.5  ,-12.5  , -5.5  , -2.5  ,  0.0  ,  4.0  ,  5.0  ,  3.0  ,  0.0  , -4.0  , -7.0  ,-12.0  ,-18.0  ,-28.0  ]],
    # Arbeitsbelastung
                            [[  0.00 ,  0.40 ,  0.50 ,  0.60 ,  0.70 ,  0.80 ,  0.85 ,  0.90 ,  0.95 ,  0.98 ,  1.00 ,  1.02 ,  1.10 ,  1.12 ,  1.20 ],
                             [-41.0  ,-33.0  ,-29.0  ,-23.0  ,-15.0  , -5.0  , -1.0  ,  2.0  ,  4.0  , 10.0  ,  2.0  ,  6.0  ,-10.0  , -2.0  ,-10.0  ]],
    # Pers.Entwicklung (vs. Konkurrenz)
                            [[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  3.00 ],
                             [-60.0  ,-35.0  ,-17.5  ,-13.0  , -9.0  , -5.5  , -2.5  ,  0.0  ,  2.0  ,  4.5  ,  7.5  , 11.0  , 15.0  , 37.5  ,212.5  ]],
    # Arbeitsplatz (vs. Konkurrenz)
                            [[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  3.00 ],
                             [-60.0  ,-35.0  ,-17.5  ,-13.0  , -9.0  , -5.5  , -2.5  ,  0.0  ,  2.0  ,  4.5  ,  7.5  , 11.0  , 15.0  , 37.5  ,212.5  ]],
    # AG-Image (vs. Referenz 100)
                            [[-50    ,-20    ,-10    , -5    , -3    , -2    , -1    ,  0    ,  1    ,  2    ,  3    ,  5    , 10    , 20    , 50    ],
                             [-28.1  ,-16.1  , -9.1  , -5.1  , -3.3  , -2.3  , -1.2  ,  0.0  ,  1.2  ,  2.3  ,  3.3  ,  5.1  ,  9.1  , 16.1  , 28.1  ]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # aktuelle Mitarbeiter-Motivation (employee motivation)
    emp_mot = 100.0*np.ones(NUM_COMPANIES)
    
    pHR_mean = pHR_input.mean(axis=1)
    
    for comp in range(NUM_COMPANIES): 
        # Entgelt-/Gehaltspolitik GP (vs. Konkurrenz)
        factor = pHR_input[0, comp] - pHR_mean[0]
        emp_mot[comp] += EMP_MOT_W[0]*round(stepwise_linear_function(
            IF_EMP_MOT[0], factor), 2)

        # Einstellungspolitik EP
        factor = pHR_input[1, comp]
        emp_mot[comp] += EMP_MOT_W[1]*round(stepwise_linear_function(
            IF_EMP_MOT[1], factor), 2)
        
        # Arbeitsbelastung AB
        factor = pHR_input[4, comp]
        emp_mot[comp] += EMP_MOT_W[2]*round(stepwise_linear_function(
            IF_EMP_MOT[2], factor), 2)
        
        # Pers.Entwicklung PE (vs. Konkurrenz)
        factor = pHR_input[2, comp]/pHR_mean[2]-1
        emp_mot[comp] += EMP_MOT_W[3]*round(stepwise_linear_function(
            IF_EMP_MOT[3], factor), 2)
        
        # Arbeitsplatz AP (vs. Konkurrenz)
        factor = pHR_input[3, comp]/pHR_mean[3]-1
        emp_mot[comp] += EMP_MOT_W[4]*round(stepwise_linear_function(
            IF_EMP_MOT[4], factor), 2)
        
        # AG-Image (vs. Referenz 100)
        factor = pHR_input[5, comp] - REF_BS_EMP
        emp_mot[comp] += EMP_MOT_W[5]*round(stepwise_linear_function(
            IF_EMP_MOT[5], factor), 2)
        
        emp_mot[comp] = round(pHR_input[6, comp]*EMP_MOT_AR1 + emp_mot[comp]*(1-EMP_MOT_AR1), 2)

    return emp_mot


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Effekte der MA-Motivation (employee motivation)
# Produktivität / Fluktuation / Fehlzeiten
def em_effects(pHR_mot):
    """Berechnung der Effekte der Mitarbeiter-Motivation: Produktivität/Fluktuation/Fehlzeiten"""

    # benötigt: pHR_mot(1)                  (MA-Motivation)
    # pRes_HR_h[17, co, PERIOD+OFFSET]
    
    # berechnet: em_effects                 (MA-Produktivität/Fluktuation/Fehlzeiten)
    # pRes_HR_h[18:21, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Referenzwerte
    REF_EMP_MOT = 100
    
    # benötigte Wirkungsfunktionen (impact factor)
    # MA-Produktivität
    IF_EMP_MOT = np.array([[[-50    ,-20    ,-10    , -5    , -3    , -2    , -1    ,  0    ,  1    ,  2    ,  3    ,  5    , 10    , 20    , 50    ],
                            [ 0.9495, 0.9645, 0.9745, 0.9870, 0.9950, 0.9975, 0.9990, 1.0000, 1.0010, 1.0025, 1.0045, 1.0095, 1.0245, 1.0345, 1.0495]],
    # MA-Fluktuation
                           [[-50    ,-20    ,-10    , -5    , -3    , -2    , -1    ,  0    ,  1    ,  2    ,  3    ,  5    , 10    , 20    , 50    ],
                            [ 0.448 , 0.328 , 0.248 , 0.198 , 0.182 , 0.176 , 0.172 , 0.170 , 0.169 , 0.167 , 0.164 , 0.156 , 0.131 , 0.111 , 0.081 ]],
    # MA-Fehlzeiten
                           [[-50    ,-20    ,-10    , -5    , -3    , -2    , -1    ,  0    ,  1    ,  2    ,  3    ,  5    , 10    , 20    , 50    ],
                            [ 0.0828, 0.0648, 0.0568, 0.0518, 0.0486, 0.0472, 0.0460, 0.0450, 0.0449, 0.0447, 0.0444, 0.0436, 0.0411, 0.0391, 0.0361]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # MA-Motivation
    factor = pHR_mot - REF_EMP_MOT
    em_eff_pr = np.around(stepwise_linear_function(IF_EMP_MOT[0], factor), 4)
    em_eff_fl = np.around(stepwise_linear_function(IF_EMP_MOT[1], factor), 4)
    em_eff_fz = np.around(stepwise_linear_function(IF_EMP_MOT[2], factor), 4)

    return np.vstack((em_eff_pr, em_eff_fl, em_eff_fz))


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Arbeitsmarkt-Produktivität (labour market productivity)
def lm_prod(pHR_input):
    """Berechnet Arbeitsmarkt-Produktivität (labour market productivity) für alle Unternehmen"""

    # benötigt: pHR_input(5 x NUM_COMPANIES)
    # pRes_HR_h[8:12, :, PERIOD+OFFSET]       (HR-Politik Wirkungen)
    # pRes_HR_h[14, :, PERIOD+OFFSET-1]       (Arbeitsmarkt-Produktivität VP)
    
    # berechnet: lm_prod
    # pRes_HR_h[14, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Anzahl Unternehmen
    NUM_COMPANIES = pHR_input.shape[1]

    #-- AR(1)-Parameter für Arbeitsmarkt-Produktivität
    LM_PROD_AR1 = 0.2
    
    #-- Gewichte für Arbeitsmarkt-Produktivität
    LM_PROD_W   = [0.50, 0.35, 0.15]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Entgelt-/Gehaltspolitik (vs. Konkurrenz)
    IF_LM_PROD  = np.array([[[ -0.20 , -0.10 , -0.05 , -0.04 , -0.03 , -0.02 , -0.01 ,  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.04 ,  0.05 ,  0.10 ,  0.20 ],
                             [ -0.100, -0.060, -0.030, -0.022, -0.015, -0.009, -0.004,  0.000,  0.003,  0.007,  0.012,  0.018,  0.025,  0.055,  0.095]],
    # Pers.Entwicklung (vs. Konkurrenz)
                            [[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  3.00 ],
                             [ -0.028, -0.023, -0.018, -0.016, -0.013, -0.009, -0.004,  0.000,  0.003,  0.007,  0.012,  0.016,  0.019,  0.029,  0.079]],
    # Arbeitsplatz (vs. Konkurrenz)
                            [[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  3.00 ],
                             [ -0.028, -0.023, -0.018, -0.016, -0.013, -0.009, -0.004,  0.000,  0.003,  0.007,  0.012,  0.016,  0.019,  0.029,  0.079]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # aktuelle Arbeitsmarkt-Produktivität (labour market productivity)
    lm_prod = 0.95*np.ones(NUM_COMPANIES)
    
    pHR_mean = pHR_input.mean(axis=1)
    
    for comp in range(NUM_COMPANIES): 
        # Entgelt-/Gehaltspolitik GP (vs. Konkurrenz)
        factor = pHR_input[0, comp] - pHR_mean[0]
        lm_prod[comp] += LM_PROD_W[0]*round(stepwise_linear_function(
            IF_LM_PROD[0], factor), 4)
        
        # Pers.Entwicklung PE (vs. Konkurrenz)
        factor = pHR_input[2, comp]/pHR_mean[2]-1
        lm_prod[comp] += LM_PROD_W[1]*round(stepwise_linear_function(
            IF_LM_PROD[1], factor), 4)
        
        # Arbeitsplatz AP (vs. Konkurrenz)
        factor = pHR_input[3, comp]/pHR_mean[3]-1
        lm_prod[comp] += LM_PROD_W[2]*round(stepwise_linear_function(
            IF_LM_PROD[2], factor), 4)
        
        lm_prod[comp] = round(pHR_input[4, comp]*LM_PROD_AR1 + lm_prod[comp]*(1-LM_PROD_AR1), 4)

    return lm_prod


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Arbeitsmarkt-Angebot
def lm_supply(pHR_input, lms_scen):
    """Berechnung des effektiven Arbeitsmarkt-Angebotes (labour market supply)"""

    # benötigt: pHR_input(NUM_COMPANIES)    (Entgelt-/Gehaltspolitiken)
    # pRes_HR_h[8, :, PERIOD+OFFSET]
    
    # benötigt: lms_scen(1)                 (aktuelle Szenario-Werte)
    # szenario['eMA'][0, PERIOD+OFFSET]     (erwarteter Gehaltsaufschlag)
    # szenario['LohnNK'][5, PERIOD+OFFSET]  (Arbeitsmarkt-Angebot gemäß Szenario)
    
    # berechnet: lm_supply  (aktuelles Arbeitsmarkt-Angebot: labour market supply)
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # benötigte Wirkungsfunktionen (impact factor)
    # durchschnittlicher Gehaltsaufschlag (Entgelt-/Gehaltspolitik)
    IF_LMS = np.array([[ -0.100, -0.050, -0.040, -0.030, -0.020, -0.010, -0.005,  0.000,  0.010,  0.020,  0.030,  0.040,  0.050,  0.100,  0.200],
                       [ -0.120, -0.110, -0.105, -0.095, -0.075, -0.045, -0.025,  0.000,  0.040,  0.070,  0.095,  0.115,  0.130,  0.180,  0.230]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # Entgelt-/Gehaltspolitik (GP)
    factor = pHR_input.mean(axis=0) - lms_scen[0]
    lm_supply = round(lms_scen[1]*(1+stepwise_linear_function(IF_LMS, factor)), 0).astype(int)
    
    return lm_supply


#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne Arbeitsmarkt-Anteile -> potenzielles Arbeitsangebot
def lm_share(pHR_input):
    """Berechnung der Arbeitsmarkt-Anteile (potenzielles Arbeits-Angebot)"""
    
    # benötigt: pHR_input(4 x NUM_COMPANIES)
    # pRes_HR_h[8:12, :, PERIOD+OFFSET]  (HR-Politik Wirkungen)
    
    # berechnet: lm_share                (Marktanteil = potenzielles Angebot)
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Anzahl Unternehmen
    NUM_COMPANIES = pHR_input.shape[1]

    # benötigte Wirkungsfunktionen (impact factor)
    # Entgelt-/Gehaltspolitik GP (vs. Konkurrenz)
    IF_LMS = np.array([[[ -0.20 , -0.10 , -0.05 , -0.04 , -0.03 , -0.02 , -0.01 ,  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.04 ,  0.05 ,  0.10 ,  0.20 ],
                        [  0.702,  0.882,  0.957,  0.969,  0.979,  0.987,  0.994,  1.000,  1.004,  1.009,  1.015,  1.023,  1.033,  1.093,  1.243]],
    # Einstellungspolitik (vs. Konkurrenz)
                       [[ -0.20 , -0.10 , -0.05 , -0.04 , -0.03 , -0.02 , -0.01 ,  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.04 ,  0.05 ,  0.10 ,  0.20 ],
                        [  0.652,  0.752,  0.852,  0.892,  0.926,  0.956,  0.980,  1.000,  1.016,  1.036,  1.060,  1.090,  1.124,  1.324,  1.424]],
    # Pers.Entwicklung (vs. Konkurrenz)
                       [[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  3.00 ],
                        [  0.606,  0.806,  0.931,  0.951,  0.963,  0.973,  0.985,  1.000,  1.015,  1.027,  1.037,  1.049,  1.069,  1.159,  1.409]],
    # Arbeitsplatz (vs. Konkurrenz)
                       [[ -1.00 , -0.50 , -0.25 , -0.20 , -0.15 , -0.10 , -0.05 ,  0.00 ,  0.05 ,  0.10 ,  0.15 ,  0.20 ,  0.25 ,  0.50 ,  3.00 ],
                        [  0.783,  0.883,  0.958,  0.968,  0.976,  0.982,  0.990,  1.000,  1.010,  1.018,  1.024,  1.032,  1.042,  1.117,  1.617]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    # Initialisierung der Marktanteil-Abweichungen
    lm_share = np.ones(NUM_COMPANIES)
    
    pHR_mean = pHR_input.mean(axis=1)
    
    # Entgelt-/Gehaltspolitik GP (vs. Konkurrenz)
    deviation = pHR_input[0] - pHR_mean[0]
    lm_share *= stepwise_linear_function(IF_LMS[0], deviation)
    
    # Einstellungspolitik (vs. Konkurrenz)
    deviation = pHR_input[1] - pHR_mean[1]
    lm_share *= stepwise_linear_function(IF_LMS[1], deviation)
    
    # Pers.Entwicklung (vs. Konkurrenz)
    deviation = np.divide(pHR_input[2], pHR_mean[2])-1
    lm_share *= stepwise_linear_function(IF_LMS[2], deviation)
    
    # Arbeitsplatz (vs. Konkurrenz)
    deviation = np.divide(pHR_input[3], pHR_mean[3])-1
    lm_share *= stepwise_linear_function(IF_LMS[2], deviation)
    
    # Berechne Marktanteile
    lm_share = 1/NUM_COMPANIES*lm_share
    lm_share = lm_share/lm_share.sum()
    
    return lm_share


#--------##--------##--------##--------##--------##--------##--------##--------#
# Arbeitsmarkt-Modell:  Marktausgleich Angebot vs. Nachfrage
def hr_department(hr_dec, hr_res, lm_scen):
    """Berechnung der Einstellungen und Produktivitäten (effektives Arbeits-Angebot)"""
    
    # benötigt: hr_dec(2 x NUM_COMPANIES)
    # hr_dec = pRes_HR_h[1, :, PERIOD+OFFSET-1]   Anfangsbestand Fertigungs-MA
    #          pDec_HR_h[0, :, PERIOD+OFFSET]     Planbestand Fertigungs-MA

    # benötigt: hr_res(4 x NUM_COMPANIES)
    # hr_res = pRes_HR_h[13, :, PERIOD+OFFSET]    (indiv. Arbeitsmarkt-Angebot)
    #          pRes_HR_h[14, :, PERIOD+OFFSET]    (Produktivität: Arbeitsmarkt)
    #          pRes_HR_h[15, :, PERIOD+OFFSET]    (Produktivität: Personalentwicklung)
    #          pRes_HR_h[16, :, PERIOD+OFFSET]    (AG-Image)
    #          pRes_HR_h[17, :, PERIOD+OFFSET]    (nicht benötigt: MA-Motivation)
    #          pRes_HR_h[18, :, PERIOD+OFFSET]    (Produktivität: MA-Motivation)
    #          pRes_HR_h[19, :, PERIOD+OFFSET]    (Fluktuation)
    #          pRes_HR_h[20, :, PERIOD+OFFSET]    (Fehlzeiten)
    #          pRes_HR_h[21, :, PERIOD+OFFSET-1]  (Produktivität: Gesamt (VP))
    #          lm_share

    # benötigt: lm_scen (1)
    # lm_scen = szenario['LohnNK'][7, PERIOD+OFFSET]

    # berechnet:  emp_act         (tatsächliche Fertigungs-Mitarbeiter)
    #             emp_prod        (tatsächliche Produktivität (Gesamt))
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Referenzwerte
    REF_BS_EMP = 100

    # Anzahl Unternehmen
    NUM_COMPANIES = hr_dec.shape[1]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Arbeitssuchende: ca. 60% der Arbeitssuchenden wechseln auch zu anderem Arbeitgeber
    IF_AR  = np.array([[[ -0.50 , -0.20 , -0.10 , -0.05 , -0.03 , -0.02 , -0.01 ,  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.05 ,  0.10 ,  0.20 ,  0.50 ],
                        [  0.182,  0.362,  0.462,  0.532,  0.564,  0.578,  0.590,  0.600,  0.602,  0.606,  0.612,  0.628,  0.678,  0.738,  0.798]],
    # Entlassene: 80% der gerade Entlassenen wechseln direkt zu anderem Arbeitgeber
                       [[ -0.50 , -0.20 , -0.10 , -0.05 , -0.03 , -0.02 , -0.01 ,  0.00 ,  0.01 ,  0.02 ,  0.03 ,  0.05 ,  0.10 ,  0.20 ,  0.50 ],
                        [  0.202,  0.502,  0.642,  0.732,  0.764,  0.778,  0.790,  0.800,  0.801,  0.803,  0.807,  0.819,  0.839,  0.859,  0.889]]])
    
    #--------##--------##--------##--------##--------##--------##--------#
    lm_scen = lm_scen.astype(int)
    hr_dec = hr_dec.astype(int)
    
    # maximale Entlassungen (Szenario: Betriebsrat)
    lm_dismiss_max = lm_scen*np.ones(NUM_COMPANIES, dtype=int)
    
    # Arbeitsmarkt-Nachfrage
    emp_retent = hr_dec[0, :]
    emp_to_abs = np.around((hr_res[6] + hr_res[7])*emp_retent, 0).astype(int)
    emp_plan   = hr_dec[1, :]
    lm_demand  = emp_plan - emp_retent + emp_to_abs
    
    # Einstellungen (recruits)/Entlassungen (dismissals)
    lm_demand0 =  np.amax(
        np.vstack((lm_demand,
                   np.zeros(NUM_COMPANIES, dtype=int))), axis=0)
    lm_supply0 = -np.amin(
        np.vstack((lm_demand,
                   np.zeros(NUM_COMPANIES, dtype=int))), axis=0)
    
    # Einstellungen/Entlassungen (0: direkt)
    lm_recruit =  np.amin(
        np.vstack((lm_demand0,
                   hr_res[0].astype(int))), axis = 0)
    lm_dismiss =  np.amin(
        np.vstack((lm_supply0,
                   lm_dismiss_max)), axis = 0)
    
    # Rest-Nachfrage
    lm_demand1 =  np.amax(
        np.vstack((lm_demand - lm_recruit,
                   np.zeros(NUM_COMPANIES, dtype=int))), axis=0)
    
    # Marktanteil am Restangebot 
    lm_share1 = hr_res[9]
    lm_share1[lm_demand1==0] = 0
    if lm_share1.sum()!=0:
        lm_share1 = lm_share1/lm_share1.sum()
    
    # Rest-Angebot: weiter Arbeitssuchende
    deviation = hr_res[3]/REF_BS_EMP-1
    lm_supply1 = np.floor(lm_share1
                          * (stepwise_linear_function(IF_AR[0], deviation)
                          * (hr_res[0] - lm_recruit).sum()
                          +  stepwise_linear_function(IF_AR[1], deviation)
                          * lm_dismiss.sum())).astype(int)
    lm_recruit +=  np.amin(np.vstack((lm_demand1, lm_supply1)), axis = 0)

    # tatsächliche Fertigungs-Mitarbeiter
    emp_act = emp_retent - emp_to_abs + lm_recruit - lm_dismiss

    # effektive MA-Produktivität (Gesamt)
    emp_prod = np.around(
        np.divide((emp_retent - emp_to_abs - lm_dismiss)
                  * hr_res[8]
                  * hr_res[2]
                  * hr_res[5]
                  + lm_recruit * hr_res[1],
                  emp_act), 4)
    
    return np.vstack((emp_act, lm_recruit)), emp_prod


#--------##--------##--------##--------##--------##--------##--------##--------#
# Finanzmarkt
#--------##--------##--------##--------##--------##--------##--------##--------#
# Berechne aktuelles Unternehmens-Rating (und Zinsaufschlag)
def rating(fCOMP_input):
    """Berechnet aktuelles Unternehmens-Rating (inkl. Zinsaufschlag)"""

    # benötigt: fCOMP_input(4 x 2)
    # fRes_COMP_h[4:8, co, PERIOD+OFFSET-1:PERIOD+OFFSET+1]
    
    # berechnet: yield_spread, comp_rating
    # pRes_HR_h[16, co, PERIOD+OFFSET]
    
    #--------##--------##--------##--------##--------##--------##--------#
    # KONSTANTEN
    #--------##--------##--------##--------##--------##--------##--------#
    # Referenzwerte
    REF_YIELD_SPREAD = [0     , 0.0005, 0.0010, 0.0015, 0.0020, 0.0025, 0.0030, 0.0040, 0.0050, 0.0060, 0.0080, 0.0100, 0.0120, 0.0150, 0.0200]
    REF_RATING       = ['AA+' , 'AA'  , 'AA-' , 'A+'  , 'A'   , 'A-'  , 'BBB+', 'BBB' , 'BBB-', 'BB+' , 'BB'  , 'BB-' , 'B'   , 'CCC' , 'CC'  ] 
    
    #-- Gewichte für Rating
    RAT_WEIGHTS = [0.50, 0.20, 0.30]
    
    # benötigte Wirkungsfunktionen (impact factor)
    # Unternehmenserfolg 1 (Verschuldungsgrad: FK/GK)
    IF_RAT = np.array([[[ 0.00  , 0.40  , 0.50  , 0.55  , 0.60  , 0.65  , 0.70  , 0.75  , 0.80  , 0.84  , 0.88  , 0.92  , 0.95  , 0.98  , 1.00  ],
                        [ 0.0000, 0.0000, 0.0001, 0.0002, 0.0004, 0.0008, 0.0013, 0.0019, 0.0027, 0.0035, 0.0045, 0.0057, 0.0069, 0.0084, 0.0096]],
    # Unternehmenserfolg 2 (Bonität/Selbstfinanzierungsgrad: FK/CFO)
                       [[ 0.00  , 2.00  , 3.00  , 4.00  , 5.00  , 6.00  , 7.00  , 8.00  , 9.00  ,10.00  ,12.00  ,15.00  ,20.00  ,25.00  ,50.00  ],
                        [ 0.0000, 0.0000, 0.0001, 0.0002, 0.0003, 0.0005, 0.0007, 0.0010, 0.0013, 0.0016, 0.0020, 0.0026, 0.0036, 0.0041, 0.0066]],
    # Unternehmenserfolg 3 (Besicherung/Deckungsgrad: FK/AV)
                       [[ 0.00  , 0.60  , 0.80  , 1.00  , 1.10  , 1.20  , 1.30  , 1.40  , 1.50  , 1.60  , 1.80  , 2.00  , 2.50  , 3.00  , 5.00  ],
                        [ 0.0000, 0.0001, 0.0004, 0.0010, 0.0014, 0.0018, 0.0022, 0.0026, 0.0030, 0.0034, 0.0044, 0.0055, 0.0085, 0.0120, 0.0260]]])
 
    #--------##--------##--------##--------##--------##--------##--------#
    # aktueller Zinsaufschlag
    yield_spread = 0.0
    
    # Unternehmenserfolg 1 (Verschuldungsgrad: FK/GK)
    factor = fCOMP_input[2, 1] / fCOMP_input[3, 1]
    yield_spread += RAT_WEIGHTS[0]*round(stepwise_linear_function(
        IF_RAT[0], factor), 4)
    
    # Unternehmenserfolg 2 (Bonität/Selbstfinanzierungsgrad: FK/CFO)
    factor = fCOMP_input[2, 0] / fCOMP_input[0, 1]
    yield_spread += RAT_WEIGHTS[1]*round(stepwise_linear_function(
        IF_RAT[1], factor), 4)
    
    # Unternehmenserfolg 3 (Besicherung/Deckungsgrad: FK/AV)
    factor = fCOMP_input[2, 1] / fCOMP_input[1, 1]
    yield_spread += RAT_WEIGHTS[2]*round(stepwise_linear_function(
        IF_RAT[2], factor), 4)
    
    yield_spread = round(yield_spread, 4)
    
    ndx = np.searchsorted(REF_YIELD_SPREAD, yield_spread, side='right')
    comp_rating = REF_RATING[ndx-1]
    
    return yield_spread, comp_rating

import json

class Pdc :
  def __init__(self):
    pass
  
  def find(self):
    # TODO Get data frm mssql client
    json_data = [
      {
        "EMPLOYEE": "falozano",
        "TSTAMP": "2024-09-14 17.17.52",
        "TYPE": "ASM     ",
        "ACTION": "RPL",
        "ID": "H2 0473",
        "IDDATE": "2024-09-17",
        "DETAILS": "ASM\nLT\nRPL AIRS\nH2473/17SEP24\nJ 32Q YKVHSBLRTMNQZXAUEOG.F00C00Y238\nCJC1006 LSC1146\nLSC1221 SCL1322\nCJCLSC 505/ET\nLSCSCL 505/ET\nSI MSG REF NUM 824141\n//\n473 17SEP24 J 320 (32N) Y186 CJC1006 LSC1146 LSC1221 SCL1322",
        "audits": ["66e5c5c56b0bba6b81169ebb", "66e5c5c66b0bba6b81169ec0", "66e5c5c66b0bba6b81169ec5"]
      },
      {
        "EMPLOYEE": "nbuccicardi",
        "TSTAMP": "2024-09-15 10.47.33",
        "TYPE": "ASM     ",
        "ACTION": "RPL",
        "ID": "H2 0473",
        "IDDATE": "2024-09-17",
        "DETAILS": "ASM\nLT\nRPL AIRS\nH2473/17SEP24\nJ 32N YKVHSBLRTMNQZXAUEOG.F00C00Y186\nCJC1006 LSC1146\nLSC1221 SCL1322\nCJCLSC 505/ET\nLSCSCL 505/ET\nSI MSG REF NUM 824342\n//\n473 17SEP24 J 321 (32Q) Y238 CJC1006 LSC1146 LSC1221 SCL1322"
      },
      {
        "EMPLOYEE": "katyjime",
        "TSTAMP": "2024-09-14 17.45.45",
        "TYPE": "ASM     ",
        "ACTION": "TIM",
        "ID": "H2 0433",
        "IDDATE": "2024-09-16",
        "DETAILS": "ASM\nLT\nTIM OPER\nH2433/16SEP24\nSCL1404 PMC1551\nPMC1626 BBA1734\nSI MSG REF NUM 824049\n//\n433 16SEP24 J 320 (32N) Y186 SCL1200 PMC1347 PMC1422 BBA1530"
      },
      {
        "EMPLOYEE": "katyjime",
        "TSTAMP": "2024-09-14 17.45.45",
        "TYPE": "ASM     ",
        "ACTION": "TIM",
        "ID": "H2 0434",
        "IDDATE": "2024-09-16",
        "DETAILS": "ASM\nLT\nTIM OPER\nH2434/16SEP24\nBBA1819 PMC1929\nPMC2004 SCL2149\nSI MSG REF NUM 824050\n//\n434 16SEP24 J 320 (32N) Y186 BBA1615 PMC1725 PMC1800 SCL1945"
      },
      {
        "EMPLOYEE": "katyjime",
        "TSTAMP": "2024-09-15 11.15.55",
        "TYPE": "ASM     ",
        "ACTION": "TIM",
        "ID": "H2 0462",
        "IDDATE": "2024-09-17",
        "DETAILS": "ASM\nLT\nTIM OPER\nH2462/17SEP24\nSCL1615 LSC1723\nLSC1808 IQQ1956\nSI MSG REF NUM 824445\n//\n462 17SEP24 J 321 (32Q) Y238 SCL1600 LSC1708 LSC1753 IQQ1941"
      }
    ]
    return json.loads(json.dumps(json_data, indent=2))
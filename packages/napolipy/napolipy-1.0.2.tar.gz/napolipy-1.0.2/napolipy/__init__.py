"""
I Know that having functions here is a bad idea,
but I couldn't find a way to not "from napolipy import napolipy"
so here we are
"""

__version__ = "1.0"
__author__ = "Adriano Oliviero"


def gen_logo():
    ESC = "\x1b"
    LBFG = ESC + "[94m"  # Light Blue ForeGround
    DBFG = ESC + "[34m"  # Dark Blue ForeGround
    WFG = ESC + "[97m"  # White ForeGround
    LBBG = ESC + "[104m"  # Light Blue BackGround
    RS = ESC + "[0m"  # Reset

    TLB = "\u2588"  # Tall Large Block
    HB = "\u2584"  # Half Block
    HHB = "\u2583"  # Half Half Block
    HHHUB = "\u2594"  # Half Half Half Upper Block
    HHHLB = "\u2581"  # Half Half Half Lower Block
    DB = "\u259a"  # Diagonal Block
    TLUB = "\u259B"  # Triangular Left Upper Block
    TLLB = "\u2599"  # Triangular Left Lower Block
    TRUB = "\u259C"  # Triangular Right Upper Block
    TRLB = "\u259F"  # Triangular Right Lower Block
    LLB = "\u2596"  # Left Lower Block
    LUB = "\u2598"  # Left Upper Block
    RLB = "\u2597"  # Right Lower Block
    RUB = "\u259D"  # Right Upper Block

    VNP = WFG + TLB + LBFG  # Vertical N Part
    EUNP = WFG + HHHUB + LBFG  # Starting Upper N Part
    ELNP = WFG + HHHLB + LBFG  # Starting Lower N Part
    TLNP = WFG + LBBG + TLLB + LBFG  # Triangular Left N Part
    TRNP = WFG + LBBG + TRUB + LBFG  # Triangular Right N Part

    LLNE = WFG + LBBG + LLB + LBFG  # Left Lower N Extension
    RUNE = WFG + LBBG + RUB + LBFG  # Right Upper N Extension
    HNE = WFG + LBBG + HB + LBFG  # Left Lower N Extension

    return f"""       {DBFG + (HHB * 12) + RS}
     {DBFG + TRLB + (TLB * 14) + TLLB + RS}
   {DBFG + TRLB + (TLB * 5) + LBBG + TLUB + LBFG + (TLB * 6) + DBFG + TRUB + RS + DBFG + (TLB * 5) + TLLB + RS}
 {DBFG + TRLB + (TLB * 4) + LBBG + TLUB + LBFG + (TLB * 4) + (TLB * 4) + (TLB * 4) + DBFG + TRUB + RS + DBFG + (TLB * 4) + TLLB + RS}
{DBFG + LBBG + (TLB * 4) + TLUB + LBFG + (TLB * 2) + EUNP + VNP + TLNP + LLNE + (TLB * 5) + EUNP + VNP + EUNP + (TLB * 2) + DBFG + TRUB + DBFG + (TLB * 4) + RS}
{DBFG + (TLB * 4) + LBFG + (TLB * 4) + VNP + TLB + TRNP + HNE + (TLB * 5) + VNP + (TLB * 4) + DBFG + (TLB * 4) + RS}
{DBFG + (TLB * 4) + LBFG + (TLB * 4) + VNP + (TLB * 3) + TRNP + TLNP + (TLB * 3) + VNP + (TLB * 4) + DBFG + (TLB * 4) + RS}
{DBFG + (TLB * 4) + LBFG + (TLB * 4) + VNP + (TLB * 5) + TRNP + LLNE + TLB + VNP + (TLB * 4) + DBFG + (TLB * 4) + RS}
{DBFG + LBBG + (TLB * 4) + TLLB + LBFG + (TLB * 2) + ELNP + VNP + ELNP + (TLB * 5) + RUNE + TRNP + VNP + (TLB * 3) + DBFG + TRLB + DBFG + (TLB * 4) + RS}
 {DBFG + TRUB + (TLB * 4) + LBBG + TLLB + LBFG + (TLB * 4) + (TLB * 4) + (TLB * 4) + DBFG + TRLB + RS + DBFG + (TLB * 4) + TLUB + RS}
   {DBFG + TRUB + (TLB * 5) + LBBG + TLLB + LBFG + (TLB * 6) + DBFG + TRLB + RS + DBFG + (TLB * 5) + TLUB + RS}
     {DBFG + TRUB + (TLB * 14) + TLUB + RS}
       {DBFG + (HHHUB * 12) + RS}"""


import math
ADISC_CONFIG_wind = {
    "vrb_to_notvrb_speci": False,
    "notvrb_to_vrb_speci": False,
    "gust_ws_diff_min": 10,
    "min_ws_for_gust_rule": 15,
    "gust_change_criteria": 10,
    "ws_change_criteria": 10,
    "min_ws_for_wd_rule": 10,
    "wd_change_criteria": 60,
    "only_deterioration_gust_change": True,
    "only_deterioration_ws_change": False
    }
ADISC_CONFIG_vis = {
    "vis_thresholds": [5000, 1600, 1500, 800],
    "only_deterioration_vis": False
    }
ADISC_CONFIG_wx = {
    "speci_weather": ["TS", "FC", "DZ", "RA", "SN", "GR", "FZRA", "FZDZ", "RASN", "SNRA", "BLSA", "DUSA", "BLDU", "DRDU", "BLSN", "DRSN", "SQ", "FZFG"],
    "check_intensity_change": True,
    "intensity_levels": {
        "ltomh_weather": ["TS", "GR", "FZRA", "FZDZ", "SNRA", "RASN", "DZ", "RA", "SN"],
        "lmtoh_weather": ["FC", "SS"],
        "htolm_weather": ["FC", "SS"],
        "mhtol_weather": ["TS", "GR", "FZRA", "FZDZ", "SNRA", "RASN", "DZ", "RA", "SN"],
        },
    "only_deterioration_wx": False
    }
ADISC_CONFIG_cld = {
    "cld_thresholds": [100, 200, 300, 400, 500, 1000, 1500, 2000, 3000],
    "only_deterioration_cld": False
    }
def distinction_wind(prev_wd, prev_ws, prev_gust, curr_wd, curr_ws, curr_gust, conf):
    is_speci = False
    is_caution = False
    reason = ""
    caution = ""
    is_prev_vrb = (prev_wd == "VRB")
    is_curr_vrb = (curr_wd == "VRB")
    not_prev_vrb = (prev_wd != "VRB")
    not_curr_vrb = (curr_wd != "VRB")    
    if is_prev_vrb and not_curr_vrb:
        if conf["vrb_to_notvrb_speci"]:
            is_speci = True
            reason = "The wind direction changed from VRB to not VRB\n風向がVRBではなくなりました\n"
            caution += ""
    if not_prev_vrb and is_curr_vrb:
        if conf["notvrb_to_vrb_speci"]:
            is_speci = True
            reason += "The wind direction changed to VRB froom not VRB\n風向がVRBになりました\n"
            caution += ""
    diff_curg_curws = abs(curr_gust - curr_ws)
    diff_preg_prews = abs(prev_gust - prev_ws)
    if diff_curg_curws < conf["gust_ws_diff_min"] and curr_gust != 0:
        is_caution = True
        criteria = conf["gust_ws_diff_min"]
        reason += ""
        caution += f"the difference between current wind speed and gust is less than {criteria}KT\n注意: 変化後の平均風速とガストの差が{criteria}KT未満です\nThere may be errors in the execution results, so correct them and run again.\n実行結果に誤りがある可能性があるので、訂正後再実行してください\n"
    if diff_preg_prews < conf["gust_ws_diff_min"] and prev_gust != 0:
        is_caution = True
        criteria = conf["gust_ws_diff_min"]
        reason += ""
        caution += f"the difference between previous wind speed and gust is less than {criteria}KT\n注意: 変化前の平均風速とガストの差が{criteria}KT未満です\nThere may be errors in the execution results, so correct them and run again.\n実行結果に誤りがある可能性があるので、訂正後再実行してください\n"
    if curr_ws >= conf["min_ws_for_gust_rule"]:
        preg = prev_gust if prev_gust else 0
        curg = curr_gust if curr_gust else 0
        if preg == 0 and curg > 0:
            is_speci = True
            reason += f"Gust began: {curg}KT\nガスト発生: {curg}KT\n"
            caution += ""
        diff_gust_val = curg - preg
        criteria = conf["gust_change_criteria"]
        if conf["only_deterioration_gust_change"]:
            if preg != 0 and curg != 0 and diff_gust_val >= criteria:
                is_speci = True
                reason += f"Gust increased by {diff_gust_val}KT (criteria: {criteria}KT or more)\nガスト増加{diff_gust_val}KT (基準; {criteria}KT以上)\n"
                caution += ""
        else:
            if preg != 0 and curg != 0 and abs(diff_gust_val) >= criteria:
                is_speci = True
                reason += f"Gust changed by {abs(diff_gust_val)}KT (criteria: {criteria}KT or more)\nガスト変化{abs(diff_gust_val)}KT (基準: {criteria}KT以上)\n"
                caution += ""
    diff_ws_val = curr_ws - prev_ws
    criteria = conf["ws_change_criteria"]
    if conf["only_deterioration_ws_change"]:
        if diff_ws_val >= criteria:
            is_speci = True
            reason += f"wind speed increased by {diff_ws_val}KT(criteria: {criteria}KT)\n風速増加{diff_ws_val}KT (基準: {criteria}KT)\n"
            caution += ""
    else:
        if abs(diff_ws_val) >= criteria:
            is_speci = True
            reason += f"wind speed changed by {abs(diff_ws_val)}KT (criteria: {criteria}KT or more)\n風速変化{abs(diff_ws_val)}KT (基準: {criteria}KT以上)\n"
            caution += ""
    if prev_ws >= conf["min_ws_for_wd_rule"] or curr_ws >= conf ["min_ws_for_wd_rule"]:
        if curr_wd == "VRB" or prev_wd == "VRB":
            pass
        else:
            diff_wd = abs(curr_wd - prev_wd)
            if diff_wd >180:
                diff_wd = 360 - diff_wd
            if diff_wd >= conf["wd_change_criteria"]:
                is_speci = True
                criteria_ws = conf["min_ws_for_wd_rule"]
                criteria_wd = conf["wd_change_criteria"]
                reason += f"wind direction shifted by {diff_wd} degrees (criteria: {criteria_wd} degrees or more (if the wind speed before or after the change is {criteria_ws}KT or more))\n風向変化{diff_wd}度 （基準: {criteria_wd}度以上（変化前または変化後の風速が{criteria_ws}KT以上の場合）)\n"
                caution += ""
    return is_caution, is_speci, reason, caution
def distinction_vis(prev_vis, curr_vis, conf):
    is_speci = False
    is_caution = False
    reason = ""
    caution = ""
    thresholds = sorted(conf["vis_thresholds"], reverse=True)
    for t in thresholds:
        if prev_vis >= t > curr_vis:
            is_speci = True
            reason += f"visibility decreased below {t}m\n視程が{t}mを下回りました\n"
            caution += ""
        elif prev_vis < t <=curr_vis:
            if not conf["only_deterioration_vis"]:
                is_speci = True
                reason += f"visibility increased above {t}m\n視程が{t}mを上回りました\n"
                caution += ""
    return is_caution, is_speci, reason, caution
def distinction_wx(prev_wx, curr_wx, conf):
    is_speci = False
    is_caution = False
    reason = ""
    caution = ""
    def get_int_val(wx):
        if wx == "": return 0
        if "+" in wx: return 3
        if "-" in wx: return 1
        else: return 2
    p_wx = prev_wx.replace("+", "").replace("-", "")
    c_wx = curr_wx.replace("+", "").replace("-", "")
    p_int = get_int_val(prev_wx)
    c_int = get_int_val(curr_wx)
    if p_wx != c_wx:
        if p_wx == "" and c_wx in conf["speci_weather"]:
            is_speci = True
            reason += f"{curr_wx} began\n{curr_wx}が発現しました\n"
            caution += ""
        elif p_wx in conf["speci_weather"] and c_wx =="":
            is_speci = True
            reason += f"{prev_wx} ended\n{prev_wx}が終了しました\n"
            caution += ""
        elif p_wx in conf["speci_weather"] or c_wx in conf ["speci weather"]:
            is_speci = True
            is_caution = True
            reason += f"{prev_wx} changed to {curr_wx}\n現在天気が{prev_wx}から{curr_wx}へ変化しました\n"
            caution += f"check again by yourself whether this change meets the SPECI criteria of your observatory\nこの天気変化があなたの観測所の特別観測基準に該当するか、改めてご自分でご確認ください\n"
    elif p_wx == c_wx and p_wx != "" and conf["check_intensity_change"]:
        if p_int != c_int:
            is_deterioration = (c_int > p_int)
            meet_criteria = False
            if p_wx in conf["intensity_levels"]["ltomh_weather"]:     
                if (p_int == 1 and c_int >= 2):
                    meet_criteria = True
            if p_wx in conf["intensity_levels"]["lmtoh_weather"]:
                if (p_int <= 2 and c_int == 3):
                    meet_criteria = True
            if p_wx in conf["intensity_levels"]["htolm_weather"]:
                if (p_int == 3 and c_int <= 2):
                    meet_criteria = True
            if p_wx in conf["intensity_levels"]["mhtol_weather"]:
                if (p_int >= 2 and c_int == 1):
                    meet_criteria = True
            if meet_criteria:
                is_speci = True
                reason += f"{prev_wx} changed to {curr_wx}\n現在天気が{prev_wx}から{curr_wx}へ変化しました\n"
                caution += ""
    return is_caution, is_speci, reason, caution
def distinction_cld(prev_ceil, curr_ceil, conf):
    is_speci = False
    is_caution = False
    reason = ""
    caution = ""
    if prev_ceil == "" and curr_ceil != "":
        is_speci = True
        reason += f"ceiling appeared\nシーリングが発現しました"
        caution += ""
    elif prev_veil != "" and curr_ceil == "":
        if not conf["only_deterioration_cld"]:
            is_speci = True
            reason += f"ceiling disappeared\nシーリングが終了しました\n"
            caution += ""
    else:
        thresholds = sorted(conf["cld_thresholds"], reverse = True)
        for t in thresholds:
            if prev_ceil >= t > curr_ceil:
                is_speci = True
                reason += f"ceiling decreased below {t}ft\nシーリングが{t}ftを下回りました\n"
                caution += ""
            elif prev_ceil < t <= curr_ceil:
                if not conf["only_deterioration_cld"]:
                    is_speci = True
                    reason += f"ceiling increased above {t}ft\nシーリングが{t}ftを上回りました\n"
                    caution += ""
    return is_caution, is_speci, reason, caution                

#PREVIOUS OBSERVATION VALUE
previous_wind_direction = 20
previous_wind_speed = 10
previous_gust = 0
previous_vis = 6000
previous_weather1 = "RA"
previous_weather2 = "BR"
previous_weather3 = "-TS"
previous_weather4 = ""
previous_weather5 = ""
previous_ceil = ""

#CURRENT OBSERVATION VALUE
current_wind_direction = "VRB"
current_wind_speed = 15
current_gust = 25
current_vis = 400
current_weather1 = "-RA"
current_weather2 = "BR"
current_weather3 = ""
current_weather4 = ""
current_weather5 = ""
current_ceil = 2000


wind_caution, wind_speci, wind_msg, wind_cau = distinction_wind(
    previous_wind_direction,
    previous_wind_speed,
    previous_gust,
    current_wind_direction,
    current_wind_speed,
    current_gust,
    ADISC_CONFIG_wind
)
vis_caution, vis_speci, vis_msg, vis_cau = distinction_vis(
    previous_vis,
    current_vis,
    ADISC_CONFIG_vis
)
wx_caution1, wx_speci1, wx_msg1, wx_cau1 = distinction_wx(
    previous_weather1,
    current_weather1,
    ADISC_CONFIG_wx
)
wx_caution2, wx_speci2, wx_msg2, wx_cau2 = distinction_wx(
    previous_weather2,
    current_weather2,
    ADISC_CONFIG_wx
)
wx_caution3, wx_speci3, wx_msg3, wx_cau3 = distinction_wx(
    previous_weather3,
    current_weather3,
    ADISC_CONFIG_wx
)
wx_caution4, wx_speci4, wx_msg4, wx_cau4 = distinction_wx(
    previous_weather4,
    current_weather4,
    ADISC_CONFIG_wx
)
wx_caution5, wx_speci5, wx_msg5, wx_cau5 = distinction_wx(
    previous_weather5,
    current_weather5,
    ADISC_CONFIG_wx
)
cld_caution, cld_speci, cld_msg, cld_cau = distinction_cld(
    previous_ceil,
    current_ceil,
    ADISC_CONFIG_cld
)
final_speci = wind_speci or vis_speci or wx_speci1 or wx_speci2 or wx_speci3 or wx_speci4 or wx_speci5 or cld_speci
final_caution = wind_caution or vis_caution or wx_caution1 or wx_caution2 or wx_caution3 or wx_caution4 or wx_caution5 or cld_caution
final_msg = wind_msg + vis_msg + wx_msg1 + wx_msg2 + wx_msg3 + wx_msg4 + wx_msg5 + cld_msg
final_cau = wind_cau + vis_cau + wx_cau1 + wx_cau2 + wx_cau3 + wx_cau4 + wx_cau5 + cld_cau
if final_caution:
    print(f"CAUTION: {final_cau}\n")
if final_speci:
    print(f"Send SPECI\n特別観測を送信してください\n{final_msg}")
else:
    print("SPECI is unnecessary\n特別観測は不要です\n")

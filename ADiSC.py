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
        caution += f"CAUTION: the difference between current wind speed and gust is less than {criteria}KT\n注意: 変化後の平均風速とガストの差が{criteria}KT未満です\nThere may be errors in the execution results, so correct them and run again.\n実行結果に誤りがある可能性があるので、訂正後再実行してください\n"
    if diff_preg_prews < conf["gust_ws_diff_min"] and prev_gust != 0:
        is_caution = True
        criteria = conf["gust_ws_diff_min"]
        reason += ""
        caution += f"CAUTION: the difference between previous wind speed and gust is less than {criteria}KT\n注意: 変化前の平均風速とガストの差が{criteria}KT未満です\nThere may be errors in the execution results, so correct them and run again.\n実行結果に誤りがある可能性があるので、訂正後再実行してください\n"
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
            if diff_gust_val >= criteria:
                is_speci = True
                reason += f"Gust increased by {diff_gust_val}KT (criteria: {criteria}KT or more)\nガスト増加{diff_gust_val}KT (基準; {criteria}KT以上)"
                caution += ""
        else:
            if abs(diff_gust_val) >= criteria:
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


previous_wind_direction = 20
previous_wind_speed = 10
previous_gust = 12
previous_vis = 4000
current_wind_direction = "VRB"
current_wind_speed = 3
current_gust = 0
current_vis = 5000

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
final_speci = wind_speci or vis_speci
final_caution = wind_caution or vis_caution
final_msg = wind_msg + vis_msg
final_cau = wind_cau + vis_cau
if final_caution:
    print(f"CAUTION: {final_cau}\n")
if final_speci:
    print(f"Send SPECI\n特別観測を送信してください\n{final_msg}")
else:
    print("SPECI is unnecessary\n特別観測は不要です\n")

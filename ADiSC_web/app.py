from flask import Flask, render_template, request
from ADiSC import distinction_vis, ADISC_CONFIG_vis
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            p_vis = int(request.form["prev_vis"])
            c_vis = int(request.form["curr_vis"])
            _, is_speci, reason, _=distinction_vis(p_vis, c_vis, ADISC_CONFIG_vis)
            if is_speci:
                result = f"【SPECI】{reason}"
            else:
                result = "SPECI不要"
        except Exception as e:
            result = f"error: {e}"
    return render_template("index.html", result=result)
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import re
import socket

app = Flask(__name__)
app.secret_key = 'programmation_reseau'

def is_valid_ip_or_domain(dest):
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", dest):
        return True
    if re.match(r"^(?!\-)([a-zA-Z0-9\-]{1,63}(?<!\-)\.)+[a-zA-Z]{2,}$", dest):
        return True
    return False

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dest = request.form.get("dest")
        direction = request.form.get("direction")
        action = request.form.get("action")
        protocol = request.form.get("protocol") or None
        port = request.form.get("port") or None
        port_end = request.form.get("port_end") or None

        if not dest or not direction or not action:
            flash("Tous les champs obligatoires doivent être remplis.", "error")
            return redirect(url_for("index"))

        if not is_valid_ip_or_domain(dest):
            flash("Adresse IP ou nom de domaine invalide.", "error")
            return redirect(url_for("index"))

        if protocol and protocol.lower() not in ("tcp", "udp", "icmp", ""):
            flash("Protocole invalide. Choisissez tcp, udp, icmp ou laissez vide.", "error")
            return redirect(url_for("index"))

        try:
            dest_ip = socket.gethostbyname(dest)
        except socket.gaierror:
            flash("Impossible de résoudre le domaine.", "error")
            return redirect(url_for("index"))

        for act in ["ACCEPT", "DROP"]:
            try:
                del_cmd = [
                    "iptables", "-D", direction.upper(),
                    "-s", get_local_ip(),
                    "-d", dest_ip,
                ]
                if protocol:
                    del_cmd += ["-p", protocol]
                if port and protocol and protocol.lower() in ("tcp", "udp"):
                    if port_end:
                        del_cmd += ["--dport", f"{port}:{port_end}"]
                    else:
                        del_cmd += ["--dport", port]
                del_cmd += ["-j", act]
                subprocess.run(del_cmd, stderr=subprocess.DEVNULL)
            except Exception:
                pass

        cmd = [
            "iptables", "-I", direction.upper(),
            "-s", get_local_ip(),
            "-d", dest_ip,
        ]

        if protocol:
            cmd += ["-p", protocol]

        if port and protocol and protocol.lower() in ("tcp", "udp"):
            if port_end:
                cmd += ["--dport", f"{port}:{port_end}"]
            else:
                cmd += ["--dport", port]

        cmd += ["-j", action.upper()]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                flash(f"Commande exécutée : {' '.join(cmd)}", "success")
            else:
                flash(f"Erreur iptables : {result.stderr}", "error")
        except Exception as e:
            flash(f"Erreur système : {str(e)}", "error")

        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/rules")
def rules():
    try:
        result = subprocess.run(["iptables", "-L", "-n", "-v", "--line-numbers"], capture_output=True, text=True)
        rules = result.stdout.splitlines()
    except Exception as e:
        rules = [f"Erreur : {str(e)}"]
    return render_template("rules.html", rules=rules)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

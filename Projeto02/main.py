
import os
from flask import Flask, render_template, request
from data_weapons import WEAPONS, NOMES, IMAGENS, ARMAS_PROX
from mapas_estrategias import MAPAS, ESTRATEGIAS_LISTA
from economia_utils import (
    carregar_ultimo_loadout, salvar_loadout, sugestao_compra,
    escolher_estrategia_contextual, calcular_planejamento_prox_round,
)

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "loadouts_registro.json")

@app.route("/", methods=["GET","POST"])
def index():
    resultado = None
    ultimo_loadout = carregar_ultimo_loadout(DATA_FILE)
    if request.method == "POST":
        dinheiro_raw = request.form.get("dinheiro","0")
        lado = request.form.get("lado","TR")
        estilo = request.form.get("estilo","rifler")
        loss_raw = request.form.get("loss_bonus","")
        enemy_raw = request.form.get("enemy_has_ak","nao")
        team_raw = request.form.get("team_min","")
        defuse_raw = request.form.get("priorizar_defuse","off")
        mapa = request.form.get("mapa","mirage")
        arma_prox = request.form.get("arma_prox","") or None

        try:
            dinheiro = int(dinheiro_raw)
            if dinheiro < 0:
                dinheiro = 0
        except ValueError:
            dinheiro = 0

        try:
            loss = int(loss_raw) if loss_raw != "" else None
        except ValueError:
            loss = None

        enemy = (enemy_raw == "sim")

        try:
            team_min = int(team_raw) if team_raw != "" else None
        except ValueError:
            team_min = None

        priorizar_defuse = (defuse_raw == "on")

        itens_cod, restante, estrategia = sugestao_compra(
            dinheiro, lado, estilo, loss, enemy, team_min,
            loadout_items=ultimo_loadout, priorizar_defuse=priorizar_defuse,
        )
        estrategia_mapa = escolher_estrategia_contextual(mapa, lado, itens_cod, estilo)
        prox_round = None
        if arma_prox:
            prox_round = calcular_planejamento_prox_round(dinheiro, loss, arma_prox)

        resultado = {
            "dinheiro": dinheiro,
            "lado": lado,
            "estilo": estilo,
            "mapa": mapa,
            "loss_bonus": loss,
            "enemy_has_ak": enemy,
            "team_min": team_min,
            "itens": [NOMES[i] for i in itens_cod],
            "restante": restante,
            "estrategia": estrategia,
            "estrategia_mapa": estrategia_mapa,
            "imagens": [IMAGENS[i] for i in itens_cod if i in IMAGENS],
            "usando_loadout": bool(ultimo_loadout),
            "priorizar_defuse": priorizar_defuse,
            "prox_round": prox_round,
        }

    armas_prox_lista = [{"cod": c, "nome": NOMES[c], "preco": WEAPONS[c]} for c in ARMAS_PROX]
    return render_template("index.html", resultado=resultado, mapas=MAPAS, armas_prox=armas_prox_lista)

@app.route("/loadout", methods=["GET","POST"])
def loadout():
    resultado = None
    if request.method == "POST":
        sel_tr = request.form.getlist("itens_tr")
        sel_ct = request.form.getlist("itens_ct")
        selecionados = sel_tr + sel_ct
        salvar_loadout(DATA_FILE, selecionados)
        itens_legiveis = [NOMES[i] for i in selecionados if i in NOMES]
        total = sum(WEAPONS[i] for i in selecionados if i in WEAPONS)
        resultado = {"itens": itens_legiveis, "total": total}

    ultimo = carregar_ultimo_loadout(DATA_FILE)
    ultimo_legivel = [NOMES[i] for i in ultimo] if ultimo else None

    categorias_tr = {
        "Pistolas TR": ["p250","tec9","cz75","dual_berettas","deagle","r8"],
        "Rifles TR": ["galil","ak47","sg553","ssg08","awp","g3sg1"],
        "SMGs / Pesadas TR": [
            "mac10","mp7","mp5sd","ump45","p90","bizon",
            "nova","sawedoff","xm1014","m249","negev",
        ],
        "Utilitários TR": ["kevlar","kevlar_helmet","zeus"],
    }

    categorias_ct = {
        "Pistolas CT": ["p250","five_seven","cz75","dual_berettas","deagle","r8"],
        "Rifles CT": ["famas","m4a4","m4a1s","aug","ssg08","awp","scar20"],
        "SMGs / Pesadas CT": [
            "mp9","mp7","mp5sd","ump45","p90","bizon",
            "nova","mag7","xm1014","m249","negev",
        ],
        "Utilitários CT": ["kevlar","kevlar_helmet","zeus","defuse"],
    }

    return render_template(
        "loadout.html",
        categorias_tr=categorias_tr,
        categorias_ct=categorias_ct,
        nomes=NOMES,
        precos=WEAPONS,
        imagens=IMAGENS,
        resultado=resultado,
        ultimo_loadout=ultimo_legivel,
    )

@app.route("/estrategias")
def estrategias():
    return render_template("estrategias.html", mapas=MAPAS)

@app.route("/estrategias/<mapa_slug>")
def estrategias_detalhe(mapa_slug):
    if mapa_slug not in MAPAS:
        mapa_slug = "mirage"
    nome_mapa = MAPAS[mapa_slug]
    dados = ESTRATEGIAS_LISTA.get(mapa_slug, {"TR": [], "CT": []})
    return render_template(
        "estrategias_detalhe.html",
        mapa_slug=mapa_slug,
        nome_mapa=nome_mapa,
        tr_list=dados.get("TR", []),
        ct_list=dados.get("CT", []),
    )

@app.route("/quem-somos")
def quem_somos():
    return render_template("quem_somos.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    status = None
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        assunto = request.form.get("assunto")
        mensagem = request.form.get("mensagem")
        status = "Mensagem enviada com sucesso! (Simulação para o projeto da faculdade.)"
    return render_template("contato.html", status=status)

if __name__ == "__main__":
    app.run(debug=True)

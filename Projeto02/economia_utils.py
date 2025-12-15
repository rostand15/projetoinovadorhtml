
import json, random
from data_weapons import WEAPONS, NOMES, GRANADAS, FORCE_PISTOL_POOL
from mapas_estrategias import ESTRATEGIA_CONTEXTUAL

def carregar_ultimo_loadout(data_file):
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("ultimo")
    except Exception:
        return None

def salvar_loadout(data_file, selecionados):
    data = {"ultimo": selecionados}
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def escolher_pistola_forcada(restante, loadout_items):
    pool = [x for x in FORCE_PISTOL_POOL if (not loadout_items or x in loadout_items)]
    if not pool:
        pool = FORCE_PISTOL_POOL[:]
    pool = [x for x in pool if WEAPONS[x] <= restante]
    if not pool:
        return None
    return random.choice(pool)

def escolher_estrategia_contextual(mapa_slug, lado, itens_cod, estilo):
    mapa_slug = mapa_slug or "mirage"
    if mapa_slug not in ESTRATEGIA_CONTEXTUAL:
        mapa_slug = "mirage"

    tipo = "rifle"
    if estilo == "eco":
        tipo = "force"
    else:
        if "awp" in itens_cod:
            tipo = "awp"
        else:
            rifles = {"ak47","m4a4","m4a1s","sg553","aug","g3sg1","scar20","ssg08"}
            if not any(r in itens_cod for r in rifles):
                tipo = "force"

    return ESTRATEGIA_CONTEXTUAL[mapa_slug][lado].get(tipo, "")

def sugestao_compra(
    dinheiro, lado, estilo, loss_bonus=None,
    enemy_has_ak=False, team_min=None,
    loadout_items=None, priorizar_defuse=False,
):
    sugestao = []
    restante = dinheiro
    gasto = 0
    estrategia_msgs = []

    allowed = set(loadout_items) if loadout_items else set(WEAPONS.keys())

    def disponivel(item):
        if item in GRANADAS:
            return item in WEAPONS
        return item in allowed and item in WEAPONS

    armas_maiores = {
        "mac10","mp9","mp7","mp5sd","ump45","p90","bizon",
        "nova","sawedoff","mag7","xm1014",
        "galil","famas","ak47","m4a4","m4a1s",
        "sg553","aug","ssg08","awp","g3sg1","scar20",
        "m249","negev",
    }

    force_mode = False
    cap_2000 = False

    if team_min is not None and team_min < 2000:
        force_mode = True
        estrategia_msgs.append("Time com jogador abaixo de $2000: recomendado forçar.")

    if (not force_mode) and loss_bonus == 2 and dinheiro < 3000:
        cap_2000 = True
        estrategia_msgs.append("Loss bonus 2 e menos de $3000: semi-buy até $2000.")

    if enemy_has_ak and lado == "CT":
        estrategia_msgs.append("TR de AK: capacete não é prioridade, foque em arma e utilidade.")

    def tenta(item):
        nonlocal restante, gasto
        if not disponivel(item):
            return False
        preco = WEAPONS[item]
        if cap_2000 and (gasto + preco > 2000):
            return False
        if restante >= preco:
            restante -= preco
            gasto += preco
            sugestao.append(item)
            return True
        return False

    is_force_round = force_mode or estilo == "eco"

    if is_force_round:
        pistola = escolher_pistola_forcada(restante, loadout_items)
        if pistola:
            tenta(pistola)
    else:
        if estilo == "rifler":
            if lado == "TR":
                if not tenta("ak47"):
                    tenta("galil")
            else:
                if not tenta("m4a4"):
                    if not tenta("m4a1s"):
                        tenta("famas")
        elif estilo == "awper":
            if not tenta("awp"):
                if lado == "TR":
                    if not tenta("ak47"):
                        tenta("galil")
                else:
                    if not tenta("m4a4"):
                        if not tenta("m4a1s"):
                            tenta("famas")

        if lado == "CT" and priorizar_defuse:
            tenta("defuse")

        comprou_maior = any(i in armas_maiores for i in sugestao)
        if comprou_maior:
            if enemy_has_ak and lado == "CT":
                tenta("kevlar")
            else:
                if not tenta("kevlar_helmet"):
                    tenta("kevlar")

    if restante >= 200:
        for g in ["smoke","flash","he","molotov","incendiary"]:
            tenta(g)

    estrategia_texto = " ".join(estrategia_msgs) if estrategia_msgs else         "Compra baseada em arma principal, economia e loadout salvo."

    return sugestao, restante, estrategia_texto

def calcular_planejamento_prox_round(dinheiro, loss_bonus, arma_cod):
    if arma_cod not in WEAPONS:
        return None
    preco = WEAPONS[arma_cod]
    income_win = 3250
    income_lose = None
    if loss_bonus is not None:
        if loss_bonus <= 0:
            streak = 1
        elif loss_bonus >= 5:
            streak = 5
        else:
            streak = loss_bonus + 1
        income_lose = 1400 + 500 * (streak - 1)

    def bound(x):
        if x is None:
            return None
        return max(0, min(dinheiro, x))

    sw = dinheiro + income_win - preco
    sl = None
    if income_lose is not None:
        sl = dinheiro + income_lose - preco

    max_win = bound(sw)
    max_lose = bound(sl) if sl is not None else None
    if sl is not None:
        safe_raw = min(sw, sl)
    else:
        safe_raw = sw
    max_safe = bound(safe_raw)

    garante_win = (dinheiro + income_win) >= preco
    garante_lose = (income_lose is not None) and ((dinheiro + income_lose) >= preco)
    pode_garantir = garante_win and (garante_lose if income_lose is not None else True)

    from data_weapons import NOMES
    return {
        "cod": arma_cod,
        "nome": NOMES.get(arma_cod, arma_cod),
        "preco": preco,
        "income_win": income_win,
        "income_lose": income_lose,
        "max_gastar_win": max_win,
        "max_gastar_lose": max_lose,
        "max_gastar_seguro": max_safe,
        "garante_win": garante_win,
        "garante_lose": garante_lose,
        "pode_garantir": pode_garantir,
    }

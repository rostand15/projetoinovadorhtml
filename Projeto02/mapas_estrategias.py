
MAPAS = {
    "mirage": "Mirage",
    "inferno": "Inferno",
    "nuke": "Nuke",
    "vertigo": "Vertigo",
    "anubis": "Anubis",
    "dust2": "Dust2",
}

ESTRATEGIAS_LISTA = {m: {"TR": [], "CT": []} for m in MAPAS}

ESTRATEGIA_CONTEXTUAL = {
    "mirage": {
        "TR": {
            "force": "Force TR Mirage: explosão curta no B; smoke janela do L e flash over, pistol rush rápido para punir rotações lentas.",
            "rifle": "Rifle TR Mirage: domínio mid (smoke janela + top con) e split A via con + ramp/palace.",
            "awp": "AWP TR Mirage: pick janela ou palácio; jogar em torno do primeiro pick e executar no bomb enfraquecido."
        },
        "CT": {
            "force": "Force CT Mirage: stack B ou avanço dupla na rampa A para punir rush TR.",
            "rifle": "Rifle CT Mirage: AWP janela + suporte con; crossfire no A entre CT/jungle.",
            "awp": "AWP CT Mirage: dominar janela ou rampa A com apoio de flash do suporte."
        },
    },

    "inferno": {
        "TR": {
            "force": "Force TR Inferno: rush banana com HE carro; se pegar espaço, explode B com smoke CT/Coffin.",
            "rifle": "Rifle TR Inferno: controle banana + avanço na varanda para split A.",
            "awp": "AWP TR Inferno: pick meio; entrar varanda/base dependendo do pick inicial."
        },
        "CT": {
            "force": "Force CT Inferno: stack A com bait pit; tentar ganhar tempo e pegar armas.",
            "rifle": "Rifle CT Inferno: disputa banana com HE/flash inicial, recuo para crossfire B.",
            "awp": "AWP CT Inferno: AWP no meio mirando avanço TR ou banana com suporte flash."
        }
    },

    "nuke": {
        "TR": {
            "force": "Force TR Nuke: explosão Hut + porta com smokes rápidas; tentar plantar rápido no A.",
            "rifle": "Rifle TR Nuke: smokes outside (wall) e split Lower via secret.",
            "awp": "AWP TR Nuke: pick outside (garage) para abrir rota secret."
        },
        "CT": {
            "force": "Force CT Nuke: stack A hut/rafters ou avanço dupla Lobby.",
            "rifle": "Rifle CT Nuke: AWP outside + rifler secret; rotação forte para B.",
            "awp": "AWP CT Nuke: jogar outside da garage ou mirando porta para controlar rush."
        }
    },

    "vertigo": {
        "TR": {
            "force": "Force TR Vertigo: explosão rampa A com smokes frontais e avanço rápido para punir CT recuado.",
            "rifle": "Rifle TR Vertigo: domínio rampa até metade + exec A com smokes CT/Elevator.",
            "awp": "AWP TR Vertigo: pick meio ou rampa alta; jogar em torno do pick e finalizar no bomb fraco."
        },
        "CT": {
            "force": "Force CT Vertigo: avanço rampa A com HE; tentar pegar vantagem cedo.",
            "rifle": "Rifle CT Vertigo: manter rampa contestada com Molo/HE e recuar para setup de retake.",
            "awp": "AWP CT Vertigo: ângulo profundo na rampa A com suporte flash curta."
        }
    },

    "anubis": {
        "TR": {
            "force": "Force TR Anubis: explosão B pelo corredor com smoke deep site.",
            "rifle": "Rifle TR Anubis: controle Mid com smoke janela e split A via con.",
            "awp": "AWP TR Anubis: pick mid e domínio do espaço para abrir caminho ao A."
        },
        "CT": {
            "force": "Force CT Anubis: avanço dupla mid para pegar controle inicial.",
            "rifle": "Rifle CT Anubis: controle mid + jogador avançado no con.",
            "awp": "AWP CT Anubis: AWP na ponte mid ou mirando entrada do B long."
        }
    },

    "dust2": {
        "TR": {
            "force": "Force TR Dust2: domínio Long com flashes altas e smoke corner.",
            "rifle": "Rifle TR Dust2: controle mid + split B (mid to B + túnel).",
            "awp": "AWP TR Dust2: pick meio (longo alcance) e decidir conforme pick inicial."
        },
        "CT": {
            "force": "Force CT Dust2: stack B ou avanço pelo long com popflash.",
            "rifle": "Rifle CT Dust2: AWP meio controlando avanço TR e crossfire A.",
            "awp": "AWP CT Dust2: meio da base mirando T spawn, ou long recuado com suporte."
        }
    }
}

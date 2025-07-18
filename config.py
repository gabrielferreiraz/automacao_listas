
# config.py

CONSULTORES = [
    "Eduardo Fujiyama", "Raphael Lucas", "Karen Landgraf", "Felipe Teles",
    "Jéssica Spinola", "Flavia Pereira", "Lucas Roques", "Ritiele Sandrin",
    "Jônatas Santos", "Polyana Dittmar", "Rafael Lima",
    "Renata Dessbesell", "Bruno Seabra", "Edson Alves", "Jonas Maidana",
    "Kássio Gomes", "Guilherme Melo"
]

EQUIPES = {
    "Equipe Flávio": [
        "Eduardo Fujiyama", "Guilherme Melo", "Karen Landgraf", 
        "Polyana Dittmar", "Rafael Lima", "Ritiele Sandrin"
    ],
    "Equipe Camila": [
        "Renata Dessbesell", "Jonas Maidana", "Flavia Pereira", 
        "Kássio Gomes", "Felipe Teles"
    ],
    "Equipe Fernando": [
        "Jônatas Santos", "Edson Alves", "Jéssica Spinola", 
        "Raphael Lucas", "Lucas Roques", "Bruno Seabra"
    ]
}

# Inverte o mapeamento para facilitar a busca por consultor
CONSULTOR_PARA_EQUIPE = {}
for equipe, consultores_lista in EQUIPES.items():
    for consultor in consultores_lista:
        CONSULTOR_PARA_EQUIPE[consultor] = equipe

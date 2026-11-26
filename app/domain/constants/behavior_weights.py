from typing import Final

from app.domain.enums.behavior_type import BehaviorType

# Relevância de cada comportamento na reação do cliente (1 = sinal fraco,
# 5 = sinal muito forte). Define qual comportamento domina a mensagem e quanto
# os demais contribuem.
# - Ofensa e tentativa de manipulação ferem benevolência e integridade
#   (Mayer; Davis; Schoorman, 1995), e o negativo pesa mais que o positivo
#   (Baumeister et al., 2001; Slovic, 1993).
# - Escuta ativa é o sinal positivo mais forte (Weger et al., 2014).
# - Repetição e perguntas fora do tema são erros típicos de entrevistadores
#   iniciantes (Bano et al., 2019).
# - Contradizer crenças da persona tende a gerar reação defensiva; pesa como
#   um erro de condução, não como agressão.
BEHAVIOR_WEIGHTS: Final = {
    BehaviorType.OFFENSIVE_COMMENT: 5,
    BehaviorType.JAILBREAK_ATTEMPT: 4,
    BehaviorType.INVASIVE_QUESTION: 3,
    BehaviorType.ACTIVE_LISTENING: 3,
    BehaviorType.VIABLE_SOLUTION: 3,
    BehaviorType.REPETITIVE_QUESTION: 2,
    BehaviorType.OFF_TOPIC_QUESTION: 2,
    BehaviorType.BELIEF_CHALLENGE: 2,
    BehaviorType.RELEVANT_QUESTION: 2,
    BehaviorType.CONFUSING_QUESTION: 1,
    BehaviorType.FRIENDLINESS: 1,
}

# Teto da contribuição de um comportamento secundário: ele conta
# SECONDARY_FACTOR x (peso dele / peso do dominante) do seu valor.
SECONDARY_FACTOR: Final = 0.5

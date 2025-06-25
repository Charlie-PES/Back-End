from typing import Dict, Any

# Exemplo de assinatura, pode ser ajustada conforme schemas reais
def calcular_compatibilidade(adotante: Dict[str, Any], pet: Dict[str, Any]) -> int:
    """
    Calcula a pontuação de compatibilidade entre um adotante e um pet com base na tabela fornecida.
    adotante: dicionário com dados do adotante
    pet: dicionário com dados do pet
    Retorna a pontuação total (int).
    """
    pontos = 0

    # Espécie
    if pet.get('species') == adotante.get('desired_species'):
        pontos += 20
    else:
        pontos -= 20

    # Porte
    if pet.get('size') == adotante.get('desired_size'):
        pontos += 10
    else:
        pontos -= 10

    # Sexo
    if pet.get('sex') == adotante.get('desired_sex'):
        pontos += 5
    else:
        pontos -= 5

    # Saúde - necessidades especiais ou tratamento contínuo
    if pet.get('special_needs'):
        if adotante.get('accepts_special_needs'):
            pontos += 10
        else:
            return float('-inf')  # Fator impeditivo
    else:
        if adotante.get('accepts_special_needs'):
            pontos += 5
        else:
            pontos += 10

    # Saúde - doença crônica ou incurável
    if pet.get('chronic_disease'):
        if adotante.get('accepts_chronic_disease'):
            pontos += 10
        else:
            return float('-inf')  # Fator impeditivo
    else:
        if adotante.get('accepts_chronic_disease'):
            pontos += 5
        else:
            pontos += 10

    # Socialização - convivência com outros animais
    if pet.get('good_with_others'):
        if adotante.get('has_other_pets'):
            pontos += 10
        else:
            pontos += 5
    else:
        if adotante.get('has_other_pets'):
            return float('-inf')  # Fator impeditivo
        else:
            pontos += 10

    # Cuidados constantes
    if pet.get('needs_constant_care'):
        if adotante.get('has_time'):
            pontos += 10
        else:
            return float('-inf')  # Fator impeditivo
    else:
        if adotante.get('has_time'):
            pontos += 5
        else:
            pontos += 10

    return pontos 
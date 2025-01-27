# PROGRAMADOR AGRO
# Laura Luísa Martins Teixeira
# Código para simular o controle de temperatura em uma câmara fria que armazena produtos sensíveis
# A linguagem de programção escolhida foi Python 

# Para baixar a biblioteca utilizadas: 
# Digitar no terminal: "pip install matplotlib"
# Digitar no terminal: "pip install matplotlib"

import matplotlib.pyplot as plt
import math

temperatura_inicial = 10
taxa_resfriamento = 0.8
taxa_aquecimento = 1.5
faixa_temperatura = [0, 15]
atraso_efeito = 5  # Constante de tempo para o atraso linear

def simular_ciclo_com_atraso(exponencial=False):
    #Simula a variação da temperatura com atraso linear ou exponencial.
    temperatura = temperatura_inicial
    tempo_total = 0
    motor_ligado = True  # Começa com o motor ligado
    tempo_atraso = 0
    estado_anterior_motor = motor_ligado
    atingiu_limite_inferior = False
    tempo_para_atingir_0 = None

    temperaturas = [temperatura]
    tempos = [tempo_total]
    estados_motor = ["Ligado"]

    print("\nSimulação de ciclo completo com atraso linear:" if not exponencial else "\nSimulação de ciclo completo com atraso exponencial:")

    while tempo_total < 50:  # Simula por 50 minutos
        # Verifica se a temperatura está fora da faixa segura
        if temperatura <= faixa_temperatura[0]:
            motor_ligado = False  # Desliga o motor
            if not atingiu_limite_inferior:
                print(f"Temperatura atingiu 0°C no minuto {tempo_total}.")
                atingiu_limite_inferior = True
                tempo_para_atingir_0 = tempo_total
        elif temperatura >= faixa_temperatura[1]:
            motor_ligado = True  # Liga o motor

        # Aplica o atraso
        if motor_ligado != estado_anterior_motor:
            tempo_atraso = atraso_efeito
            estado_anterior_motor = motor_ligado

        # Aplica a taxa de variação de temperatura
        if tempo_atraso > 0:
            # Durante o atraso, a temperatura varia com base no estado anterior do motor
            if estado_anterior_motor:
                if exponencial:
                    temperatura -= taxa_resfriamento * (1 - math.exp(-tempo_atraso / atraso_efeito))
                else:
                    temperatura -= taxa_resfriamento
            else:
                if exponencial:
                    temperatura += taxa_aquecimento * (1 - math.exp(-tempo_atraso / atraso_efeito))
                else:
                    temperatura += taxa_aquecimento
            tempo_atraso -= 1
        else:
            # Após o atraso, a temperatura varia com base no estado atual do motor
            if motor_ligado:
                temperatura -= taxa_resfriamento
            else:
                temperatura += taxa_aquecimento

        # Mantém a temperatura dentro da faixa segura
        temperatura = max(faixa_temperatura[0], min(faixa_temperatura[1], temperatura))

        # Atualiza o tempo
        tempo_total += 1

        # Registra os dados
        temperaturas.append(temperatura)
        tempos.append(tempo_total)
        estados_motor.append("Ligado" if motor_ligado else "Desligado")

        # Exibe o status
        print(f"Minuto {tempo_total}: Temperatura = {temperatura:.2f}°C, Motor = {estados_motor[-1]}")

    return temperaturas, tempos, estados_motor, tempo_para_atingir_0

def simular_ciclo_sem_atraso():
    #Simula a variação da temperatura sem atraso.
    temperatura = temperatura_inicial
    tempo_total = 0
    motor_ligado = True  # Começa com o motor ligado
    tempo_para_atingir_0 = None

    temperaturas = [temperatura]
    tempos = [tempo_total]
    estados_motor = ["Ligado"]

    print("\nSimulação de ciclo completo sem atraso:")

    while tempo_total < 50:  # Simula por 50 minutos
        # Verifica se a temperatura está fora da faixa segura
        if temperatura <= faixa_temperatura[0]:
            motor_ligado = False  # Desliga o motor
            if tempo_para_atingir_0 is None:
                print(f"Temperatura atingiu 0°C no minuto {tempo_total}.")
                tempo_para_atingir_0 = tempo_total
        elif temperatura >= faixa_temperatura[1]:
            motor_ligado = True  # Liga o motor

        # Aplica a taxa de variação de temperatura
        if motor_ligado:
            temperatura -= taxa_resfriamento
        else:
            temperatura += taxa_aquecimento

        # Mantém a temperatura dentro da faixa segura
        temperatura = max(faixa_temperatura[0], min(faixa_temperatura[1], temperatura))

        # Atualiza o tempo
        tempo_total += 1

        # Registra os dados
        temperaturas.append(temperatura)
        tempos.append(tempo_total)
        estados_motor.append("Ligado" if motor_ligado else "Desligado")

        # Exibe o status
        print(f"Minuto {tempo_total}: Temperatura = {temperatura:.2f}°C, Motor = {estados_motor[-1]}")

    return temperaturas, tempos, estados_motor, tempo_para_atingir_0

def plotar_graficos(tempos_com_atraso, temperaturas_com_atraso, tempos_sem_atraso, temperaturas_sem_atraso, tempos_exponencial, temperaturas_exponencial):
    # Plota gráficos da simulação.
    plt.figure(figsize=(10, 6))

    plt.plot(tempos_com_atraso, temperaturas_com_atraso, label="Com Atraso Linear")
    plt.plot(tempos_sem_atraso, temperaturas_sem_atraso, label="Sem Atraso", linestyle="--")
    plt.plot(tempos_exponencial, temperaturas_exponencial, label="Com Atraso Exponencial", linestyle="-.")
    plt.axhline(y=faixa_temperatura[0], color='r', linestyle='--', label="Limite Inferior (0°C)")
    plt.axhline(y=faixa_temperatura[1], color='g', linestyle='--', label="Limite Superior (15°C)")

    plt.title("Simulação de Controle de Temperatura")
    plt.xlabel("Tempo (minutos)")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.grid()
    plt.show()

# Simulação com atraso linear
temperaturas_com_atraso, tempos_com_atraso, estados_motor_com_atraso, tempo_para_0_com_atraso = simular_ciclo_com_atraso()

# Simulação sem atraso
temperaturas_sem_atraso, tempos_sem_atraso, estados_motor_sem_atraso, tempo_para_0_sem_atraso = simular_ciclo_sem_atraso()

# Simulação com atraso exponencial (passo bônus)
temperaturas_exponencial, tempos_exponencial, estados_motor_exponencial, tempo_para_0_exponencial = simular_ciclo_com_atraso(exponencial=True)

# Exibe os tempos para atingir 0°C
print(f"\nTempo para atingir 0°C:")
print(f"Com atraso linear: {tempo_para_0_com_atraso} minutos")
print(f"Sem atraso: {tempo_para_0_sem_atraso} minutos")
print(f"Com atraso exponencial: {tempo_para_0_exponencial} minutos")

# Gráficos
plotar_graficos(tempos_com_atraso, temperaturas_com_atraso, tempos_sem_atraso, temperaturas_sem_atraso, tempos_exponencial, temperaturas_exponencial)
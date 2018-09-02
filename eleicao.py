import pandas as pd
import numpy as np

#Abrindo o arquivo
df = pd.read_csv('eleicao.csv', sep = ';')

#Declarando os valores obtidos previamente 
total_vagas = 29
quociente_eleitoral = 12684

#Artifício para maninupular a coluna 'Partido/Coligação'
df['Coligação'] = df['Partido/Coligação']
df['Coligação'] = df.Coligação.str.split('-')

#Função para definir as coligações de cada candidato
def sep_coligacao(df):
    if (len(df['Coligação']) == 2):
        return df['Coligação'][1]
    else:
        return df['Coligação'][0]
    
df['Coligação'] = df.apply(sep_coligacao, axis = 1)

#Calculando os votos obtidos por cada coligação
votos_coligacao = df.groupby(['Coligação'])['Votos'].sum()

#Obtendo o quociente partidário
quociente_partidario = votos_coligacao//quociente_eleitoral

#Obtendo as vagas residuais
vagas_residuais = total_vagas - quociente_partidario.sum()

#Função auxiliar para limpar um Pandas.Series
def limpa_lista(pd):
    pd_clear = pd.copy()
    for i in range(pd.count()):
        pd_clear[i] = 0
    return pd_clear

#Vagas residuais recebidas por certa coligação
vagasResiduais_coligacao = limpa_lista(votos_coligacao)

#Função para calcular a média de uma coligação para definir quem ganhará as vagas residuais
def calculo_media(votos_coligacao, quociente_P, vagas_recebidas):
    partido_media = votos_coligacao/(quociente_P + vagas_recebidas + 1)
    return partido_media

#Distribui as vagas residuais calculando a média Mi a cada interação e atribuindo a quem obteve a maior média
def distribuir_vagasResiduais(numero_vagasResiduais, votos_coligacao, quociente_P, vagas_recebidas):
    for i in range(0,numero_vagasResiduais):
        media_Atual = calculo_media(votos_coligacao, quociente_P, vagas_recebidas)
        vagas_recebidas[media_Atual.nlargest(1).index] += 1
    return vagas_recebidas

#Aplica os resultados da distribuição das vagas residuais
vagasResiduais_coligacao = distribuir_vagasResiduais(vagas_residuais, votos_coligacao, quociente_partidario, vagasResiduais_coligacao)

#Atualiza as vagas de cada coligação (vagas do quociente partidário + vagas residuais)
numero_vagas = vagasResiduais_coligacao + quociente_partidario

#laço de repetição para identificar os candidatos aptos a assumirem a vaga
for i in range(0,17):
    for j in range(0, numero_vagas[i]):
        df.loc[df['Coligação'] == numero_vagas.index[i]]

#exportando os dados para .tsv
df.to_csv('eleicao.csv')
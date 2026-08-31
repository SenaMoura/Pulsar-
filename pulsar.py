import trimesh
import numpy as np 


divs = 80  
num_p = divs + 1

x = np.linspace(-5, 5, num_p)
y = np.linspace(-5, 5, num_p)


massa_pulsar = 4.5     
raio_deformacao = 0.8  
rotacao_pulsar = 0.6   

def deformar_ponto(px, py):
    distancia = np.sqrt(px**2 + py**2)
    
    z = -massa_pulsar / (1 + (distancia / raio_deformacao)**2)

    angulo = rotacao_pulsar / (distancia + 0.2)
    
    novo_x = px * np.cos(angulo) - py * np.sin(angulo)
    novo_y = px * np.sin(angulo) + py * np.cos(angulo)
    
    return [novo_x, novo_y, z]

linhas = []


for pos_y in y:
    pontos_linha = []
    for pos_x in x:
        pontos_linha.append(deformar_ponto(pos_x, pos_y))
    
    for k in range(len(pontos_linha) - 1):
        linhas.append([pontos_linha[k], pontos_linha[k + 1]])

for pos_x in x:
    pontos_linha = []
    for pos_y in y:
        pontos_linha.append(deformar_ponto(pos_x, pos_y))
    
    for k in range(len(pontos_linha) - 1):
        linhas.append([pontos_linha[k], pontos_linha[k + 1]])





grade = trimesh.load_path(linhas)
grade.colors = np.tile([100, 150, 255, 180], (len(grade.entities), 1))
raio_estrela = 0.3

s = trimesh.creation.icosphere(radius=0.5, subdivisions=3)
s.visual.face_colors = [255, 255, 255, 255]

z_fundo_real = -massa_pulsar
s.apply_translation([0, 0, -2.5])

comprimento_jato = 3.5
raio_jato = 0.05
jato = trimesh.creation.cylinder(radius=raio_jato, height=comprimento_jato)
jato.visual.face_colors = [0, 200, 255, 255]

angulo_inclinacao = np.radians(25.0)
vetor_direcao = np.array([np.sin(angulo_inclinacao), 0, np.cos(angulo_inclinacao)])

matriz_alinhamento = trimesh.geometry.align_vectors([0, 0, 1], vetor_direcao)
jato.apply_transform(matriz_alinhamento)

jato.apply_translation([0, 0, z_fundo_real])

scene = trimesh.Scene([grade, s])
scene.show(
    background=[5, 5, 15]
)
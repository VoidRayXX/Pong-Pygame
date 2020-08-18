import pygame,sys
from random import choice

#funciones
def dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola):
	ventana.fill(bg)
	pygame.draw.rect(ventana,gris_claro,jugador)
	pygame.draw.rect(ventana,gris_claro,oponente)
	pygame.draw.ellipse(ventana,gris_claro,bola)
	pygame.draw.aaline(ventana,gris_claro,(Ancho/2,0),(Ancho/2, Largo))
	pygame.display.update()

def animacionBola(bola,jugador,oponente,Ancho,Largo):
	global bola_velX,bola_velY
	bola.x += bola_velX
	bola.y += bola_velY

	if bola.left <= 0 or bola.right >= Ancho:
		reiniciarBola(bola,Ancho,Largo)
	if bola.top <= 0 or bola.bottom >= Largo:
		bola_velY *= -1

	if bola.colliderect(jugador) or bola.colliderect(oponente):
		bola_velX *= -1

def animacionJugador(jugador,jugador_vel,Largo):
	jugador.y += jugador_vel
	if jugador.top <= 0:
		jugador.top = 0
	if jugador.bottom >= Largo:
		jugador.bottom = Largo

def oponenteIA(oponente,bola,oponente_vel,Largo):
	if oponente.top < bola.y:
		oponente.top += oponente_vel
	if oponente.bottom > bola.y:
		oponente.bottom -= oponente_vel
	if oponente.top <= 0:
		oponente.top = 0
	if oponente.bottom >= Largo:
		oponente.bottom = Largo

def reiniciarBola(bola,Ancho,Largo):
	global bola_velX,bola_velY
	bola.center = (Ancho/2,Largo/2)
	bola_velX *= choice((1,-1))
	bola_velY *= choice((1,-1))

#variables constantes
pygame.init()
Ancho = 1280
Largo = 960
ventana = pygame.display.set_mode((Ancho,Largo))
pygame.display.set_caption("Pong")
reloj = pygame.time.Clock()
fps = 60

#colores
bg = pygame.Color("gray12")
gris_claro = (200,200,200)
#gris_claro = (255,255,255) esto es por si decido cambiar el color de los objetos a blanco

#dibujos del juego
bola = pygame.Rect(Ancho/2 - 15, Largo/2 - 15,30,30)
jugador = pygame.Rect(Ancho - 20, Largo/2 - 70,10,140)
oponente = pygame.Rect(10, Largo/2 - 70,10,140)

#variables de las velocidades
bola_velX = 7 * choice((1,-1))
bola_velY = 7 * choice((1,-1))
jugador_vel = 0
oponente_vel = 7

#ciclo principal
while True:
	reloj.tick(fps)
	
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_DOWN:
				jugador_vel += 7
			if evento.key == pygame.K_UP:
				jugador_vel -= 7

		if evento.type == pygame.KEYUP:
			if evento.key == pygame.K_DOWN:
				jugador_vel -= 7
			if evento.key == pygame.K_UP:
				jugador_vel += 7


	animacionBola(bola,jugador,oponente,Ancho,Largo)
	animacionJugador(jugador,jugador_vel,Largo)
	oponenteIA(oponente,bola,oponente_vel,Largo)


	dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola)

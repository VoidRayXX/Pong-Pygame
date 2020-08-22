import pygame,sys
from random import choice

#funciones
def dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco):
	ventana.fill(bg)
	pygame.draw.rect(ventana,gris_claro,jugador)
	pygame.draw.rect(ventana,gris_claro,oponente)
	pygame.draw.ellipse(ventana,gris_claro,bola)
	pygame.draw.aaline(ventana,gris_claro,(Ancho/2,0),(Ancho/2, Largo))
	scoreOp = fuente.render(str(victoriasOponente),True,blanco)
	ventana.blit(scoreOp,(600,470))
	scoreJug = fuente.render(str(victoriasJugador),True,blanco)
	pos_vicJugX = 660
	if victoriasJugador >= 10:
		pos_vicJugX = 645
	ventana.blit(scoreJug,(pos_vicJugX,470))
	pygame.display.update()


def animacionBola(bola,jugador,oponente,Ancho,Largo,ventana,fuente,blanco,bloqueo,rebote,score):
	global bola_velX,bola_velY,victoriasJugador,victoriasOponente
	bola.x += bola_velX
	bola.y += bola_velY

	if bola.left <= 0:
		victoriasJugador += 1
		pygame.mixer.Sound.play(score)
		reiniciarBola(bola,Ancho,Largo)
		delay(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco,fuente_timer)
		return False
	
	if bola.right >= Ancho:
		victoriasOponente += 1
		pygame.mixer.Sound.play(score)
		reiniciarBola(bola,Ancho,Largo)
		delay(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco,fuente_timer)
		return False
	
	if bola.top <= 0 or bola.bottom >= Largo:
		bola_velY *= -1
		pygame.mixer.Sound.play(rebote)

	if bola.colliderect(jugador) and bola_velX > 0:
		pygame.mixer.Sound.play(bloqueo)
		if abs(bola.right - jugador.left) < 10:
			bola_velX *= -1
		elif abs(bola.bottom - jugador.top) < 10 and bola_velY > 0:
			bola_velY *= -1
		elif abs(bola.top - jugador.bottom) < 10 and bola_velY < 0:
			bola_velY *= -1
		else:
			bola_velX *= -1
			bola_velY *= -1

	if bola.colliderect(oponente) and bola_velX < 0:
		pygame.mixer.Sound.play(bloqueo)
		if abs(bola.left - oponente.right) < 10:
			bola_velX *= -1
		elif abs(bola.bottom - oponente.top) < 10 and bola_velY > 0:
			bola_velY *= -1
		elif abs(bola.top - oponente.bottom) < 10 and bola_velY < 0:
			bola_velY *= -1
		else:
			bola_velX *= -1
			bola_velY *= -1

	return True

def animacionJugador(jugador,jugador_vel,Largo):
	jugador.y += jugador_vel
	if jugador.top <= 0:
		jugador.top = 0
	if jugador.bottom >= Largo:
		jugador.bottom = Largo

def oponenteIA(oponente,bola,oponente_vel,Largo,Ancho):
	#esto es para que la IA no se mueva todo el tiempo
	if abs(bola.x - oponente.x) <= (Ancho/2):
		if oponente.y < bola.y:
			oponente.y += oponente_vel
		elif oponente.y > bola.y:
			oponente.y -= oponente_vel
	#esto es para evitar que el oponente salga de la ventana
	if oponente.top <= 0:
		oponente.top = 0
	if oponente.bottom >= Largo:
		oponente.bottom = Largo

def reiniciarBola(bola,Ancho,Largo):
	global bola_velX,bola_velY
	bola.center = (Ancho/2,Largo/2)
	bola_velX *= choice((1,-1))
	bola_velY *= choice((1,-1))

def delay(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco,fuente_timer):
	tiempo_inicial = pygame.time.get_ticks()
	Flag1 = True
	Flag2 = True
	Flag3 = True
	jugador,oponente,jugador_vel = foto()
	
	while True:
		tiempoActual = pygame.time.get_ticks()
		
		#le permite al usuario cerrar el programa mientras el juego se prepara para reiniciar
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		if tiempoActual - tiempo_inicial >= 3000:
			break
		
		if tiempoActual - tiempo_inicial <= 700 and Flag1:
			dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco)
			timer = fuente_timer.render("3",True,blanco)
			ventana.blit(timer,(Ancho/2 - timer.get_width()/2,250))
			Flag1 = False
			
		if 700 < tiempoActual - tiempo_inicial <= 1400 and Flag2:
			dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco)
			timer = fuente_timer.render("2",True,blanco)
			ventana.blit(timer,(Ancho/2 - timer.get_width()/2,250))
			Flag2 = False

		if 1400 < tiempoActual - tiempo_inicial <= 2100 and Flag3:
			dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco)
			timer = fuente_timer.render("1",True,blanco)
			ventana.blit(timer,(Ancho/2 - timer.get_width()/2,250))
			Flag3 = False
		
		pygame.display.update()
	reestablecerPosiciones()
	
def reestablecerPosiciones():
	global jugador,oponente,jugador_vel
	jugador = pygame.Rect(Ancho - 40, Largo/2 - 70,10,140)
	oponente = pygame.Rect(40, Largo/2 - 70,10,140)
	jugador_vel = 0

def foto():
	jug = pygame.Rect(Ancho - 40, Largo/2 - 70,10,140)
	opo = pygame.Rect(40, Largo/2 - 70,10,140)
	jug_vel = 0
	return jug,opo,jug_vel
	

#variables constantes
pygame.mixer.pre_init(44100,-16,2,512)
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
blanco = (255,255,255) 

#dibujos del juego
bola = pygame.Rect(Ancho/2 - 15, Largo/2 - 15,30,30)
jugador = pygame.Rect(Ancho - 40, Largo/2 - 70,10,140)
oponente = pygame.Rect(40, Largo/2 - 70,10,140)

#variables de las velocidades
bola_velX = 7 * choice((1,-1))
bola_velY = 7 * choice((1,-1))
jugador_vel = 0
oponente_vel = 15
aceleracion = 0.01

#variables de los puntajes/scores
victoriasJugador = 0
victoriasOponente = 0
fuente = pygame.font.Font("freesansbold.ttf",32)
fuente_timer = pygame.font.Font("freesansbold.ttf",100)
start = True

#sonidos del juego
bloqueo = pygame.mixer.Sound("hit.ogg")
rebote = pygame.mixer.Sound("wall.ogg")
score = pygame.mixer.Sound("score.ogg")
bg_music = pygame.mixer.music.load("reloaded-installer-10.mp3")
pygame.mixer.music.play(-1)

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
				jugador_vel = 0
			if evento.key == pygame.K_UP:
				jugador_vel = 0

	#Animaciones del juego
	if start:
		delay(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco,fuente_timer)
		start = False
	acelerar = animacionBola(bola,jugador,oponente,Ancho,Largo,ventana,fuente,blanco,bloqueo,rebote,score)
	animacionJugador(jugador,jugador_vel,Largo)
	oponenteIA(oponente,bola,oponente_vel,Largo,Ancho)
	dibujar(ventana,gris_claro,bg,Ancho,Largo,jugador,oponente,bola,victoriasJugador,victoriasOponente,fuente,blanco)
	
	#permite acelerar la bola hasta cierto límite
	if acelerar and abs(bola_velX) <= 15:
		if bola_velX > 0:
			bola_velX += aceleracion
		else:
			bola_velX -= aceleracion
		if bola_velY > 0:
			bola_velY += aceleracion
		else:
			bola_velY -= aceleracion
	
	#reinicia las velocidades de la bola a sus valores originales cuando se empieza una nueva ronda
	if not acelerar:
		bola_velX = 7 * choice((1,-1))
		bola_velY = 7 * choice((1,-1))
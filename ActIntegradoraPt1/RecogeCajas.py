import pygame
from pygame.locals import *
import random

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Recoge Cajas")

class pilaDeCajas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill((139, 69, 19))  # Color marrón para la caja
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.cantidad = random.randint(5, 15)  # Cantidad de cajas en la pila
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render(str(self.cantidad), True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self):
        self.text = self.font.render(str(self.cantidad), True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.rect.center)    
        window.blit(self.image, self.rect)
        window.blit(self.text, self.text_rect)  
    def recoger_caja(self):
        if self.cantidad <= 0:
            return False
        
class Recolector(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 128, 255))  # Color azul para el recolector
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.cajas_recogidas = 0
        self.capacidad_maxima = 5

    def update(self):
        window.blit(self.image, self.rect)

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def recoger(self, pila):
        if pygame.sprite.collide_rect(self, pila):
            if pila.cantidad > 0 and self.cajas_recogidas < self.capacidad_maxima:
                pila.cantidad -= 1
                self.cajas_recogidas += 1
                
class dropZone(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Color verde para la zona de entrega
        self.rect = self.image.get_rect()
        self.x, self.y = 700, 500
        self.rect.topleft = (self.x, self.y)

    def update(self):
        window.blit(self.image, self.rect)
        
    def entregar_cajas(self, recolector):
        if pygame.sprite.collide_rect(self, recolector):
            recolector.cajas_recogidas = 0
    
def main():
    clock = pygame.time.Clock()
    recolectores = []
    for _ in range(5):
        recolector = Recolector(random.randint(50, 700), random.randint(50, 500))
        recolectores.append(recolector)
    pilas = [pilaDeCajas(random.randint(50, 700), random.randint(50, 500)) for _ in range(random.randint(5, 15))  ]
    zona_entrega = dropZone()
    distancias = []
    for pila in pilas:
        distancia = ((zona_entrega.rect.x - pila.rect.x) ** 2 + (zona_entrega.rect.y - pila.rect.y) ** 2) ** 0.5
        distancias.append((distancia, pila))

    all_sprites = pygame.sprite.Group()
    for recolector in recolectores:
        all_sprites.add(recolector)
    for pila in pilas:
        all_sprites.add(pila)
    
    all_sprites.add(zona_entrega)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        if not pilas and all(recolector.cajas_recogidas == 0 for recolector in recolectores):
            print("¡Todas las cajas han sido recogidas!")
            running = False
        # Movimiento automatico del recolector
        for recolector in recolectores:
            if recolector.cajas_recogidas < recolector.capacidad_maxima and pilas:
                for distancia, pila in sorted(distancias, key=lambda x: x[0]):
                    if pila.cantidad > 0:
                        if recolector.rect.x < pila.rect.x:
                            recolector.mover(2, 0)
                        elif recolector.rect.x > pila.rect.x:
                            recolector.mover(-2, 0)
                        if recolector.rect.y < pila.rect.y:
                            recolector.mover(0, 2)
                        elif recolector.rect.y > pila.rect.y:
                            recolector.mover(0, -2)
                        break
            else:
                if recolector.rect.x < zona_entrega.rect.x:
                    recolector.mover(2, 0)
                elif recolector.rect.x > zona_entrega.rect.x:
                    recolector.mover(-2, 0)
                if recolector.rect.y < zona_entrega.rect.y:
                    recolector.mover(0, 2)
                elif recolector.rect.y > zona_entrega.rect.y:
                    recolector.mover(0, -2)
        # Eliminar pilas vacías
        for pila in pilas:
            if pila.cantidad == 0:
                pilas.remove(pila)
                all_sprites.remove(pila)
        
        #colisión y recogida de cajas
        for recolector in recolectores:
            for pila in pilas:
                if pygame.sprite.collide_rect(recolector, pila):
                    recolector.recoger(pila)
        
        #colisión y entrega de cajas
        for recolector in recolectores:
            if pygame.sprite.collide_rect(recolector, zona_entrega):
                zona_entrega.entregar_cajas(recolector)
        # Actualización de la pantalla

        window.fill((0, 0, 0))  # Fondo negro
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
        
if __name__ == "__main__":
    pygame.init()
    main()
import pygame
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CBullet import CBullet
from src.ecs.components.CEnemy import CEnemy
from src.create.prefab_creator import PrefabCreator

def system_bullet_enemy_collision(entities: dict, prefab_creator: PrefabCreator):
    bullets = []
    enemies = []

    for eid, comps in entities.items():
        if CPosition in comps and CSurface in comps:
            if CBullet in comps:
                bullets.append((eid, comps[CPosition], comps[CSurface]))
            elif CEnemy in comps:
                enemies.append((eid, comps[CPosition], comps[CSurface]))

    to_remove = set()

    for bullet_id, bullet_pos, bullet_surf in bullets:
        bullet_rect = bullet_surf.area.copy()
        bullet_rect.topleft = (bullet_pos.x, bullet_pos.y)

        for enemy_id, enemy_pos, enemy_surf in enemies:
            enemy_rect = enemy_surf.area.copy()
            enemy_rect.topleft = (enemy_pos.x, enemy_pos.y)

            if bullet_rect.colliderect(enemy_rect):
                to_remove.add(bullet_id)
                to_remove.add(enemy_id)

                collision_point = {
                    "x": enemy_pos.x + enemy_rect.width / 2,
                    "y": enemy_pos.y + enemy_rect.height / 2
                }

                prefab_creator.create_explosion(collision_point)
                print(f"💥 Bullet {bullet_id} hit Enemy {enemy_id}")
                break

    for eid in to_remove:
        del entities[eid]

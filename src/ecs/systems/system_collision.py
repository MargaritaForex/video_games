from src.ecs.components.CPosition import CPosition
from src.ecs.components.CRect import CRect
from src.ecs.components.CHealth import CHealth

def system_collision(world):
    # Get all entities with position and rect components
    entities = world.get_entities_with_components(CPosition, CRect)
    
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            entity1 = entities[i]
            entity2 = entities[j]
            
            pos1 = world.get_component(entity1, CPosition)
            rect1 = world.get_component(entity1, CRect)
            pos2 = world.get_component(entity2, CPosition)
            rect2 = world.get_component(entity2, CRect)
            
            # Check collision
            if (pos1.x < pos2.x + rect2.w and
                pos1.x + rect1.w > pos2.x and
                pos1.y < pos2.y + rect2.h and
                pos1.y + rect1.h > pos2.y):
                
                # Handle collision based on entity types
                health1 = world.get_component(entity1, CHealth)
                health2 = world.get_component(entity2, CHealth)
                
                if health1 and health2:
                    # Both entities can take damage
                    health1.current -= 1
                    health2.current -= 1
                    
                    # Remove entities if health reaches 0
                    if health1.current <= 0:
                        world.entities[entity1] = {}
                    if health2.current <= 0:
                        world.entities[entity2] = {} 
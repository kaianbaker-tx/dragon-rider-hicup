extends Node2D

## How fast the world slides past. Bigger = you feel like you're going faster.
@export var world_speed := 120.0

@onready var sky: ParallaxBackground = $Sky


func _process(delta: float) -> void:
	sky.scroll_offset.x -= world_speed * delta

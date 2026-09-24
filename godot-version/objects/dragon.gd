extends CharacterBody2D

## How fast the dragon flies. Bigger = faster.
@export var speed := 520.0
## How quickly it gets up to speed. Bigger = snappier, smaller = floatier.
@export var grip := 9.0

@onready var sprite: AnimatedSprite2D = $Sprite


func _physics_process(delta: float) -> void:
	var wanted := Vector2.ZERO
	wanted.x = Input.get_axis("ui_left", "ui_right")
	wanted.y = Input.get_axis("ui_up", "ui_down")
	# WASD works too
	if Input.is_action_pressed("move_left"): wanted.x -= 1.0
	if Input.is_action_pressed("move_right"): wanted.x += 1.0
	if Input.is_action_pressed("move_forward"): wanted.y -= 1.0
	if Input.is_action_pressed("move_back"): wanted.y += 1.0
	wanted = wanted.limit_length(1.0)

	velocity = velocity.lerp(wanted * speed, grip * delta)
	move_and_slide()

	# tip the nose up when climbing, down when diving
	rotation = lerp_angle(rotation, velocity.y / speed * 0.35, 8.0 * delta)

	# flap faster when you're pulling up
	sprite.speed_scale = 1.0 + maxf(0.0, -velocity.y / speed) * 1.2

	# don't let him leave the screen
	var edge := get_viewport_rect().size
	position.x = clampf(position.x, 90.0, edge.x - 90.0)
	position.y = clampf(position.y, 80.0, edge.y - 80.0)

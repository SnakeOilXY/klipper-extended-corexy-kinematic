# Sample config

- The basic configuration uses 4 motors. A(was X motor on traditional coreXY config), B(was Y motor on traditional coreXY config), C and C1.
- Motor B and C must have the same <code>position_min</code> and <code>position_max</code>.
- By default, When home Y axis, the fw will use endstop of C and C1(if available) motor. User can set <code>home_y_axis_with_b_rail</code> to <code>True</code> to enable homing Y axis with B motor endstop.

<pre>
[printer]
kinematics: extended_corexy
max_velocity: 500 ; max feedrate 30K
max_accel: 20000
max_accel_to_decel: 20000
max_z_velocity: 10 ; max feedrate 600
max_z_accel: 1000
square_corner_velocity: 5
home_y_axis_with_b_rail : False

[stepper_a]
step_pin: PG4
dir_pin: PC1
enable_pin: !PA0
microsteps: 32
rotation_distance: 40
full_steps_per_rotation:200
endstop_pin:!PG15
position_endstop: 3
position_min: 0
position_max: 250
homing_speed: 100
homing_retract_dist: 10.0

[stepper_b]
step_pin: PF9
dir_pin: PF10
enable_pin: !PG2
microsteps: 32
rotation_distance: 40
full_steps_per_rotation:200
endstop_pin: !PG11
position_endstop: 200
position_min: -15
position_max: 200
homing_speed: 100
homing_retract_dist: 10.0

[stepper_c]
step_pin: PE2
dir_pin: !PE3
enable_pin: !PD4
microsteps: 32
rotation_distance: 40
full_steps_per_rotation:200
endstop_pin: !PG10
position_endstop: 200
position_min: -15
position_max: 200
homing_speed: 100
homing_retract_dist: 10.0

[stepper_c1]
step_pin: PE6
dir_pin: PA14
enable_pin: !PE0
microsteps: 32
rotation_distance: 40
full_steps_per_rotation:200
endstop_pin: !PG9

</pre>
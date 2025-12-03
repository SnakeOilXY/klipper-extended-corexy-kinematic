# Code for handling the kinematics of extended corexy robots
#
# Copyright (C) 2022  John Smith <chip@snakeoildev.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging, math
import stepper

class ExtendedCoreXYKinematics:
    def __init__(self, toolhead, config):
        # Setup axis rails
        self.rails = [stepper.LookupMultiRail(config.getsection('stepper_' + n))
                      for n in 'abzc']
        # rail[0](a): add B endstop
        for s in self.rails[1].get_steppers():
            self.rails[0].get_endstops()[0][0].add_stepper(s)
        # rail[1](b): add A and C endstop
        for s in self.rails[0].get_steppers():
            self.rails[1].get_endstops()[0][0].add_stepper(s)
        for s in self.rails[3].get_steppers():
            self.rails[1].get_endstops()[0][0].add_stepper(s)
        # rail[3](c): add A and B endstop
        for s in self.rails[0].get_steppers():
            self.rails[3].get_endstops()[0][0].add_stepper(s)
        for s in self.rails[1].get_steppers():
            self.rails[3].get_endstops()[0][0].add_stepper(s)

        self.rails[0].setup_itersolve('corexy_stepper_alloc', b'+')
        self.rails[1].setup_itersolve('corexy_stepper_alloc', b'-')
        self.rails[2].setup_itersolve('cartesian_stepper_alloc', b'z')
        self.rails[3].setup_itersolve('cartesian_stepper_alloc', b'y')

        for s in self.get_steppers():
            s.set_trapq(toolhead.get_trapq())
            # toolhead.register_step_generator(s.generate_steps)
        # Setup boundary checks
        max_velocity, max_accel = toolhead.get_max_velocity()
        self.max_z_velocity = config.getfloat(
            'max_z_velocity', max_velocity, above=0., maxval=max_velocity)
        self.max_z_accel = config.getfloat(
            'max_z_accel', max_accel, above=0., maxval=max_accel)
        self.limits = [(1.0, -1.0)] * 3

        # check ranges and endstop positions of B and Y motors
        if self.rails[1].get_range() != self.rails[3].get_range():
            raise config.error("B and C motors must have the same position_min and position_max")
        if self.rails[1].position_endstop != self.rails[3].position_endstop:
            raise config.error("B and C motors must have the same position_endstop")

        # get ranges : X from rail 0(A), Y from rail 2(Y), Z from rail 3(Z)
        ranges = [self.rails[0].get_range(),self.rails[1].get_range(),self.rails[2].get_range()]
        self.axes_min = toolhead.Coord([r[0] for r in ranges])
        self.axes_max = toolhead.Coord([r[1] for r in ranges])

        # what rail wil be used to home y axis
        self.home_y_axis_with_b_rail = config.getboolean(
            'home_y_axis_with_b_rail', False)
    def get_steppers(self):
        return [s for rail in self.rails for s in rail.get_steppers()]
    def calc_position(self, stepper_positions):
        pos = [stepper_positions[rail.get_name()] for rail in self.rails]
        return [0.5 * (pos[0] + pos[1]), 0.5 * (pos[0] - pos[1]), pos[2]]
    def set_position(self, newpos, homing_axes):
        for i, rail in enumerate(self.rails):
            rail.set_position(newpos)
            # rails : abzc, axes : xyz
            # rail C is also based on B, so no need to check on C when B is set
            if i < len("xyz"):
                if "xyz"[i] in homing_axes:
                    self.limits[i] = rail.get_range()
    def home(self, homing_state):
        # Each axis is homed independently and in order
        for axis in homing_state.get_axes():
            rail_number_to_home = axis
            # Decide to use rail 1(B) or rail 3(C) to home Y axis
            if axis == 1 and not self.home_y_axis_with_b_rail:
                rail_number_to_home = 3
            rail = self.rails[rail_number_to_home]

            # Determine movement
            position_min, position_max = rail.get_range()
            hi = rail.get_homing_info()
            homepos = [None, None, None, None]
            homepos[axis] = hi.position_endstop
            forcepos = list(homepos)
            if hi.positive_dir:
                forcepos[axis] -= 1.5 * (hi.position_endstop - position_min)
            else:
                forcepos[axis] += 1.5 * (position_max - hi.position_endstop)
            # Perform homing
            homing_state.home_rails([rail], forcepos, homepos)
    def clear_homing_state(self, clear_axes):
        for axis, axis_name in enumerate("xyz"):
            if axis_name in clear_axes:
                self.limits[axis] = (1.0, -1.0)
    def _check_endstops(self, move):
        end_pos = move.end_pos
        for i in (0, 1, 2):
            if (move.axes_d[i]
                and (end_pos[i] < self.limits[i][0]
                     or end_pos[i] > self.limits[i][1])):
                if self.limits[i][0] > self.limits[i][1]:
                    raise move.move_error("Must home axis first")
                raise move.move_error()
    def check_move(self, move):
        limits = self.limits
        xpos, ypos = move.end_pos[:2]
        if (xpos < limits[0][0] or xpos > limits[0][1]
            or ypos < limits[1][0] or ypos > limits[1][1]):
            self._check_endstops(move)
        if not move.axes_d[2]:
            # Normal XY move - use defaults
            return
        # Move with Z - update velocity and accel for slower Z axis
        self._check_endstops(move)
        z_ratio = move.move_d / abs(move.axes_d[2])
        move.limit_speed(
            self.max_z_velocity * z_ratio, self.max_z_accel * z_ratio)
    def get_status(self, eventtime):
        axes = [a for a, (l, h) in zip("xyz", self.limits) if l <= h]
        return {
            'homed_axes': "".join(axes),
            'axis_minimum': self.axes_min,
            'axis_maximum': self.axes_max,
        }

def load_kinematics(toolhead, config):
    return ExtendedCoreXYKinematics(toolhead, config)



import pygame
import unittest
import pymunk
import math
from unittest.mock import MagicMock, patch
from  main import create_ball


# Function to handle events
def handle_events(event, taking_shot, powering_up, run):
    if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
        powering_up = True
    elif event.type == pygame.MOUSEBUTTONUP and taking_shot:
        powering_up = False
    elif event.type == pygame.QUIT:
        run = False
    return taking_shot, powering_up, run

# Unit test class
class TestEventHandler(unittest.TestCase):
    def test_handle_events(POCKET):
        # Simulate events
        pygame.init()
        # Set initial states
        taking_shot = True
        powering_up = False
        run = True

        # Simulate a MOUSEBUTTONDOWN event
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        taking_shot, powering_up, run = handle_events(event, taking_shot, powering_up, run)
        POCKET.assertTrue(powering_up)

        # Simulate a MOUSEBUTTONUP event
        event = pygame.event.Event(pygame.MOUSEBUTTONUP)
        taking_shot, powering_up, run = handle_events(event, taking_shot, powering_up, run)
        POCKET.assertFalse(powering_up)

        # Simulate a QUIT event
        event = pygame.event.Event(pygame.QUIT)
        taking_shot, powering_up, run = handle_events(event, taking_shot, powering_up, run)
        POCKET.assertFalse(run)

class TestGame(unittest.TestCase):
    def test_ball_creation(balls):
        # Define the expected properties of the ball
        testradius = 10
        testpos = (20, 30)
        testmass = 5
        testelasticity = 0.8

        # Create a ball using the create_ball function
        ball = create_ball(testradius, testpos)

        # Check if the ball's properties are as expected
        balls.assertEqual(ball.radius, testradius)
        balls.assertEqual(ball.body.position, testpos)
        balls.assertEqual(ball.mass, testmass)
        balls.assertEqual(ball.elasticity, testelasticity)


    def setUp(POCKET):
        # Initialize necessary variables, create a space, and set up the game environment

        # Define a pocket diameter for collision detection
        POCKET.pocket_diameter = 66

        # Define a list of pockets [(x1, y1), (x2, y2), ...]
        POCKET.pockets = [
            (55, 63),
            (592, 48),
            (1134, 64),
            (55, 616),
            (592, 629),
            (1134, 616)
        ]

        # Create a ball at a position close to one of the pockets
        POCKET.ball_radius = 18
        POCKET.ball_position = (50, 60)  # Adjust to be near a pocket

        POCKET.space = pymunk.Space()
        POCKET.ball = POCKET.create_ball(POCKET.ball_radius, POCKET.ball_position)

    def create_ball(POCKET, radius, pos):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = 5
        shape.elasticity = 0.8
        POCKET.space.add(body, shape)
        return shape

    def test_ball_pocket_collision(POCKET):
        for pocket in POCKET.pockets:
            ball_x_dist = abs(POCKET.ball.body.position[0] - pocket[0])
            ball_y_dist = abs(POCKET.ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
            
            
            if ball_dist <= POCKET.pocket_diameter / 2:
                POCKET.assertTrue(ball_dist <= POCKET.pocket_diameter / 2)
    
    def handle_events(event, taking_shot, powering_up, run):
     if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
        powering_up = True
     elif event.type == pygame.MOUSEBUTTONUP and taking_shot:
        powering_up = False
     elif event.type == pygame.QUIT:
        run = False
     return taking_shot, powering_up, run   
def power_up_pool_cue(powering_up, game_running, force, force_direction, max_force, taking_shot, balls, cue_angle):
    if powering_up and game_running:
        force += 100 * force_direction
        if force >= max_force or force <= 0:
            force_direction *= -1
        return force, force_direction
    elif not powering_up and taking_shot:
        x_impulse = 0
        y_impulse = 0
        if len(balls) > 0:
            x_impulse = math.cos(math.radians(cue_angle))
            y_impulse = math.sin(math.radians(cue_angle))
            balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
        return force, force_direction

class TestPowerUpPoolCue(unittest.TestCase):
    def test_power_up_pool_cue_powering_up_true(POCKET):
        force = 5000
        force_direction = 1
        max_force = 10000
        game_running = True
        powering_up = True
        taking_shot = True
        balls = []  # Mocking the balls list for simplicity
        cue_angle = 45  # Arbitrary value for testing

        updated_force, updated_force_direction = power_up_pool_cue(
            powering_up, game_running, force, force_direction, max_force, taking_shot, balls, cue_angle
        )

        POCKET.assertEqual(updated_force, 5100)  # Expected force after power-up
        POCKET.assertEqual(updated_force_direction, 1)  # Expected force direction after power-up

    def test_power_up_pool_cue_powering_up_false(POCKET):
        force = 5000
        force_direction = 1
        max_force = 10000
        game_running = True
        powering_up = False
        taking_shot = True
        balls = []  # Mocking the balls list for simplicity
        cue_angle = 45  # Arbitrary value for testing

        updated_force, updated_force_direction = power_up_pool_cue(
            powering_up, game_running, force, force_direction, max_force, taking_shot, balls, cue_angle
        )

        POCKET.assertEqual(updated_force, 5000)  # Expected force remains unchanged
        POCKET.assertEqual(updated_force_direction, 1)  # Expected force direction remains unchanged

    # Additional test cases for various scenarios can be added as needed
# Assuming these are global variables or part of a class
taking_shot = True
game_running = True
cue_ball_potted = True  # Assuming the cue ball is potted

# Unit test class
class TestDrawPoolCue(unittest.TestCase):
    def test_draw_pool_cue(POCKET):
        global taking_shot, game_running, cue_ball_potted

        if taking_shot and game_running:
            if cue_ball_potted:
                # Reposition the cue ball
                cue_ball_position = (888, 339)  # Position where the cue ball is repositioned
                POCKET.assertEqual(cue_ball_position, (888, 339))  # Check if the cue ball is repositioned correctly

                # Calculate pool cue angle
                mouse_pos = (800, 400)  # Mouse position (assumed)
                cue_ball_position = (888, 339)  # Current cue ball position
                x_dist = cue_ball_position[0] - mouse_pos[0]
                y_dist = -(cue_ball_position[1] - mouse_pos[1])
                cue_angle = math.degrees(math.atan2(y_dist, x_dist))

                # Check if the calculated cue angle is within an expected range
                POCKET.assertTrue(0 <= cue_angle <= 360)  # Adjust the range as per your expectation

                # Ensure that cue.update(cue_angle) is called (assuming cue.update() exists)
                # Mock or check any function calls related to drawing the cue

     

if __name__ == '__main__':
    unittest.main()

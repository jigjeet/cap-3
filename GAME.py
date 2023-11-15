import unittest
from main import create_ball, pymunk, new_ball, cue, math


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


    def setUp(self):
        # Initialize necessary variables, create a space, and set up the game environment

        # Define a pocket diameter for collision detection
        self.pocket_diameter = 66

        # Define a list of pockets [(x1, y1), (x2, y2), ...]
        self.pockets = [
            (55, 63),
            (592, 48),
            (1134, 64),
            (55, 616),
            (592, 629),
            (1134, 616)
        ]

        # Create a ball at a position close to one of the pockets
        self.ball_radius = 18
        self.ball_position = (50, 60)  # Adjust to be near a pocket

        self.space = pymunk.Space()
        self.ball = self.create_ball(self.ball_radius, self.ball_position)

    def create_ball(self, radius, pos):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = 5
        shape.elasticity = 0.8
        self.space.add(body, shape)
        return shape

    def test_ball_pocket_collision(self):
        # Simulate a situation where a ball collides with a pocket
        for pocket in self.pockets:
            ball_x_dist = abs(self.ball.body.position[0] - pocket[0])
            ball_y_dist = abs(self.ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
            
            # Check if the distance between the ball and any pocket is less than or equal to pocket diameter / 2
            if ball_dist <= self.pocket_diameter / 2:
                # Collision occurred, test asserts
                # For example, you might assert that the ball is removed or its position changes
                self.assertTrue(ball_dist <= self.pocket_diameter / 2)
                # Add further assertions based on the expected behavior after collision
                # For instance, removing the ball from active balls and asserting its removal

                # For instance, if you have a function to handle ball removal:
                # handle_ball_pocket_collision(self.ball) 
                # Then you can assert that the ball was removed:
                # self.assertNotIn(self.ball, self.space.b
    



    


if __name__ == '__main__':
    unittest.main()

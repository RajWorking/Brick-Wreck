# Brick-Wreck
Terminal based arcade game in Python3 inspired from the old classic brick breaker game.

## Description
The player uses a paddle with a bouncing ball to smash bricks and get a high score before the time runs out.

## Game Ending
The game is over when all bricks (except unbreakable ones) are finished or the time runs out.
You can exit the game voluntarily by pressing 'q'.

A life is lost when all balls on the screen go into the abyss.

## Game Play
'a' : Move Paddle Left  
'd' : Move Paddle Right  
's' : Release Ball from Paddle  
(WARNING: no caps-lock)

Ball deflects upon hitting paddle. More distance from center, more the deflection.
When a ball hits a brick, its strength is reduced.
Balls collide with the 3 walls.
 
## Explosive Bricks:
When a explosive brick is hit, it damages all bricks around it. This may initiate a chain reaction.

## Power Ups
Power ups fall down when a brick is damaged completely. These can be collected by the paddle to activate them.
The powers ups expire after a short while. Bricks damaged by thru-ball and Explosive Bricks do **not** generate powerups.

* Grapes (Multi-ball) - All balls duplicate with sister balls go in opposite direction.
* Strawberry (Ball Grab) - Ball does not simply bounce off paddle, it waits for user to release it by pressing 's'.
* Carrot (Elongate Paddle) - Paddle becomes longer.
* Lemon (Shorten Paddle) - Paddle shrinks in size.
* Bomb (Thru-ball) - Ball completely damages any brick (irrespective of strength) in its way without reflecting from it.
* Clock (Fast Ball) - Game speeds up. Higher Frame Rate.
* Heart (Extra Life) - Yipee!

All power ups are lost when a life is lost.

## Scoring
Your score depends on the time played and bricks broken.
 * More the bricks broken => Higher Score  
 * More Time Played => Less Score 

## Note
This project is built using OOPS principles of classes and objects.

- [x] Abstraction  
- [x] Polymorphism
- [x] Encapsulation
- [x] Inheritance
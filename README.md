# raycasting
Exploring raycasting to create 3d graphics in pygame.

Although the code is still being cleaned up, so far the program works like this:
![raycast](./raycasting.gif)
----

EXPLANATION:
----
Using a 2d image we can send out "rays" from an object in an angle we'll call the players field of vision (FOV). When these rays collide with 2d objects we can represent them as slivers of vertical rectangles with heights and color values based on the distance of the ray (smaller and darker if farther away). These slivers blend together to create the "3d" look.


REPRESENTATION:
----
![show](https://github.com/jacob1st/raycasting/blob/main/representation_of_raycasting.PNG)


Known issues: There is a slight curvature to objects, noticable when you look at them from an angle. They appear this way due to some math I implemented to fix shapes appearing like fishbowls.

Use WASD to move. Press Z to lock/unlock the mouse. While locked, move the mouse to rotate the player.

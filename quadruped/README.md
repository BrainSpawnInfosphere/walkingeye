# Quadraped

A lot of good info comes from:

* [Tote RTD](http://tote.readthedocs.io/en/latest/ik.html)
* [Sheep](http://sheep.art.pl/Robots)

## Quadraped Gaits

1. **Static Gait**: No matter where you are in the process, you are always stable.
Typically used at slow speeds (e.g., creeping).
  * Small robot: you have to keep track center of mass (CM) inside the area
  of support (AoS). The AoS is defined by a polygon on the ground with a robot's
  legs at the vertexes.
  * Large robot: with larger/heavier robots, you need to also track the zero-moment
  point (ZMP). The ZMP is a shifted off the CM (to account for inertia) and
  you need to keep the ZMP inside the AoS.
2. **Dynamic Gait**: Unstable, but you rely on the fact it takes time for the 
robot to fall. These cannot be interrupted like stable gaits and are typically
executed faster than stable gaits (e.g., trot).

**Creep**: one leg moves at a time (stable). An example is shown below for an
optimal moving of the 4 legs.

    Forward    Turn
    1 3        1 2
    4 2        4 3

**Trot**: two legs move at a time (unstable). Due to the instability, a trot
can only be stopped once a step is complete (e.g., all feet on the ground).

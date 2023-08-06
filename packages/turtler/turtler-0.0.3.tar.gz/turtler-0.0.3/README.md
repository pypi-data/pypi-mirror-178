## Introduction

Start your Data Science journey with Turtler. Written to make learning fun!

### Getting Started

Turtler is built on top of [turtle](https://docs.python.org/3/library/turtle.html) but makes drawing easy.

#### Import

`from turtler import Turtler`



#### Initialize

`myTurtler = Turtler()`



#### Move and Draw

```
myTurtler.go(DIRECTIONS)
myTurtler.draw(DIRECTIONS)
```



DIRECTIONS is a string consisting of:-
| Character | Direction |
| --------- | --------- |
| u         | UP        |
| d         | DOWN      |
| l         | LEFT      |
| r         | RIGHT     |

EXAMPLE:-
```
directions = "uldr"
myTurtler.go(directions)
```



#### End Drawing

`myTurtler.done()`


---

### Other Methods

**Set Animation Speed**

`myTurtler.setSpeed(YOUR_SPEED)`

Options:
- fastest
- fast
- normal
- slow
- slowest

**Set Step Size**

`myTurtler.setSpeed(YOUR_SIZE)`

YOUR_SIZE is an int object
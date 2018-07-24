# BuildingGenerator
My bachelor's thesis, a nodegraph-based generator for all kinds of buildings.

![pagoda](https://i.imgur.com/9IfAlzf.png)
![pagoda](https://i.imgur.com/7xmRj0W.jpg)
![pagoda](https://i.imgur.com/8VFXd1g.jpg)


## Warnings

This Blender plugin is for a VERY old version of Blender (2.71) and "features" a bug I never found a solution to:
When loading a .blend file with a "Building" type nodegraph in it, changing anything inside the graph without clicking on "update" first will crash Blender immediately, without any dumps or logs available. This makes debugging especially hard, but I'm fairly certain there's something wrong in the custom update system I've added in order to circumvent the standard, non-performant PyNode update system. I'd love to put some more work into the generator as it seems powerful enough to create basically any procedural model - if I'll ever not be swamped with work for side projects I'll give it a go.


## Installing

Simply download the zip and load it from inside Blender's plugin manager.

# Tasks for future versions

* Generate better documentation than the monolithic readme

* Add ability to set a constant velocity for a shape

* Work out a better way of calculating the margins outside of which a shape is removed.
  Maybe calculate those based on a bounding box of existing shapes when run () is called?
  Can default to the current setup as a minimum, but allow that to increase if shapes are
  placed outside that range initially.

  Or, document set_margins if that's the way to set them.

* Add a color function to set the default color with which shapes are drawn.  This would 
  make it easier for very early drawing assignments.


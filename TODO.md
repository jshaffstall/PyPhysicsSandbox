# Tasks for future versions

* Generate better documentation than the monolithic readme

* Add ability to set a constant velocity for a shape

* Work out a better way of calculating the margins outside of which a shape is removed.
  Maybe calculate those based on a bounding box of existing shapes when run () is called?
  Can default to the current setup as a minimum, but allow that to increase if shapes are
  placed outside that range initially.

  Or, document set_margins if that's the way to set them.

* Screencasts
- volcano example
- misc shape stuff: debug flag, hit method, conveyer belts, paste_on
- large number of shapes example

* Text drawing when combined with paste_on seems wonky.  Actual
  angle of the box the text is drawn in seems okay, must be a translation
  problem between pymunk and pygame.

  Confirmed, drawing at angles of 1, 2, 3, etc produces radical shifts
  in the angle the text is drawn at.

  Seems to be a bug in the angle property introduced during the shift
  to counter clockwise angles.

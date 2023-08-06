CHANGE HISTORY
==============

1.7.0
-----
- Added unicode support for input and output.
- Reworked Screen construction.

  - Added open() and close() methods to Screen.
  - Retired from_windows(), from_curses() and from_blessed() methods.
  - Retired Blessed support.

- Added set_scenes() and draw_next_frame() to allow asynchronous frameworks to
  use Screen.
- Added Plasma renderer and sample code to use it.
- Added background colour support to ColourImageFile.
- Added support for multi-colour rendering using ${c,a,b} syntax.
- Added highlight() method to Screen and Canvas.
- Added UT framework for testing and CI configurations to run the tests.
- Added shadows to Frames.
- Fixed bug in restoring console colours on Exit for Windows.
- Fixed up logic for handling Ctrl keys and documented OS restrictions.
- Fixed refresh timer in play() when handling intensive computational load.
- Added repeat flag to play() to allow termination of the animation instead of
  infinite looping.
- Improved CPU usage for Widgets-based UIs.
- General docs and test tidy up.

1.6.0
-----
- Added `widgets` sub-package, providing a Frame effect for encapsulating a User
  Interface, a Layout to organise the content and the following widgets:

  - Button
  - CheckBox
  - Divider
  - Label
  - ListBox
  - RadioButtons
  - Text
  - TextBox

- Added PopUpDialog for simple alerting in a UI.
- Added `attr` option to Print Effect.
- Added `keys` option to BarChart Renderer.

1.5.0
-----
- Created the ParticleEffect and associated classes.
- Implemented the StarFirework, RingFirework, SerpentFirework, PalmFirework,
  Explosion, DropScreen, ShootScreen and Rain effects.
- Added background colour options to BarChart renderer.
- Added set_title() method to set title for window that owns the Screen.

1.4.2
-----
- Fix for Python 3 support on Linux variants.

1.4.1
-----
- Minor fixes to setup.py to correct packaging meta-data.

1.4.0
-----
- Added Fire renderer and demo.
- Added Mouse support.  This had 2 major impacts:

  1. It meant that blessed support is now completely deprecated as it doesn't
     support mouse input.
  2. All references to processing keys is now deprecated.  You must now use the
     `get_event()` equivalent API instead.

- Added support for dynamic addition/removal of Effects from a Scene, using
  `add_effect()` and `remove_effect()`.
- Converted all effects to use `**kwargs` to pass through to base Effect class
  so that future common frame related features were instantly available.  These
  parameters must now always be specified as keyword arguments as a result.
- Added support for background colours.
- Renamed `getch()` and `putch()` to `get_from()` and `print_at()`.  Old
  functions are still present, but deprecated.
- Fixed up `get_from()` so that it is consistent across all platforms and
  includes all character attributes.

1.3.0
-----
- Added BarChart renderer and demo.
- Added support for extended key codes on Windows and Linux.
- Added support for dynamic paths using keyboard input.  Created interactive
  demo sample to show how this works.
- Split Renderer into StaticRenderer and DynamicRenderer.  Code that used
  Renderer should now use StaticRenderer.
- Added speed option to Print effect.
- Fixed up curses colour detection and Unicode bug in python2 on Windows.

1.2.0
-----
- Added Windows support, complete with `Screen.wrapper()` to handle all
  required screen set up.  The old from_XXX class methods are now deprecated.
- Fixed ColourImageFile to do bare minimum rendering on low colour terminals.
- Added formal palette property to Screen for image conversions.
- Verified Python 3.4 support.

1.1.0
-----
- Added the Julia Set and Cog effects.
- Fixed up off-by-one error in line drawing.
- Added support for screen resizing while playing a scene.
- Added support for Python 3.

1.0.0
-----
- Added Bressenham line drawing algorithm with anti-aliasing.
- Added Random Noise effect.
- Added support for blessed as well as curses - if you want to continue to
  use curses, construct the Screen using the `from_curses()` class method.
- Fixed up some docs errors.

0.4.0
-----
- Added support for 256 colour terminals.
- Moved ${c,a} syntax for inline colouring from Screen to Renderer.
- Created some samples for 256 colour mode and colour images.

0.3.0
-----
- Added support for multi-colour rendering using ${c,a} syntax.
- Added Snow effect.
- Fixed bug when erasing small Sprites.
- Fixed up various documentation niggles.

0.2.0
-----
- Original public release.

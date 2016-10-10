My personal usage of video editors is usually just to convert, resize, trim, and concatenate a bunch of videos. Maybe sometimes adding text. As of writing, there's no good free video editor. To me, writing a Python wrapper on top of ffmpeg seems better than:
- paying money
- fixing Blender
- building vlmc

The result is kind of cool. In general, I like things that work on code instead of GUI. The drawback is obvious: harder to see your work in progress. The benefits are less obvious. None of the video editors I've used have a solid GUI where you're certain what a left click will do. Code is expressed in text, and text is manipulated by the text editor, a mature species of software where you can pretty easily find a specimen where you know exactly what left click will do. You can stick text in a repo and see meaningful diffs, and you can even hit undo and know what will happen. Code is composable.

Why bother writing a wrapper at all? In general, I think anything that has a sufficiently complex specification language should stop inventing its own wheels and write an API in some other well-adopted language. This applies here. Instead of reading the ffmpeg documentation and learning an I-made-this-quick-so-I-could-get-back-to-video-stuff specification language, we get to use Python, a language designed to be a good language that lots of people already know.

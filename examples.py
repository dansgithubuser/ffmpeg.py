# this wont run, but here are some examples

import dansvideoeditor as dve

dve.concat_copy(
    [
        dve.Source('/home/dan/Downloads/bass_1_2.mp4').cut(38, 40),
        dve.Source('/home/dan/Downloads/bass_2_1.mp4').cut(70, 72),
        dve.Source('/home/dan/Downloads/bass_3_1.mp4').cut(40, 42),
        dve.Source('/home/dan/Downloads/bass_4_1.mp4').cut(90, 92),
    ],
    'output1.mov',
)

dve.concat(
    [
        dve.Source('/home/dan/Downloads/bass_1_2.mp4').cut(38, 40),
        dve.Source('/home/dan/Downloads/bass_2_1.mp4').cut(70, 72),
        dve.Source('/home/dan/Downloads/bass_3_1.mp4').cut(40, 42),
        dve.Source('/home/dan/Downloads/bass_4_1.mp4').cut(90, 92),
    ],
    out_path='output2.mov',
)

dve.concat(
    [
        dve.Source('/home/dan/Downloads/bass_1_2.mp4').cut(38, 40),
        dve.Source('/home/dan/Downloads/bass_2_1.mp4').cut(70, 72),
        dve.Source('/home/dan/Downloads/bass_3_1.mp4').cut(40, 42),
        dve.Source('/home/dan/Downloads/bass_4_1.mp4').cut(90, 92),
    ],
    640,
    480,
    'output3.mov',
)

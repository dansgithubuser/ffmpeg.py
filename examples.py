# this wont run, but here are some examples

import dansvideoeditor as dve

import os

def build_ifiles():
    dve.Ifile('b1', '/home/dan/Downloads/bass_1_2.mp4', 38, 40)
    dve.Ifile('b2', '/home/dan/Downloads/bass_2_1.mp4', 70, 72)
    dve.Ifile('b3', '/home/dan/Downloads/bass_3_1.mp4', 40, 42)
    dve.Ifile('b4', '/home/dan/Downloads/bass_4_1.mp4', 90, 92)
    dve.Ifile('a', '/home/dan/Desktop/mess/audio/test16.flac')

if not os.path.exists('output1.mov'):
    build_ifiles()
    dve.concat_copy(
        ['b1', 'b2', 'b3', 'b4'],
        'output1.mov',
    )
    dve.reset()

if not os.path.exists('output2.mov'):
    build_ifiles()
    dve.concat_center(
        ['b1', 'b2', 'b3', 'b4'],
        'output3.mov',
    )
    dve.reset()

if not os.path.exists('output3.mov'):
    build_ifiles()
    dve.concat_center(
        ['b1', 'b2', 'b3', 'b4'],
        640,
        480,
        'output3.mov',
    )
    dve.reset()

if not os.path.exists('output4.mov'):
    build_ifiles()
    dve.Concat('q1', ['b1', 'b2', 'b3', 'b4'])
    dve.Concat('q2', ['b2', 'b3', 'b4', 'b1'])
    dve.Concat('q3', ['b3', 'b4', 'b1', 'b2'])
    dve.Concat('q4', ['b4', 'b1', 'b2', 'b3'])
    dve.Hsplit('h1', 'q1', 'q2')
    dve.Hsplit('h2', 'q3', 'q4')
    dve.Vsplit('v', 'h1', 'h2')
    dve.render('output4.mov', 'v', 'q1')
    dve.reset()

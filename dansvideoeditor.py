import os
import subprocess

TMP_PATH = '.dansvideoeditor-tmp.txt'

class Source:
    def __init__(self, path):
        self.path = path
        self.is_cut = False

    def cut(self, start, end):
        self.cut_start = start
        self.cut_end = end
        self.is_cut = True
        return self

def concat_copy(sources, out_path='output.mov'):
    with open(TMP_PATH, 'w') as f:
        for source in sources:
            f.write(f'file {source.path}\n')
            if source.is_cut:
                f.write(f'inpoint {source.cut_start}\n')
                f.write(f'outpoint {source.cut_end}\n')
    subprocess.run(
        [
            'ffmpeg',
            '-f', 'concat',  # use the concat demuxer
            '-safe', '0',  # allow absolute file paths
            '-i', TMP_PATH,
            '-codec', 'copy',
            out_path,
        ],
        check=True,
    )

def concat(sources, width=None, height=None, out_path='output.mov'):
    # get dims from first source if needed
    if width == None or height == None:
        width, height = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0',
                sources[0].path,
            ],
            check=True,
            capture_output=True,
        ).stdout.decode('utf-8').strip().split(',')
    # inputs
    inputs = []
    for source in sources:
        if source.cut:
            inputs.extend([
                '-ss', str(source.cut_start),
                '-t', str(source.cut_end - source.cut_start),
            ])
        inputs.extend(['-i', str(source.path)])
    # reshape filters
    m = rf'min({width}/iw\,{height}/ih)'  # so that reshaped is as big as possible without clipping
    reshapes = [
        f'[{i}:v:0]'  # video of input i
        f'scale=iw*{m}:ih*{m},'  # scale by m
        f'pad={width}:{height}:({width}-iw*{m})/2:({height}-ih*{m})/2,'  # center
        f'setsar=1'  # force SAR to 1 (is this gonna be an issue?)
        f'[reshaped{i}]'  # name the result
        for i, source in enumerate(sources)
    ]
    # concat filter
    concat = ''.join([
        *[
            f'[reshaped{i}][{i}:a:0]'  # video of reshaped i, audio of input i
            for i in range(len(sources))
        ],
        f'concat={len(sources)}:1:1',  # map n inputs to 1 video and 1 audio stream
        '[v][a]',  # name the result
    ])
    # run
    subprocess.run(
        [
            'ffmpeg',
            *inputs,
            '-filter_complex', ';'.join(reshapes+[concat]),
            '-map', '[v]',  # create the output from final results
            '-map', '[a]',
            out_path,
        ],
        check=True,
    )

import os
import subprocess

TMP_PATH = '.dansvideoeditor-tmp.txt'

def reset():
    _Element._elements = {}

# elements
def _element(name):
    return _Element._elements[name]

def _vlink(name):
    return _element(name).vlink()

def _alink(name):
    return _element(name).alink()

class _Element:
    def __init__(self, name):
        self.name = name
        _Element._elements[name] = self

    def vlink(self, check=False):
        if check: return False
        raise Exception(f"element {self.name} doesn't have a vlink")

    def alink(self, check=False):
        if check: return True
        raise Exception(f"element {self.name} doesn't have an alink")

    _elements = {}

class _VElement(_Element):
    def vlink(self):
        return f'[{self.name}]'

class _VAElement(_Element):
    def vlink(self):
        return f'[{self.name}__v]'

    def alink(self):
        return f'[{self.name}__a]'

# input file
class Ifile(_Element):
    def __init__(self, name, path, start=None, end=None):
        _Element.__init__(self, name)
        self.path = path
        self.start = start
        self.end = end

    def set_index(self, index):
        self._index = index

    def index(self):
        return self._index

    def vlink(self):
        return f'[{self.index()}:v:0]'

    def alink(self):
        return f'[{self.index()}:a:0]'

    def get_dims(self):
        w, h = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0',
                self.path,
            ],
            check=True,
            capture_output=True,
        ).stdout.decode('utf-8').strip().split(',')
        return (int(w), int(h))

# filters
class _Filter: pass

class Concat(_VAElement, _Filter):
    def __init__(self, name, inames):
        _Element.__init__(self, name)
        self.inames = inames

    def _filter(self):
        return ''.join([
            *[f'{_vlink(iname)}{_alink(iname)}' for iname in self.inames,
            f'concat={len(input_names)}:1:1',
            f'{self.vlink()}{self.alink()}',
        ])

class Scale(_VElement, _Filter):
    def __init__(self, name, iname, x, y):
        _Element.__init__(self, name)
        self.iname = iname
        self.x = x
        self.y = y

    def _filter(self):
        return (
            f'{_vlink(self.iname)}'
            f'scale={self.x}:{self.y}'
            f'{self.vlink()}'
        )

class Pad(_VElement, _Filter):
    def __init__(self, name, iname, w, h, x, y):
        _Element.__init__(self, name)
        self.iname = iname
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def _filter(self):
        return (
            f'{_vlink(self.iname)}'
            f'pad={self.w}:{self.h}:{self.x}:{self.y}'
            f'{self.vlink()}'
        )

# invocations
def concat_copy(ifile_names, opath='output.mov'):
    with open(TMP_PATH, 'w') as file:
        for name in ifile_names:
            ifile = _element(name)
            file.write(f'file {ifile.path}\n')
            if ifile.start != None:
                file.write(f'inpoint {ifile.start}\n')
            if ifile.end != None:
                file.write(f'outpoint {ifile.end}\n')
    subprocess.run(
        [
            'ffmpeg',
            '-f', 'concat',  # use the concat demuxer
            '-safe', '0',  # allow absolute file paths
            '-i', TMP_PATH,
            '-codec', 'copy',
            opath,
        ],
        check=True,
    )

def render(opath, vname, aname):
    ifile_options = []
    index = 0
    for element in _Element._elements.values():
        if isinstance(element, Ifile):
            if element.start != None:
                ifile_options.extend(['-ss', str(element.start)])
            if element.end != None:
                ifile_options.extend(['-t', str(element.end - (element.start or 0))])
            ifile_options.extend(['-i', element.path])
            element.set_index(index)
            index += 1
    filters = []
    for element in _Element._elements.values():
        if isinstance(element, _Filter):
            filters.append(element._filter())
    subprocess.run(
        [
            'ffmpeg',
            *ifile_options,
            '-filter_complex', ';'.join(filters),
            '-map', _vlink(vname),
            '-map', _alink(aname),
            opath,
        ],
        check=True,
    )

def concat_center(ifile_names, width=None, height=None, opath='output.mov'):
    # get dims from first source if needed
    if width == None or height == None:
        width, height = _element(source_names[0]).get_dims()
    # reshapes
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
            f'[reshaped{i}]'  # video of reshaped i
                + (f'[{i}:a:0]' if not source.silenced else '')  # audio of input i
            for i, source in enumerate(sources)
        ],
        f'concat={len(sources)}:1:1',  # map n inputs to 1 video and 1 audio stream
        '[v][a]',  # name the result
    ])

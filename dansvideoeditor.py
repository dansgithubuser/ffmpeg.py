class Node:
		def __init__(self, file_path):
				import os
				self.file_path=file_path

		def __add__(self, other):
				if not hasattr(self, 'children'): self.children=[]
				self.children.append(other)
				return self

		def trim(self, start, end):
				self.start=start
				self.end=end
				return self

		def render(self, width, height, copy=False, dry=False):
				render=self._render(width, height, copy)
				invocation='ffmpeg'
				if copy:
					with open('dansvideoeditor-temp.txt', 'w') as f: f.write(render['input_files'])
					invocation+=' -safe 0 -f concat -i dansvideoeditor-temp.txt -codec copy'
				else:
					invocation+=' '+render['input_files']
					invocation+=' -filter_complex "'
					invocation+=render['reshapes']
					invocation+=render['concat_links']+'concat=n='+str(render['index']+1)+':v=1:a=1[v][a]'
					invocation+='"'
					invocation+=' -map [v] -map [a]'
				invocation+=' output.mov'
				if dry: print(invocation)
				else:
						import subprocess
						subprocess.check_call(invocation, shell=True)

		def _render(self, width, height, copy, index=0):
			if copy:
				input_file='file '+self.file_path+'\n'
				if hasattr(self, 'start'):
					input_file+='inpoint '+str(self.start)+'\n'
					input_file+='outpoint '+str(self.end)+'\n'
			else:
				input_file='-i '+self.file_path
				if hasattr(self, 'start'):
					input_file='-ss '+str(self.start)+' -t '+str(self.end-self.start)+' '+input_file
			reshape ='[{i}:v:0]'
			reshape+='scale=iw*{m}:ih*{m}'
			reshape+=',pad={w}:{h}:({w}-iw*{m})/2:({h}-ih*{m})/2'
			reshape+='[reshaped{i}];'
			reshape=reshape.format(i=index, w=width, h=height, m=r'min({w}/iw\,{h}/ih)'.format(w=width, h=height))
			concat_link='[reshaped{0}][{0}:a:0]'.format(index)
			result={
				'input_files': input_file,
				'reshapes': reshape,
				'concat_links': concat_link,
				'index': index,
			}
			if hasattr(self, 'children'):
				for child in self.children:
					x=child._render(width, height, copy, result['index']+1)
					result={i: result[i]+' '+x[i] for i in ['input_files', 'reshapes', 'concat_links']}
					result['index']=x['index']
			return result

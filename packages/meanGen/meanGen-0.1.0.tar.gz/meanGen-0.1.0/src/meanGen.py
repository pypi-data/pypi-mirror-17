import os
import sys
import shutil
import errno

class main:
	def __init__(self):
		if len(sys.argv) > 1:
			if str(sys.argv[1]) == "new":
				if len(sys.argv) > 2:
					self.gen_mean(str(sys.argv[2]))
				else: 
					self.gen_mean('angularSkeleton')
			else:
				raise ValueError('To create a new pylot project run mean new project_name')
	def gen_mean(self, dest):
		try:
			current = os.path.dirname(os.path.realpath(__file__))
			src = current + "/angularSkeleton"
			shutil.copytree(src, dest, ignore=self.ignore_function('.git'))
		except OSError as e:
			if e.errno == errno.ENOTDIR:
				shutil.copy(src, dest, ignore=self.ignore_function('.git'))
			else:
				if e is not None:
					print('Directory not copied. Error: %s' % e)
				else:
					print('Directory not copied. Error: %s' % e)

	def ignore_function(self, ignore):
		def _ignore_(path, names):
			ignored_names = []
			if ignore in names:
				ignored_names.append(ignore)
			return set(ignored_names)
		return _ignore_
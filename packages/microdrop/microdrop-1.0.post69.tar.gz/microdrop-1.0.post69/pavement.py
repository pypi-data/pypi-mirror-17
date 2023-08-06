import os
import pkg_resources
import platform
import sys

from paver.easy import task, needs, path
from paver.setuputils import setup

root_dir = path(__file__).parent.abspath()
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import version


install_requires = ['application_repository>=0.5', 'blinker', 'configobj',
                    'flatland-fork', 'geo-util', 'ipython',
                    'ipython-helpers>=0.4', 'matplotlib>=1.5.0',
                    'microdrop-plugin-template>=1.1.post30',
                    'microdrop_utility>=0.4.post2', 'networkx',
                    'opencv-helpers', 'openpyxl', 'pandas', 'pandas',
                    'path-helpers>=0.2', 'paver>=1.2.4', 'pip-helpers>=0.6',
                    'pygst-utils>=0.2.post26,<0.3',
                    'pygtk_textbuffer_with_undo', 'pyparsing',
                    'pyutilib.component.core>=4.4.1',
                    'pyutilib.component.loader>=3.3.1', 'pyyaml', 'pyzmq',
                    'run-exe>=0.5', 'scipy', 'si-prefix',
                    'svg_model>=0.5.post24', 'svgwrite', 'task_scheduler',
                    'tornado', 'wheeler.pygtkhelpers>=0.12.post7']

if platform.system() == 'Windows':
    install_requires += ['pycairo-gtk2-win', 'pygst-0.10-win', 'pywin32']

try:
    import gtk
except ImportError:
    print >> sys.stderr, ("Please install Python bindings for Gtk 2 using "
                          "your system's package manager.")
try:
    import cairo
except ImportError:
    print >> sys.stderr, ("Please install Python bindings for cairo using "
                          "your system's package manager.")

setup(name='microdrop',
      version=version.getVersion(),
      description='Microdrop is a graphical user interface for the DropBot '
      'Digital Microfluidics control system',
      keywords='digital microfluidics dmf automation dropbot microdrop',
      author='Ryan Fobel and Christian Fobel',
      author_email='ryan@fobel.net and christian@fobel.net',
      url='http://microfluidics.utoronto.ca/microdrop',
      license='GPL',
      long_description='\n%s\n' % open('README.md', 'rt').read(),
      packages=['microdrop'],
      include_package_data=True,
      install_requires=install_requires)


@task
def create_requirements():
    package_list = [p.split('==')[0] for p in install_requires]
    requirements_path = os.path.join('microdrop', 'requirements.txt')
    with open(requirements_path, 'wb') as output:
        output.write('\n'.join(['%s==%s' %
                                (p, pkg_resources.get_distribution(p).version)
                                for p in package_list]))

@task
@needs('generate_setup', 'minilib', 'create_requirements',
       'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass

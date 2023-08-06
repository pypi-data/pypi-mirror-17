from setuptools import setup

setup(name='osm_hall_monitor',
      version='0.52',
      description='Passive changeset monitoring for OpenStreetMap.',
      url='http://github.com/ethan-nelson/osm_hall_monitor',
      author='Ethan Nelson',
      license='MIT',
      author_email='git@ethan-nelson.com',
      install_requires = ['psycopg2','osm_diff_tool'],
      packages=['osmhm'])
      

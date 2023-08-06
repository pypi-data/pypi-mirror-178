# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stream_video',
 'stream_video.gen',
 'stream_video.gen.permissions.permissions_v1_rpc',
 'stream_video.gen.validate',
 'stream_video.gen.video.coordinator.app_v1',
 'stream_video.gen.video.coordinator.broadcast_v1',
 'stream_video.gen.video.coordinator.call_v1',
 'stream_video.gen.video.coordinator.client_v1_rpc',
 'stream_video.gen.video.coordinator.edge_v1',
 'stream_video.gen.video.coordinator.event_v1',
 'stream_video.gen.video.coordinator.member_v1',
 'stream_video.gen.video.coordinator.participant_v1',
 'stream_video.gen.video.coordinator.permissions',
 'stream_video.gen.video.coordinator.push_v1',
 'stream_video.gen.video.coordinator.recording_v1',
 'stream_video.gen.video.coordinator.server_v1_rpc',
 'stream_video.gen.video.coordinator.stat_v1',
 'stream_video.gen.video.coordinator.user_v1',
 'stream_video.gen.video.coordinator.utils_v1',
 'stream_video.gen.video.sfu.cascading_rpc',
 'stream_video.gen.video.sfu.event',
 'stream_video.gen.video.sfu.models',
 'stream_video.gen.video.sfu.remote_control_rpc',
 'stream_video.gen.video.sfu.signal_rpc',
 'stream_video.gen.video.videoerr']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0,<3.0.0',
 'protobuf>=4.21.6,<5.0.0',
 'twirp>=0.0.7,<0.0.8',
 'typed-ast>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'stream-video',
    'version': '0.0.3',
    'description': '',
    'long_description': '# Stream Video Python SDK\n\n## Setup\n\n```bash\nmake deps\n```\n\n## Check\n\n```bash\nmake check\n```\n',
    'author': 'Stream.io',
    'author_email': 'support@getstream.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

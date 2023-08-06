# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpp_asgi']

package_data = \
{'': ['*']}

install_requires = \
['ocpp>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'ocpp-asgi',
    'version': '0.4.0',
    'description': 'ocpp-asgi provides ASGI compliant interface for implementing event-driven server-side support for OCPP protocol with Python',
    'long_description': '<p align="center">\n<a href="https://github.com/villekr/ocpp-asgi/actions?query=workflow%3Amain" target="_blank">\n    <img src="https://github.com/villekr/ocpp-asgi/workflows/main/badge.svg" alt="main">\n</a>\n<a href="https://codecov.io/gh/villekr/ocpp-asgi">\n  <img src="https://codecov.io/gh/villekr/ocpp-asgi/branch/main/graph/badge.svg?token=DZ2QWVF3DX"/>\n</a>\n<a href="https://pypi.org/project/ocpp-asgi" target="_blank">\n    <img src="https://img.shields.io/pypi/v/ocpp-asgi?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n</p>\n\n---\n\n# OCPP-ASGI\n\nocpp-asgi provides **ASGI compliant** interface for implementing **event-driven** **server-side** support for OCPP protocol with Python. It depends on and extends [mobilityhouse/ocpp](https://github.com/mobilityhouse/ocpp). \n\nThe key features are:\n* ASGI compliant interface supporting both WebSocket and HTTP protocols.\n* Event-driven and "stateless" approach for implementing action handlers for OCPP messages. \n* Highly-scalable and supports serverless (e.g. AWS Lambda, Azure Functions) with compatible ASGI server.\n* Requires small and straightforward changes from ocpp to action handlers (but is not backwards compatible).\n\nRead the [blog post](https://ville-karkkainen.medium.com/towards-event-based-serverless-ocpp-backend-system-part-i-motivation-and-architecture-options-5d51ba09dfd6) about the motivation behind creating this library.\n\n## Disclaimer!\n\nThis library is still in alpha state. At the moment I don\'t have time nor immediate business need to invest in further development. However, I\'m happy to discuss and help if you are considering the benefits of using this library in you project.\n\nPlease send [email](mailto:ville.karkkainen@outlook.com) if you have any questions about this library or have some business inquiries in mind.\n\n# Getting started\n\n## Installation\n\n```\npip install ocpp-asgi\n```\n\nAlso ASGI server is required e.g. [uvicorn](https://www.uvicorn.org) or [mangum](https://www.uvicorn.org) when deployed to AWS Lambda with API Gateway.\n```\npip install uvicorn\n```\n\n## Action handlers\n\nDecorating OCPP message action handlers follows the similar approach as in ocpp-library. However, you don\'t need to define classes per OCPP protocol version. \n\n```python\n# provisioning_router.py\nfrom datetime import datetime\n\nfrom ocpp.v16 import call, call_result\nfrom ocpp.v16.enums import Action, RegistrationStatus\n\nfrom ocpp_asgi.router import HandlerContext, Router, Subprotocol\n\nrouter = Router(subprotocol=Subprotocol.ocpp16)\n\n\n@router.on(Action.BootNotification)\nasync def on_boot_notification(\n    *, payload: call.BootNotificationPayload, context: HandlerContext\n) -> call_result.BootNotificationPayload:\n    id = context.charging_station_id\n    print(f"(Central System) on_boot_notification Charging Station {id=}")\n    # Do something with the payload...\n    return call_result.BootNotificationPayload(\n        current_time=datetime.utcnow().isoformat(),\n        interval=10,\n        status=RegistrationStatus.accepted,\n    )\n```\n\n## Central System\n\nCentral System is a collection of routes. You implement it by subclassing from ocpp_asti.ASGIApplication and overriding necessary methods to accommodate your needs. Here\'s a minimal example using uvicorn.\n\n```python\n# central_system.py\nimport uvicorn\nfrom provisioning_router import router\nfrom ocpp_asgi.app import ASGIApplication, RouterContext, Subprotocol\n\n\nclass CentralSystem(ASGIApplication):\n    """Central System is collection of routers."""\n\n\nif __name__ == "__main__":\n    central_system = CentralSystem()\n    central_system.include_router(router)\n    subprotocols = f"{Subprotocol.ocpp16}"\n    headers = [("Sec-WebSocket-Protocol", subprotocols)]\n    uvicorn.run(central_system, host="0.0.0.0", port=9000, headers=headers)\n```\n\n## Run the examples\n\nIn order to run the examples clone the ocpp-asgi repository and install dependencies. Poetry and pyenv are recommended.\n\nThere are two kind of examples how to implement central system with ocpp-asgi: standalone and serverless. Both examples use same ocpp action handlers (routers).\n\n### Standalone example\n\nRun the following commands e.g. in different terminal windows (or run the files within IDE).\n\nStart Central System:\n```\npython ./examples/central_system/standalone/central_system.py\n```\n\nStart Charging Station:\n```\npython ./examples/charging_station.py\n```\n\n### Serverless example\n\nRun the following commands in different terminal windows (or run the files within IDE). Of course when you run the example like this it\'s not really serverless. But deploying something central_system_http.py to e.g. AWS Lambda and running it with Mangum ASGI server is totally possible.\n\nStart Central System HTTP backend:\n```\npython ./examples/central_system/serverless/central_system_http.py\n```\n\nStart Central System WebSocket proxy:\n```\npython ./examples/central_system/serverless/central_system_proxy.py\n```\n\nStart Charging Station:\n```\npython ./examples/charging_station.py\n```',
    'author': 'Ville Kärkkäinen',
    'author_email': 'ville.karkkainen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/villekr/ocpp-asgi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)

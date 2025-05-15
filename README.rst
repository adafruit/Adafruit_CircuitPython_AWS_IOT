Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-aws-iot/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/aws_iot/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_AWS_IOT/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_AWS_IOT/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

Amazon AWS IoT MQTT Client for CircuitPython.


**Note**: This library requires version **>=1.4.0** of the `Adafruit fork of the Arduino NINA-W102 firmware <https://github.com/adafruit/nina-fw>`_
 installed on your ESP32 Airlift/WiFi Co-Processor.

If you do not know how to do this, `visit the Adafruit Learning System guide for this topic... <https://learn.adafruit.com/upgrading-esp32-firmware>`_


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit CircuitPython ConnectionManager <https://github.com/adafruit/Adafruit_CircuitPython_ConnectionManager/>`_
* `Adafruit CircuitPython MiniMQTT <https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-aws_iot/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-aws-iot

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-aws-iot

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-aws-iot

Usage Example
=============

Library examples within examples/ folder.

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/aws_iot/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_AWS_IOT/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

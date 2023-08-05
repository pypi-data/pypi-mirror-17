from setuptools import setup

setup(
    name="sPyNNakerExternalDevicesPlugin",
    version="3.0.0",
    description="Spinnaker External Devices Plugin",
    url="https://github.com/SpiNNakerManchester/SpyNNaker",
    packages=['spynnaker_external_devices_plugin',
              'spynnaker_external_devices_plugin.pyNN',
              'spynnaker_external_devices_plugin.pyNN.connections',
              'spynnaker_external_devices_plugin.pyNN.external_devices_models',
              'spynnaker_external_devices_plugin.pyNN.model_binaries',
              'spynnaker_external_devices_plugin.pyNN.utility_models'],
    package_data={'spynnaker_external_devices_plugin.pyNN.model_binaries': ['*.aplx']},
    install_requires=['sPyNNaker >= 3.0.0, < 4.0.0']
)

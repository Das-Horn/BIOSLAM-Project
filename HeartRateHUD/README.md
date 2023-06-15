# Heart Rate HUD

This part of the project contains a simple electron example that takes the current heart rate from a "bpm" topic on mqtt and displays it in a transparent always on top window on the pc. This allows the user to constantly see the window.

# Usage

To use this section of the project ensure node is installed. Then either using yarn or npm install the dependencies for it.
``` bash
npm install
```
or
``` bash
yarn
```
The server address for MQTT may have to be adjusted to connect to your broker. This configuration option can be found in renderer.js on *line 80*.

Then to run the program simply run npm or yarn + "start". This will compile and run the program.
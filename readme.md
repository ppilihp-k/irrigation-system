# Control Unit for my Irigation System

The System consist of multiple Gardena Sprinkler Valves, https://www.gardena.com/de/produkte/bewaesserung/sprinklersystem/bewaesserungsventil-24-v/900904101.html
Valves are controled by a Raspberry Pi Pico W.

## Development

The Software is developed with Thonny. 
Upload control_unit/ to the Root of the Picos Filesystem.
Create main.py in the Root by Hand. Insert

    from control_unit import main

into main.py.

## Let it Run

To be able to Run properly the Software needs access to a WLan Network and an MQTT Broker within this Network.
Create the following Files in control_unit/

    control_unit/wlan_config.txt
    {"ssid":"your_ssid","password":"your_pw"}

    control_unit/mqtt_config.txt
    {"host":"ip","port":1883,"user_name":"mqtt_username","password":"pw","topic":"/my_irigation_system/","client_id":"MY_IRIGATION_SYSTEM"} 

The Irigation System is not controlled via MQTT.

Subscribe to /my_irigation_system/ to get a List of available Valves. Subscribe to /my_irigation_system/valve_x, for x between 0 and 2, to get Statusupdates from each Valve.

Request a Valve State Change through a Publication to the Topic /my_irigation_system/command/
For Example 

    {"command":"set_actor_state", "data":{"actor":"valve_2","state":1}} to Open Valve 2 or 
    {"command":"set_actor_state", "data":{"actor":"valve_2","state":0}} to close it.

## Tests

Run Tests

    cd control_unit/
    python3 -m .venv && source .venv/bin/activate && pip install -r requirements.txt
    python -m unittest discover test.unittest



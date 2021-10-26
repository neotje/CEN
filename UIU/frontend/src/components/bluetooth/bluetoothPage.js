import React, { useEffect } from 'react';
import Box from '@material-ui/core/Box';
import { DiscoverySwitch } from './discoverySwitch';
import { PairedDevicesList } from './pairedDevicesList';
import { AvailableDevicesList } from './availableDevicesList';

export function BluetoothPage() {

    const [discovery, setDiscovery] = React.useState(false)
    const [pairedDevices, setPairedDevices] = React.useState([])
    const [nearbyDevices, setNearbyDevices] = React.useState([])
    const [discoveryInterval, setDiscoveryInterval] = React.useState()
    const [pairingTo, setPairingTo] = React.useState()

    const onDiscoverySwitch = (enable) => {

        if(enable) {
            window.uiu.api.bl_pause()
            setDiscoveryInterval(setInterval(retreiveDevices, 500))
        } else {
            window.uiu.api.bl_play()
            clearInterval(discoveryInterval)
            setDiscoveryInterval(setInterval(retreiveDevices, 2000))
        }

        window.uiu.api.bl_adapter_discovery(enable)
        setDiscovery(enable)
    }

    const retreiveDevices = () => {
        window.uiu.api.bl_devices().then(result => {
            let paired = []
            let nearby = []
            for (const device of result.devices) {
                if (device.Paired === 1) {
                    paired.push(device)
                } else if (device.Name !== "" && device.Name !== null) {
                    nearby.push(device)
                }
            }

            setPairedDevices(paired)
            setNearbyDevices(nearby)
        })
    }

    const onDeletePairedDevice = (device) => {
        window.uiu.api.bl_remove_device(device.Address).then(r => {
            retreiveDevices();
        })
    }

    const onPairDevice = (device) => {
        setPairingTo(device)
        window.uiu.api.bl_pair(device.Address).then(r => {
            setPairingTo(undefined)
            retreiveDevices()
        })
    }

    useEffect(() => {
        console.log("paired Devices list")
        retreiveDevices();
        setDiscoveryInterval(setInterval(retreiveDevices, 2000))
    }, [])

    return (
        <Box>
            <DiscoverySwitch onChange={onDiscoverySwitch} />
            <PairedDevicesList list={pairedDevices} onDelete={onDeletePairedDevice} />
            <AvailableDevicesList list={nearbyDevices} discovering={discovery} onClick={onPairDevice} pairingTo={pairingTo}/>
        </Box>
    )
}
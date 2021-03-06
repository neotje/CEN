import React, { useEffect } from 'react';
import Box from '@material-ui/core/Box';
import { DiscoverySwitch } from './discoverySwitch';
import { PairedDevicesList } from './pairedDevicesList';
import { AvailableDevicesList } from './availableDevicesList';
import { ApiSocketContext } from '../api/apiSocket';

export function BluetoothPage() {

    // TODO: check if discovery is already enabled
    const [discovery, setDiscovery] = React.useState(false)
    const [pairedDevices, setPairedDevices] = React.useState([])
    const [nearbyDevices, setNearbyDevices] = React.useState([])
    const [discoveryInterval, setDiscoveryInterval] = React.useState()
    const [pairingTo, setPairingTo] = React.useState()

    const {api} = React.useContext(ApiSocketContext)

    const onDiscoverySwitch = (enable) => {
        if (enable) {
            api.bl_pause()
            setDiscoveryInterval(setInterval(retreiveDevices, 1000))
        } else {
            api.bl_play()
            clearInterval(discoveryInterval)
            setDiscoveryInterval(setInterval(retreiveDevices, 2000))
        }

        api.bl_adapter_discovery(enable)
        setDiscovery(enable)
    }

    const retreiveDevices = () => {
        api.bl_devices().then(result => {
            let paired = []
            let nearby = []
            for (const device of result.devices) {
                if (device.Paired) {
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
        api.bl_remove_device(device.Address).then(r => {
            retreiveDevices();
        })
    }

    const onPairDevice = (device) => {
        setPairingTo(device)
        api.bl_pair(device.Address).then(r => {
            setPairingTo(undefined)
            retreiveDevices()
        })
    }

    useEffect(() => {
        console.log("paired Devices list")
        retreiveDevices();
        setDiscoveryInterval(setInterval(retreiveDevices, 2000))

        api.bl_is_discovering().then(r => {
            if(r.discovering) setDiscovery(true)         
        })
    }, [])

    return (
        <Box>
            <DiscoverySwitch onChange={onDiscoverySwitch} />
            <PairedDevicesList list={pairedDevices}
                onDelete={onDeletePairedDevice} />
            <AvailableDevicesList list={nearbyDevices}
                discovering={discovery}
                onClick={onPairDevice}
                pairingTo={pairingTo} />
        </Box>
    )
}
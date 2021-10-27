import BluetoothIcon from '@material-ui/icons/Bluetooth';
import SmartphoneIcon from '@material-ui/icons/Smartphone';
import ComputerIcon from '@material-ui/icons/Computer';

const AUDIO_SRC_UUID = "0000110a-0000-1000-8000-00805f9b34fb"

export function getDeviceIcon(device) {
    switch (device.Icon) {
        case "phone":
            return <SmartphoneIcon />

        case "computer":
            return <ComputerIcon />

        default:
            return <BluetoothIcon />

    }
}

export function hasAudioSrc(device) {
    for (const uuid of device.UUIDs) {
        if(uuid === AUDIO_SRC_UUID) return true
    }
    return false
}
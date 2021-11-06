import BluetoothIcon from '@material-ui/icons/Bluetooth';
import SmartphoneIcon from '@material-ui/icons/Smartphone';
import ComputerIcon from '@material-ui/icons/Computer';

export const AUDIO_SRC_UUID = "0000110a-0000-1000-8000-00805f9b34fb"
export const LED_STRIP_SERVICE = "dff41a39-471b-4ca1-a837-c76895946d78"

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
        if (uuid === AUDIO_SRC_UUID) return true
    }
    return false
}

export function hasService(device, uuid) {
    if (!isIterable(device.UUIDs)) return false

    for (const deviceUUID of device.UUIDs) {
        if (deviceUUID === uuid) return true
    }
    return false
}

function isIterable(obj) {
    // checks for null and undefined
    if (obj == null) {
        return false;
    }
    return typeof obj[Symbol.iterator] === 'function';
}
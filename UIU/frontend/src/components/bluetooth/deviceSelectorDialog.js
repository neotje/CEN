import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from "@material-ui/core"
import React from "react"
import { ApiSocketContext } from "../api/apiSocket"
import { AvailableDevicesList } from "./availableDevicesList"
import { hasService } from "./bluetoothTools"

export function DeviceSelectorDialog(props) {
    const onExit = props.onExit ? props.onExit : () => {}
    const onSelect= props.onSelect ? props.onSelect : (device) => {}
    const title = props.title ? props.title : "Selecteer een bluetooth apparaat"
    const service = props.service ? props.service : false
    const open = props.open ? props.open : false

    const [devices, setDevices] = React.useState([])
    const [discoveryInterval, setDiscoveryInterval] = React.useState()
    const {api} = React.useContext(ApiSocketContext)

    const handleClose = () => {
        onExit()
    }

    const handleSelect = (device) => {
        onSelect(device)
    }

    const retreiveDevices = () => {
        api.bl_devices().then(result => {
            let filtered = []
            for (const device of result.devices) {
                if (service) {
                    if (hasService(device, service)) {
                        filtered.push(device)
                    }
                } else {
                    filtered.push(device)
                }
            }

            setDevices(filtered)
        })
    }

    api.bl_adapter_discovery(open).then(() => {})

    if (open && discoveryInterval == undefined) {
        setDiscoveryInterval(setInterval(retreiveDevices, 500))
    }

    if (!open && discoveryInterval != undefined) {
        clearInterval(discoveryInterval)
        setDiscoveryInterval(undefined)
    }

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            scroll="paper"
        >
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                <AvailableDevicesList onClick={handleSelect} list={devices} pairingTo={props.pairingTo}/>
            </DialogContent>
            <DialogActions>
                <Button onClick={e => handleClose()} color="secondary">Annuleren</Button>
            </DialogActions>
        </Dialog>
    )
}
import { Box, Dialog, DialogContent, IconButton, List, ListItem, ListItemSecondaryAction, ListItemText } from "@material-ui/core";
import React from "react";
import { LED_STRIP_SERVICE } from "../bluetooth/bluetoothTools";
import { DeviceSelectorDialog } from "../bluetooth/deviceSelectorDialog";
import ChevronRight from "@material-ui/icons/ChevronRight";
import ColorizeIcon from '@material-ui/icons/Colorize';
import { HexColorPicker } from "react-colorful";
import frontLed from "../api/frontled";

export function LightingPage() {
    const [frontLedDevice, setFrontLedDevice] = React.useState(frontLed.device)
    const [openSelector, setOpenSelector] = React.useState(false)
    const [pairingTo, setPairingTo] = React.useState()
    const [fillColor, setFillColor] = React.useState(frontLed.fillColor)
    const [showPicker, setShowPicker] = React.useState(false)

    const onDeviceSelector = (device) => {
        setPairingTo(device)
        window.uiu.api.settings_set("frontLedDevice", device.Address)
        .then(result => {
            return frontLed.loadDevice(device.Address)
        })
        .then(() => {
            setFrontLedDevice(device.Address)
            setPairingTo(undefined)
            closeDeviceSelector()
        })
    }

    const openDeviceSelector = (e) => {
        setOpenSelector(true)
    }

    const closeDeviceSelector = () => {
        setOpenSelector(false)
    }

    const openColorPicker = () => {
        setShowPicker(true)
    }

    const closeColorPicker = () => {
        setShowPicker(false)
    }

    const changeFillColor = (color) => {
        setFillColor(color)
        frontLed.fill(color)
    }

    return (
        <Box marginTop={4}>
            <DeviceSelectorDialog open={openSelector} onSelect={onDeviceSelector} service={LED_STRIP_SERVICE} onExit={closeDeviceSelector} pairingTo={pairingTo}/>
            <Dialog open={showPicker} onClose={closeColorPicker} >
                <DialogContent>
                    <HexColorPicker color={fillColor === null ? "#000000" : fillColor} onChange={changeFillColor}/>
                </DialogContent>
            </Dialog>
            <List>
                <ListItem button onClick={openDeviceSelector}>
                    <ListItemText primary="FrontLED apparaat" />
                    <ListItemText secondary={frontLedDevice === null ? "geen" : frontLedDevice} />
                    <ListItemSecondaryAction>
                        <IconButton onClick={openDeviceSelector}>
                            <ChevronRight />
                        </IconButton>
                    </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                    <ListItemText>Kleur</ListItemText>
                    <ListItemSecondaryAction>
                        <IconButton style={{backgroundColor: fillColor}} onClick={e => openColorPicker()}>
                            <ColorizeIcon />
                        </IconButton>
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </Box>
    )
}
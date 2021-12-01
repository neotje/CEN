import { Box, IconButton, List, ListItem, ListItemSecondaryAction, ListItemText, Switch } from "@material-ui/core";
import React from "react";
import { ApiSocketContext } from "../api/apiSocket";
import { DeviceSelectorDialog } from "../bluetooth/deviceSelectorDialog";
import ChevronRight from "@material-ui/icons/ChevronRight";

export function NetworkPage() {
    const [openSelector, setOpenSelector] = React.useState(false)

    const { api } = React.useContext(ApiSocketContext)
    const [tethering, setTethering] = React.useState({ enabled: api.tethering.enabled, device: api.tethering.device })

    const setEnableTethering = (state) => {
        api.tethering.enabled = state
        const newValue = { ...tethering, enabled: state }
        setTethering(newValue)
    }

    const setTetheringDevice = (state) => {
        api.tethering.device = state
        const newValue = { ...tethering, device: state }
        setTethering(newValue)
    }

    const onDeviceSelector = (device) => {
        setTetheringDevice(device.Address)
        setOpenSelector(false)
    }

    return (
        <Box marginTop={4}>
            <DeviceSelectorDialog
                open={openSelector}
                onSelect={onDeviceSelector}
                service={api.tethering.NETWORK_SERVICE}
                onExit={e => setOpenSelector(false)}
            />
            <List>
                <ListItem>
                    <ListItemText>Bluetooth-tethering</ListItemText>
                    <ListItemSecondaryAction>
                        <Switch checked={api.tethering.enabled} onChange={e => setEnableTethering(e.target.checked)} />
                    </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                    <ListItemText primary="Tethering apparaat" />
                    <ListItemText secondary={tethering.device === null ? "geen" : tethering.device} />
                    <ListItemSecondaryAction>
                        <IconButton onClick={e => setOpenSelector(true)}>
                            <ChevronRight />
                        </IconButton>
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </Box>
    )
}
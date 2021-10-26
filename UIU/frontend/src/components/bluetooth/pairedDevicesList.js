import { IconButton, List, ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText, ListSubheader } from '@material-ui/core';
import React, { useEffect } from 'react';
import BluetoothIcon from '@material-ui/icons/Bluetooth';
import DeleteIcon from '@material-ui/icons/Delete';

export function PairedDevicesList(props) {
    const pairedDevices = props.list ? props.list : []

    const handleDelete = (device) => {
        if(props.onDelete) props.onDelete(device)
    }

    const listItems = pairedDevices.map((device, i) =>
        <ListItem key={i}>
            <ListItemIcon>
                <BluetoothIcon />
            </ListItemIcon>
            <ListItemText primary={device.Name} secondary={device.Connected === 1 ? "Verbonden" : undefined} />
            <ListItemSecondaryAction>
                <IconButton onClick={ e => handleDelete(device)}>
                    <DeleteIcon />
                </IconButton>
            </ListItemSecondaryAction>
        </ListItem>
    )

    return (
        <List
            subheader={
                <ListSubheader>
                    Gekoppelde Apparaten
                </ListSubheader>
            }
        >
            {listItems}
        </List>
    )
}
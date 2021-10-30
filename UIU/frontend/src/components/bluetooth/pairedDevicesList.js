import { IconButton, List, ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText, ListSubheader } from '@material-ui/core';
import React from 'react';
import DeleteIcon from '@material-ui/icons/Delete';
import { getDeviceIcon } from './bluetoothTools';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    listItem: {
        color: theme.palette.text.primary
    }
}))

export function PairedDevicesList(props) {
    const classes = useStyles()
    const pairedDevices = props.list ? props.list : []

    const handleDelete = (device) => {
        if (props.onDelete) props.onDelete(device)
    }

    const listItems = pairedDevices.map(
        (device, i) => {
            var icon = getDeviceIcon(device)

            return <ListItem key={i} className={classes.listItem}>
                <ListItemIcon>
                    {icon}
                </ListItemIcon>
                <ListItemText primary={device.Name} secondary={device.Connected === 1 ? "Verbonden" : undefined} />
                <ListItemSecondaryAction>
                    <IconButton onClick={e => handleDelete(device)}>
                        <DeleteIcon />
                    </IconButton>
                </ListItemSecondaryAction>
            </ListItem>
        }
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
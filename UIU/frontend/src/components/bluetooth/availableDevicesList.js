import { CircularProgress, IconButton, List, ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText, ListSubheader, Grid } from '@material-ui/core';
import React, { useEffect } from 'react';
import BluetoothIcon from '@material-ui/icons/Bluetooth';
import DeleteIcon from '@material-ui/icons/Delete';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
    searchProgress: {
        marginRight: "1rem"
    }
})

export function AvailableDevicesList(props) {
    const classes = useStyles()
    const nearbyDevices = props.list ? props.list : []
    const progressDevice = props.pairingTo ? props.pairingTo : undefined

    const handleOnClick = (device) => {
        if(props.onClick) props.onClick(device)
    }

    const listItems = nearbyDevices.map((device, i) =>
        <ListItem key={i} button onClick={e => {handleOnClick(device)}}>
            <ListItemIcon>
                <BluetoothIcon />
            </ListItemIcon>
            <ListItemText primary={device.Name} secondary={device == progressDevice ? "Verbinden..." : undefined} />
        </ListItem>
    )

    return (
        <List
            subheader={
                <ListSubheader>
                    <Grid
                        container
                        justifyContent="space-between"
                    >
                        <Grid item>
                            Beschikbare Apparaten
                        </Grid>
                        <Grid item>
                            {
                                props.discovering &&
                                <CircularProgress className={classes.searchProgress} color="secondary" size={20} />
                            }
                        </Grid>
                    </Grid>
                </ListSubheader>
            }
        >
            {listItems}
        </List>
    )
}
import { CircularProgress, List, ListItem, ListItemIcon, ListItemText, ListSubheader, Grid } from '@material-ui/core';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { getDeviceIcon } from './bluetoothTools';

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
        if (props.onClick) props.onClick(device)
    }

    const listItems = nearbyDevices.map(
        (device, i) => {
            var icon = getDeviceIcon(device)

            return <ListItem key={i} button onClick={e => { handleOnClick(device) }}>
                <ListItemIcon>
                    {icon}
                </ListItemIcon>
                <ListItemText primary={device.Name} secondary={device === progressDevice ? "Verbinden..." : undefined} />
            </ListItem>
        }
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
import { CircularProgress, List, ListItem, ListItemIcon, ListItemText, ListSubheader, Grid } from '@material-ui/core';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { getDeviceIcon } from './bluetoothTools';

const useStyles = makeStyles((theme) => ({
    searchProgress: {
        marginRight: "1rem"
    },
    listItem: {
        color: theme.palette.text.primary
    }
}))

export function AvailableDevicesList(props) {
    const classes = useStyles(props)
    const nearbyDevices = props.list ? props.list : []
    const progressDevice = props.pairingTo ? props.pairingTo : undefined

    const handleOnClick = (device) => {
        if (props.onClick) props.onClick(device)
    }

    const listItems = nearbyDevices.map(
        (device, i) => {
            var icon = getDeviceIcon(device)

            return <ListItem key={i} button onClick={e => { handleOnClick(device) }} className={classes.listItem}>
                <ListItemIcon>
                    {icon}
                </ListItemIcon>
                <ListItemText primary={device.Name === null ? device.Address : device.Name} secondary={progressDevice && device.Address === progressDevice.Address ? "Verbinden..." : undefined} />
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
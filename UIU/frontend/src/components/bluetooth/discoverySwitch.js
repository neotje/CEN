import {  Switch, Typography, Grid } from '@material-ui/core';
import React from 'react';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        color: theme.palette.text.primary
    }
}))

export function DiscoverySwitch(props) {
    const classes = useStyles()
    const [state, setState] = React.useState({
        enable: false
    })

    const handleChange = (event) => {
        setState({ ...state, enable: event.target.checked})

        if(props.onChange) {
            props.onChange(event.target.checked)
        }
    }

    return (
        <Grid 
            container
            alignItems="center"
            justifyContent="space-evenly"
            className={classes.root}
        >
            <Grid item>
                <Typography variant="body1">Scannen</Typography>
            </Grid>
            <Grid>
                <Switch 
                    checked={state.enable}
                    onChange={handleChange}
                />
            </Grid>
        </Grid>
    )
}
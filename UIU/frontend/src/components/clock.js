import { Typography } from '@material-ui/core';
import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1)
    }
}))

export function Clock(props) {
    const classes = useStyles(props)
    const [value, setValue] = useState(new Date())

    useEffect(() => {
        const interval = setInterval(
            () => setValue(new Date()),
            1000
        )

        return () => {
            clearInterval(interval)
        }
    })

    return (
        <div className={classes.root}>
            <Typography align='right' variant='caption'>
                {value.getHours()}:{value.getMinutes().toString().length < 2 ? "0" + value.getMinutes().toString() : value.getMinutes()}
            </Typography>
        </div>
    )
}
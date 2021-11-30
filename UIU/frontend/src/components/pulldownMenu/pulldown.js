import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Box, Card, CardContent, Container, Divider, Paper, SwipeableDrawer, Typography } from '@material-ui/core';
import { BrightnessSlider } from './brightnessSlider';
import { QuickTiles } from './quicktiles';

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: "rgba(0, 0, 0, 0)"
    },
    background: {
        backgroundColor: "rgba(0, 0, 0, 0)"
    },
    content: {
        margin: theme.spacing(1),
        padding: theme.spacing(2)
    },
    quicktile: {
        marginBottom: theme.spacing(2)
    }
}))

export function Pulldown(props) {
    const classes = useStyles(props)
    const [open, setOpen] = useState(false)

    return (
        <React.Fragment>
            <SwipeableDrawer
                anchor='top'
                open={open}
                onOpen={e => setOpen(true)}
                onClose={e => setOpen(false)}
                className={classes.root}
                PaperProps={{
                    className: classes.background,
                    elevation: 0
                }}
            >
                <Container maxWidth="sm">
                    <Paper className={classes.content}>
                        <QuickTiles className={classes.quicktile} />
                        <BrightnessSlider />
                    </Paper>
                </Container>
            </SwipeableDrawer>
        </React.Fragment>
    )
}
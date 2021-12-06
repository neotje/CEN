import React from "react";
import { Grid, IconButton } from "@material-ui/core";
import { CustomThemeContext } from "../theme/customThemeProvider";
import Brightness4Icon from '@material-ui/icons/Brightness4';
import Brightness7Icon from '@material-ui/icons/Brightness7';
import WbIncandescentIcon from '@material-ui/icons/WbIncandescent';

import { makeStyles } from '@material-ui/core/styles';
import { ApiSocketContext } from "../api/apiSocket";
import frontLed from "../api/frontled";

const useStyles = makeStyles((theme) => ({
    tile: {
        backgroundColor: theme.palette.divider,
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        '&:hover': {
            backgroundColor: theme.palette.divider,
        }
    }
}))

export function QuickTiles(props) {
    const classes = useStyles(props)
    const { currentTheme, setTheme } = React.useContext(CustomThemeContext)
    const { api } = React.useContext(ApiSocketContext)

    const [fillColor, setFillColor] = React.useState(frontLed.fillColor)

    const themeIcon = currentTheme === "light" ? <Brightness4Icon /> : <Brightness7Icon />
    const ledIconColor = fillColor === "#000000" ? undefined : "yellow"


    React.useEffect(() => {
        frontLed.setup(api).then(() => {
            setFillColor(frontLed.fillColor)
        })
    }, [])

    const handleThemeToggle = () => {
        setTheme(currentTheme === "light" ? "dark" : "light")
    }

    const handleLedStripToggle = () => {
        if (fillColor == "#000000") {
            frontLed.setup(api).then(() => {
                setFillColor(frontLed.fillColor)
            })
        } else {
            frontLed.fill("#000000", api).then(() => {})
            setFillColor("#000000")
        }
    }

    return (
        <Grid container className={props.className}>
            <Grid item>
                <IconButton className={classes.tile} onClick={e => handleThemeToggle()}>
                    {themeIcon}
                </IconButton>
                <IconButton className={classes.tile} onClick={e => handleLedStripToggle()}>
                    <WbIncandescentIcon htmlColor={ledIconColor} />
                </IconButton>
            </Grid>
        </Grid>
    )
}
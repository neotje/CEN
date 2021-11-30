import React from "react";
import { Grid, IconButton } from "@material-ui/core";
import { CustomThemeContext } from "../theme/customThemeProvider";
import Brightness4Icon from '@material-ui/icons/Brightness4';
import Brightness7Icon from '@material-ui/icons/Brightness7';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    tile: {
        backgroundColor: theme.palette.divider
    }
}))

export function QuickTiles(props) {
    const classes = useStyles(props)
    const { currentTheme, setTheme } = React.useContext(CustomThemeContext)
    const icon = currentTheme === "light" ? <Brightness4Icon /> : <Brightness7Icon />
    const handleThemeToggle = () => {
        setTheme(currentTheme === "light" ? "dark" : "light")
    }

    return (
        <Grid container className={props.className}>
            <Grid item>
                <IconButton className={classes.tile} onClick={e => handleThemeToggle()}>
                    {icon}
                </IconButton>
            </Grid>
        </Grid>
    )
}
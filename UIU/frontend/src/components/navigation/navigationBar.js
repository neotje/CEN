import { BottomNavigation, Container, IconButton } from "@material-ui/core"
import { makeStyles } from '@material-ui/core/styles';
import React from "react";
import Brightness4Icon from '@material-ui/icons/Brightness4';
import Brightness7Icon from '@material-ui/icons/Brightness7';

const useStyles = makeStyles((theme) => ({
    root: {
        position: "relative",
        backgroundColor: theme.palette.background.default
    },
    nav: {
        backgroundColor: theme.palette.background.default
    },
    themeToggle: {
        position: "absolute",
        right: 0,
        top: 0
    },  
}))

export function NavigationBar(props) {
    const onNavigation = props.onNavigation ? props.onNavigation : (val) => { }

    const { children, value } = props
    const classes = useStyles(props)

    return (
        <Container className={classes.root}>
            <BottomNavigation className={classes.nav} value={value} onChange={(e, i) => onNavigation(i)}>
                {children}
            </BottomNavigation>
        </Container>
    )
}
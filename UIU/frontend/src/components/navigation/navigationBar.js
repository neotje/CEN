import { BottomNavigation, Button, Container, IconButton, Switch } from "@material-ui/core"
import { makeStyles } from '@material-ui/core/styles';
import React from "react";
import { CustomThemeContext } from "../theme/customThemeProvider";
import Brightness4Icon from '@material-ui/icons/Brightness4';
import Brightness7Icon from '@material-ui/icons/Brightness7';

const useStyles = makeStyles((theme) => ({
    root: {
        position: "relative"
    },
    themeToggle: {
        position: "absolute",
        right: 0,
        top: 0
    },  
}))

export function NavigationBar(props) {
    const onNavigation = props.onNavigation ? props.onNavigation : (val) => { }
    const onTheme = props.onTheme ? props.onTheme : () => {}
    const theme = props.theme ? props.theme : "light"

    const { children, value } = props

    const classes = useStyles(props)

    const icon = theme == "light" ? <Brightness4Icon /> : <Brightness7Icon />

    const handleToggleTheme = () => {
        onTheme()
    }

    return (
        <Container className={classes.root}>
            <BottomNavigation value={value} onChange={(e, i) => onNavigation(i)}>
                {children}
            </BottomNavigation>
            <IconButton className={classes.themeToggle} onClick={e => handleToggleTheme()}>
                {icon}
            </IconButton>
        </Container>
    )
}
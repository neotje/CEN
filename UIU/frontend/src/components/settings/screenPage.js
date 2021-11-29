import { Box, Grid, IconButton, List, ListItem, ListItemSecondaryAction, ListItemText, Slider, Switch, Typography } from "@material-ui/core"
import BrightnessHigh from "@material-ui/icons/BrightnessHigh";
import BrightnessLow from "@material-ui/icons/BrightnessLow";
import React from "react";
import { ApiSocketContext } from "../api/apiSocket";
import { CustomThemeContext } from "../theme/customThemeProvider";

export function ScreenPage() {
    const [brightness, _setBrightness] = React.useState(0);
    const themeManager = React.useContext(CustomThemeContext);
    const {api} = React.useContext(ApiSocketContext)

    console.log(themeManager);

    React.useEffect(() => {
        api.brightness_get().then(result => {
            setBrightness(result.value / 255 * 100)
        })
    }, [])

    const setBrightness = (value) => {
        api.brightness_set(value / 100 * 255)
        _setBrightness(value)
    }

    const handleBrightnessSlider = (event, newvalue) => {
        setBrightness(newvalue);
    }

    const increaseBrightnessButton = (e) => {
        setBrightness(brightness + 10);
    }

    const decreaseBrightnessButton = (e) => {
        setBrightness(brightness - 10);
    }

    const handleDarkModeSwitch = (event) => {
        if(themeManager.currentTheme === "dark") {
            themeManager.setTheme("light");
        } else {
            themeManager.setTheme("dark");
        }
    }

    return (
        <Box marginTop={4}>
            <List>
                <ListItem>
                    <Box width="100%">
                        <Typography gutterBottom>
                            Scherm helderheid
                        </Typography>
                        <Grid container spacing={2} alignItems="center">
                            <Grid item>
                                <IconButton onClick={decreaseBrightnessButton}>
                                    <BrightnessLow />
                                </IconButton>
                            </Grid>
                            <Grid item xs>
                                <Slider value={brightness} onChange={handleBrightnessSlider} />
                            </Grid>
                            <Grid item>
                                <IconButton onClick={increaseBrightnessButton}>
                                    <BrightnessHigh />
                                </IconButton>
                            </Grid>
                        </Grid>
                    </Box>
                </ListItem>
                <ListItem>
                    <ListItemText primary="Donkere modus" />
                    <ListItemSecondaryAction>
                        <Switch checked={themeManager.currentTheme === "dark"} onChange={handleDarkModeSwitch}/>
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </Box>
    )
}
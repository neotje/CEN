import React from "react";
import { Grid, IconButton, Slider } from "@material-ui/core";
import BrightnessHigh from "@material-ui/icons/BrightnessHigh";
import BrightnessLow from "@material-ui/icons/BrightnessLow";
import { ApiSocketContext } from "../api/apiSocket";

export function BrightnessSlider() {
    const [brightness, _setBrightness] = React.useState(0);

    const {api} = React.useContext(ApiSocketContext)

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

    React.useEffect(() => {
        api.brightness_get().then(result => {
            setBrightness(result.value / 255 * 100)
        })
    }, [])

    return (
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
    )
}
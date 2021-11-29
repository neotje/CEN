import React from "react"
import { ApiSocket } from "./apiSocket";

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
     ] : null;
}

class FrontLED {
    device
    fillColor

    setup(api) {
        return api.settings_get("frontLedFillColor")
            .then(result => {
                this.fillColor = result.value

                this.fill(this.fillColor === null ? "#000000" : this.fillColor, api)
            })
            .catch(() => {
            })
    }

    fill(color, api) {
        this.fillColor = color
        api.settings_set("frontLedFillColor", color).then(result => { })
        return api.frontLed_fill("all", hexToRgb(color)).then(result => { })
    }
}

const frontLed = new FrontLED()
export default frontLed
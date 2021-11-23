import React from "react"

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

    constructor() { }

    setup() {
        return window.uiu.api.settings_get("frontLedFillColor")
            .then(result => {
                this.fillColor = result.value

                this.fill(this.fillColor === null ? "#000000" : this.fillColor)
            })
            .catch(() => {
            })
    }

    fill(color) {
        this.fillColor = color
        window.uiu.api.settings_set("frontLedFillColor", color).then(result => { })
        return window.uiu.api.frontLed_fill("all", hexToRgb(color)).then(result => { })
    }
}

const frontLed = new FrontLED()
export default frontLed
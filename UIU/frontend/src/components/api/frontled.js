import React from "react"

class FrontLED {
    device
    fillColor

    constructor() {}
    
    setup() {
        return window.uiu.api.settings_get("frontLedDevice")
        .then(result => {
            this.device = result.value

            return this.loadDevice(this.device)
        })
        .then(result => {
            return window.uiu.api.settings_get("frontLedFillColor")
        })
        .then(result => {
            this.fillColor = result.value

            this.fill(this.fillColor === null ? "#000000" : this.fillColor)
        })
        .catch(() => {
        })
    }

    hasDevice() {
        return this.device !== null && this.device !== undefined
    }

    fill(color) {
        this.fillColor = color
        window.uiu.api.settings_set("frontLedFillColor", color).then(result => {})
        return window.uiu.api.frontLed_fill("all", color).then(result => {})
    }

    loadDevice(device) {
        return window.uiu.api.frontLed_loadDevice(device).then(result => {
            this.device = device
        })
    }
}

const frontLed = new FrontLED()
export default frontLed
import { Box, Dialog, DialogContent, IconButton, List, ListItem, ListItemSecondaryAction, ListItemText } from "@material-ui/core";
import React from "react";
import ColorizeIcon from '@material-ui/icons/Colorize';
import { HexColorPicker } from "react-colorful";
import frontLed from "../api/frontled";
import { ApiSocketContext } from "../api/apiSocket";

export function LightingPage() {
    const [fillColor, setFillColor] = React.useState(frontLed.fillColor)
    const [showPicker, setShowPicker] = React.useState(false)

    const {api} = React.useContext(ApiSocketContext)

    const openColorPicker = () => {
        setShowPicker(true)
    }

    const closeColorPicker = () => {
        setShowPicker(false)
    }

    const changeFillColor = (color) => {
        setFillColor(color)
        frontLed.fill(color, api)
    }

    return (
        <Box marginTop={4}>
            <Dialog open={showPicker} onClose={closeColorPicker} >
                <DialogContent>
                    <HexColorPicker color={fillColor === null ? "#000000" : fillColor} onChange={changeFillColor}/>
                </DialogContent>
            </Dialog>
            <List>
                <ListItem>
                    <ListItemText>Kleur</ListItemText>
                    <ListItemSecondaryAction>
                        <IconButton style={{backgroundColor: fillColor}} onClick={e => openColorPicker()}>
                            <ColorizeIcon />
                        </IconButton>
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </Box>
    )
}
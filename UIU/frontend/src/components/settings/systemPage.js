import { Box, Button, ButtonGroup, List, ListItem, ListItemSecondaryAction, ListItemText } from "@material-ui/core"
import React from "react"
import { ConfirmInput } from "./confirmInput"

export function SystemPage() {
    const [confirmShutdown, setConfirmShutdown] = React.useState(false)
    const [confirmReboot, setConfirmReboot] = React.useState(false)

    const handleShutdownBtn = (e) => {
        setConfirmShutdown(true)
    }

    const handleRebootBtn = (e) => {
        setConfirmReboot(true)
    }

    const handleShutdownConfirmation = (confirmed) => {
        setConfirmShutdown(false)

        if (confirmed) {
            console.log("shutdown");
            window.uiu.api.system_shutdown().then(() => {})
        }
    }

    const handleRebootConfirmation = (confirmed) => {
        setConfirmReboot(false)

        if (confirmed) {
            console.log("reboot");
            window.uiu.api.system_reboot().then(() => {})
        }
    }

    const handleSoftRebootBtn = ()=> {
        console.log("reboot");
        window.uiu.api.system_softReboot().then(() => {})
    }

    return (
        <Box marginTop={4}>
            <ConfirmInput
                open={confirmShutdown}
                title="Wil je de Matiz UI afsluiten?" body="Als je de Matiz UI afsluit is het mogelijk dat sommige belangrijke systemen niet meer werken!"
                onClick={handleShutdownConfirmation}
            />
            <ConfirmInput
                open={confirmReboot}
                title="Wil je de Matiz UI herstarten?" body="Let op! tijdens het herstarten zijn sommige belangrijke systemen niet beschikbaar!"
                onClick={handleRebootConfirmation}
            />
            <List>
                <ListItem>
                    <ListItemText primary="Power opties" />
                    <ListItemSecondaryAction>
                        <ButtonGroup variant="contained" size="small">
                            <Button color="primary" onClick={handleRebootBtn}>Herstarten</Button>
                            <Button color="" onClick={handleSoftRebootBtn}>Soft Reboot</Button>
                            <Button color="secondary" onClick={handleShutdownBtn}>Afsluiten</Button>
                        </ButtonGroup>
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </Box>
    )
}
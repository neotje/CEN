import { Avatar, List, ListItem, ListItemAvatar, ListItemText } from "@material-ui/core";
import Brightness6Icon from '@material-ui/icons/Brightness6';
import PowerSettingsNewIcon from '@material-ui/icons/PowerSettingsNew';
import WbIncandescentIcon from '@material-ui/icons/WbIncandescent';
import WifiIcon from '@material-ui/icons/Wifi';
import React from "react";
import { PageManagerContext } from "../navigation/pageManagerProvider";

function SettingsItem(props) {
    const { label, icon, page } = props

    const pageManager = React.useContext(PageManagerContext)

    return (
        <ListItem button onClick={e => pageManager.goTo(page)}>
            <ListItemAvatar>
                <Avatar>
                    {icon}
                </Avatar>
            </ListItemAvatar>
            <ListItemText primary={label} />
        </ListItem>
    )
}

export function SettingsHome() {
    return (
        <List>
            <SettingsItem label="Scherm en helderheid" icon={<Brightness6Icon />} page="screen" />
            <SettingsItem label="Verlichting" icon={<WbIncandescentIcon />} page="lighting" />
            <SettingsItem label="Netwerk" icon={<WifiIcon />} page="network" />
            <SettingsItem label="Systeem" icon={<PowerSettingsNewIcon />} page="system" />
        </List>
    )
}
import { Container } from "@material-ui/core";
import React from "react";
import { PageManagerProvider } from "../navigation/pageManagerProvider";
import { LightingPage } from "./lightingPage";
import { NetworkPage } from "./networkPage";
import { ScreenPage } from "./screenPage";
import { SettingsHome } from "./settingsHome";
import { SystemPage } from "./systemPage";

export function SettingsPage() {
    const settingsPages = {
        home: {
            title: "Instellingen",
            elem: <SettingsHome />
        },
        screen: {
            title: "Scherm en helderheid",
            elem: <ScreenPage />
        },
        system: {
            title: "Systeem",
            elem: <SystemPage />
        },
        lighting: {
            title: "Verlichting",
            elem: <LightingPage />
        },
        network: {
            title: "Netwerk",
            elem: <NetworkPage />
        }
    }

    return (
        <Container>
            <PageManagerProvider breadcrumbs={true} pages={settingsPages} />
        </Container>
    )
}
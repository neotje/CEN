import { Container } from "@material-ui/core";
import React from "react";
import { PageManagerProvider } from "../navigation/pageManagerProvider";
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
        }
    }

    return (
        <Container>
            <PageManagerProvider breadcrumbs={true} pages={settingsPages} />
        </Container>
    )
}
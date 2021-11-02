import React from 'react'
import { ThemeProvider } from '@material-ui/core/styles'
import getTheme from './themes'

export const CustomThemeContext = React.createContext({
    currentTheme: 'light',
    setTheme: null,
})

export function CustomThemeProvider(props) {
    const { children } = props

    const currentTheme = 'light'

    const [themeName, _setThemeName] = React.useState(currentTheme)

    const theme = getTheme(themeName)

    const setThemeName = (name) => {
        console.log("Setting them to", name);
        window.uiu.api.settings_set("theme", name)
        _setThemeName(name)
    }

    const contextValue = {
        currentTheme: themeName,
        setTheme: setThemeName,
    }

    return (
        <CustomThemeContext.Provider value={contextValue}>
            <ThemeProvider theme={theme}>{children}</ThemeProvider>
        </CustomThemeContext.Provider>
    )
}

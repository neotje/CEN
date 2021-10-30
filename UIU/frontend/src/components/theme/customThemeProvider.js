import React from 'react'
import { ThemeProvider } from '@material-ui/core/styles'
import getTheme from './themes'

export const CustomThemeContext = React.createContext({
    currentTheme: 'light',
    setTheme: null,
})

export function CustomThemeProvider(props) {
    const { children } = props

    const currentTheme = localStorage.getItem('appTheme') || 'light'

    const [themeName, _setThemeName] = React.useState(currentTheme)

    const theme = getTheme(themeName)

    const setThemeName = (name) => {
        localStorage.setItem('appTheme', name)
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

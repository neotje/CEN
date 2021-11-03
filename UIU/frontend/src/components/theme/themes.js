import { createTheme } from "@material-ui/core/styles"

const colors = {
    primary: {
        light: '#5e92f3',
        main: '#1565c0',
        dark: '#003c8f',
        contrastText: '#fff',
    },
    secondary: {
        light: '#ffc046',
        main: '#ff8f00',
        dark: '#c56000',
        contrastText: '#000',
    },
}

const themes = {
    light: createTheme({
        palette: {
            ...colors,
            type: "light"
        }
    }),
    dark: createTheme({
        palette: {
            ...colors,
            type: "dark"
        },
    })
}

export default function getTheme(name) {
    if (name in themes) return themes[name]
    return themes.light
}
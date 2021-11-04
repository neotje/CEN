import { createTheme } from "@material-ui/core/styles"

const shared = createTheme({
    palette: {
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
    },
    typography: {
        fontSize: 18
    },
    spacing: 8,
    shape: {
        borderRadius: 6
    }
})

const themes = {
    light: createTheme({
        ...shared,
        palette: {
            type: "light"
        }
    }),
    dark: createTheme({
        ...shared,
        palette: {
            type: "dark"
        },
    })
}

export default function getTheme(name) {
    if (name in themes) return themes[name]
    return themes.light
}
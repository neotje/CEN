import { createTheme } from "@material-ui/core/styles"

const themes = {
    light: createTheme({
        palette: {
            type: "light"
        }
    }),
    dark: createTheme({
        palette: {
            type: "dark"
        }
    })
}

export default function getTheme(name) {
    if(name in themes) return themes[name]
    return themes.light
}
import { Box, Breadcrumbs, Link } from "@material-ui/core";
import React from "react";

export const PageManagerContext = React.createContext({
    history: ["home"],
    current: "home",
    pages: {},
    addPage: (page, elem) => { },
    goTo: (page) => { },
    goBack: () => { },
})

export function PageManagerProvider(props) {
    const { init, breadcrumbs } = props
    const [history, setHistory] = React.useState(["home"])
    const [current, setCurrent] = React.useState("home")
    const [pages, setPages] = React.useState(props.pages ? props.pages : {})

    const addPage = (page, title, elem) => {
        var newPages = { ...pages }
        newPages[page] = {
            elem,
            title
        }
        setPages(newPages)
    }

    const goTo = (page) => {
        if (page === current) return

        if (page === "home") {
            setHistory(["home"])
        } else {
            var newHistory = [...history]
            newHistory.push(page)

            setHistory(newHistory)
        }
        setCurrent(page)
    }

    const goBack = () => {
        var newHistory = [...history]
        newHistory.pop()

        setHistory(newHistory)
        setCurrent(newHistory[newHistory.length - 1])
    }
    const contextValue = {
        history,
        current,
        pages,
        addPage,
        goTo,
        goBack,
    }

    React.useState(() => {
        if (init) {
            init(contextValue)
        }
    }, [])

    console.log(history)
    const crumbs = history.map((page) => {
        const clickHandler = (e) => {
            e.preventDefault()
            goTo(page)
        }

        const title = pages[page] ? pages[page].title : page

        const color = page == current ? "secondary" : "primary"

        return (
            <Link href="#" onClick={clickHandler} color={color}>{title}</Link>
        )
    })

    return (
        <PageManagerContext.Provider value={contextValue}>
            {breadcrumbs === true &&
                <Box>
                    <Breadcrumbs>
                        {crumbs}
                    </Breadcrumbs>
                </Box>
            }
            {pages ? pages[current]?.elem : <p>Unkown</p>}
        </PageManagerContext.Provider>
    )
}
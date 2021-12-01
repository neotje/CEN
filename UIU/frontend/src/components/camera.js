import { Box } from "@material-ui/core"
import { makeStyles } from "@material-ui/styles"
import React from "react"

const useStyles = makeStyles((theme) => ({
    root: {
        padding: 0
    },
    video: {
        height: "100%",
        width: "100%"
    }
}))

export function Camera() {
    const video = React.useRef()
    const classes = useStyles()

    React.useEffect(() => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                video.current.srcObject = stream
            })
    }, [])

    return (
        <video className={classes.video} ref={video} autoPlay>

        </video>
    )
}
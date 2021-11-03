import { Fade, Grid, LinearProgress, makeStyles } from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
    root: {
        height: "100vh",
        backgroundColor: theme.palette.background.paper
    }
}))

export function LoadingScreen(props) {
    const progress = props.progress ? props.progress : 0
    const fade = props.fade ? props.fade : true
    const classes = useStyles(props)

    return (
        <Grid
            container
            justifyContent='center'
            alignItems='center'
            className={classes.root}
        >
            <Grid item xs={11}>
                <Fade in={fade}>
                    <LinearProgress variant="buffer" value={progress} valueBuffer={0}/>
                </Fade>
            </Grid>
        </Grid>
    )
}
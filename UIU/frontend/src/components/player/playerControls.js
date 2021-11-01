import { Grid, IconButton } from "@material-ui/core"
import PauseCircleFilled from "@material-ui/icons/PauseCircleFilled"
import PlayCircleFilled from "@material-ui/icons/PlayCircleFilled"
import SkipPrevious from "@material-ui/icons/SkipPrevious"
import { makeStyles } from '@material-ui/core/styles';
import SkipNext from "@material-ui/icons/SkipNext";

const useStyles = makeStyles((theme) => ({
    button: {
        fontSize: "72px",
        margin: "6px",
    }
}))

export function PlayerControls(props) {
    const classes = useStyles(props)
    const playing = props.playing ? props.playing : false
    const onClick = props.onClick ? props.onClick : (c) => {} 
    const disabled = props.disabled ? props.disabled : false

    const handleOnPrevious = (e) => {
        onClick("previous")
    }

    const handleOnNext = (e) => {
        onClick("next")
    }

    const handlePausePlay = (e) => {
        if (playing) {
            onClick("pause")
        } else {
            onClick("play")
        }
    }

    return (
        <Grid container justifyContent="center">
            <Grid item>
                <IconButton size="medium" onClick={handleOnPrevious} disabled={disabled}>
                    <SkipPrevious className={classes.button} />
                </IconButton>
            </Grid>
            <Grid item>
                <IconButton size="medium" onClick={handlePausePlay} disabled={disabled}>
                    {
                        playing ? <PauseCircleFilled className={classes.button} /> : <PlayCircleFilled className={classes.button} />
                    }
                </IconButton>
            </Grid>
            <Grid item>
                <IconButton size="medium" onClick={handleOnNext} disabled={disabled}>
                    <SkipNext className={classes.button} />
                </IconButton>
            </Grid>
        </Grid>
    )
}
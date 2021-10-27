import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import { Paper, Typography } from '@material-ui/core';
import LibraryMusicIcon from '@material-ui/icons/LibraryMusic';
import { makeStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';
import PlayCircleFilledIcon from '@material-ui/icons/PlayCircleFilled';
import PauseCircleFilledIcon from '@material-ui/icons/PauseCircleFilled';
import IconButton from '@material-ui/core/IconButton';
import SkipNextIcon from '@material-ui/icons/SkipNext';
import SkipPreviousIcon from '@material-ui/icons/SkipPrevious';
import Box from '@material-ui/core/Box';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import { hasAudioSrc } from '../bluetooth/bluetoothTools';

const useStyles = makeStyles({
    songImg: {
        height: "17vw",
        width: "17vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
    controlsContainer: {
        display: "flex",
        justifyContent: "center",
        alignContent: "center"
    },
    controls: {
        fontSize: "72px",
        margin: "6px",
    },
    deviceSelect: {
        alignSelf: "center",
        position: "absolute",
        left: 0
    }
})

function millisToMinutesAndSeconds(millis) {
    var minutes = Math.floor(millis / 60000);
    var seconds = ((millis % 60000) / 1000).toFixed(0);
    return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
}

export function Player() {
    const classes = useStyles()
    const [track, setTrack] = React.useState()
    const [position, setPosition] = React.useState(0)
    const [status, setStatus] = React.useState("paused")

    const [current, setCurrent] = React.useState()
    const [connected, setConnected] = React.useState([])

    const [updater, setUpdater] = React.useState()
    const [slowUpdater, setSlowUpdater] = React.useState()

    const [message, setMessage] = React.useState("")

    useEffect(() => {
        window.uiu.api.bl_current().then(r => {
            console.log(r);
            setCurrent(r.device == null ? false : r.device)

            if (r.device === null) {
                window.uiu.api.bl_devices().then(result => {
                    for (const device of result.devices) {
                        if (device.Connected === 1) {
                            window.uiu.api.bl_enable_audio(device.Address).then(() => { })
                            setCurrent(device)
                            return
                        }
                    }
                })
            }
        })

        const slowUpdate = () => {
            window.uiu.api.bl_devices().then(result => {
                var arr = []
                for (const device of result.devices) {
                    if (device.Paired === 1 && hasAudioSrc(device)) {
                        arr.push(device)
                    }/*  else if (device.Paired === 1) {
                        arr.push(device)
                        window.uiu.api.bl_connect(device.Address).then(r => {

                            if (r.device !== null) {
                                var arr = [...connected]
                                arr.push(r.device)
                                setConnected(arr)
                            }
                        })
                    } */
                }
                setConnected(arr)
            })
        }

        slowUpdate();

        clearTimeout(updater)
        clearInterval(slowUpdater)

        setSlowUpdater(setInterval(slowUpdate, 10000))

        const fastUpdate = () => {
            clearTimeout(updater)
            
            window.uiu.api.bl_current().then(r => {
                setCurrent(r.device == null ? false : r.device)
                r.device = r.device == null ? false : r.device

                if (r.device) {
                    window.uiu.api.bl_status().then(r => {
                        setStatus(r.status)
                        setTrack(r.track)
                        setPosition(r.position)

                        setUpdater(setTimeout(fastUpdate, 500))
                    })
                } else {
                    setUpdater(setTimeout(fastUpdate, 500))
                }
            })
        }

        fastUpdate()

        return () => {
            clearTimeout(updater)
            clearInterval(slowUpdater)
        }
    }, [])

    const onPause = () => {
        window.uiu.api.bl_pause().then(() => {
            setStatus("paused")
        })
    }

    const onPlay = () => {
        window.uiu.api.bl_play().then(() => {
            setStatus("playing")
        })
    }

    const onPrevious = () => {
        window.uiu.api.bl_previous().then(() => { })
    }

    const onNext = () => {
        window.uiu.api.bl_next().then(() => { })
    }

    const onSetDevice = (e) => {
        console.log(e)

        if (e.target.value === 0) {
            window.uiu.api.bl_disable_audio().then(() => {
                setCurrent(false)
                setMessage("Disconnected")
            })
        } else {
            setMessage("Connecting...")

            window.uiu.api.bl_disable_audio().then(() => {
                setCurrent(false)
                setStatus("paused")
                setTrack({})

                window.uiu.api.bl_connect(e.target.value).then(r => {

                    if (r.device !== null) {
                        window.uiu.api.bl_enable_audio(e.target.value).then(() => {
                            onPlay()
                            window.uiu.api.bl_current().then(r => {
                                setMessage("")
                                setCurrent(r.device)
                            })
                        })
                    } else {
                        setMessage("Failed to connect!")
                    }
                })
            })
        }
    }

    return (
        <Grid container spacing={3}>
            <Grid item xs={4}>
                <Paper className={classes.songImg}>
                    <LibraryMusicIcon fontSize="large" />
                </Paper>
            </Grid>
            <Grid item xs={8}>
                <Typography variant="h5">{track && track.Title ? track.Title : "Onbekend"}</Typography>
                <Typography variant="caption">{track && track.Artist ? track.Artist : "Onbekend"}</Typography>
                <Typography variant="h5">{message}</Typography>
            </Grid>
            <Grid item xs={12}>
                <Box display="flex" alignItems="center">
                    <Box minWidth={35}>
                        <Typography variant="body2">{millisToMinutesAndSeconds(position)}</Typography>
                    </Box>
                    <Box width="100%" mr={1}>
                        <LinearProgress variant="determinate" value={track ? (position / track.Duration) * 100 : 0} />
                    </Box>
                    <Box minWidth={35}>
                        <Typography variant="body2">{millisToMinutesAndSeconds(track ? track.Duration : 0)}</Typography>
                    </Box>
                </Box>
            </Grid>
            <Grid item xs={12} className={classes.controlsContainer}>
                <Select value={current ? current.Address : 0} className={classes.deviceSelect} onChange={onSetDevice} disabled={message == "Connecting..."} color="secondary">
                    <MenuItem key={999} value={0}>uitschakelen</MenuItem>
                    {
                        connected.map((device, i) => {
                            return <MenuItem key={i} value={device.Address}>{device.Name}</MenuItem>
                        })
                    }
                </Select>
                <IconButton size="medium" onClick={e => onPrevious()}>
                    <SkipPreviousIcon className={classes.controls} />
                </IconButton>
                {
                    status === "playing" ?
                        <IconButton size="medium" onClick={e => onPause()}>
                            <PauseCircleFilledIcon className={classes.controls} />
                        </IconButton>
                        :
                        <IconButton size="medium" onClick={e => onPlay()}>
                            <PlayCircleFilledIcon className={classes.controls} />
                        </IconButton>
                }
                <IconButton size="medium" onClick={e => onNext()}>
                    <SkipNextIcon className={classes.controls} />
                </IconButton>
            </Grid>
        </Grid>
    )
}
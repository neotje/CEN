// TODO: bluetooth player rework

import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import { Paper, Typography } from '@material-ui/core';
import LibraryMusicIcon from '@material-ui/icons/LibraryMusic';
import { makeStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';
import Box from '@material-ui/core/Box';
import { hasAudioSrc } from '../bluetooth/bluetoothTools';
import { PlayerControls } from './playerControls';
import { DeviceSelector } from './deviceSelector';

const useStyles = makeStyles((theme) => ({
    songImg: {
        height: "17vw",
        width: "17vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
    trackInfo: {
        color: theme.palette.text.primary
    },
    trackProgress: {
        color: theme.palette.text.primary
    },
    controlsContainer: {
        display: "flex",
        justifyContent: "center",
        alignContent: "center"
    },
}))

function millisToMinutesAndSeconds(millis) {
    var minutes = Math.floor(millis / 60000);
    var seconds = ((millis % 60000) / 1000).toFixed(0);
    return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
}

export function Player(props) {
    const classes = useStyles(props)
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
                        if (device.Connected) {
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
                    if (device.Paired && hasAudioSrc(device)) {
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
                        setMessage("")

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

    const execControlCommand = (cmd) => {
        switch (cmd) {
            case "pause":
                window.uiu.api.bl_pause().then(() => {
                    setStatus("paused")
                })
                break;

            case "play":
                window.uiu.api.bl_play().then(() => {
                    setStatus("playing")
                })
                break;

            case "next":
                window.uiu.api.bl_next().then(() => { })
                break;

            case "previous":
                window.uiu.api.bl_previous().then(() => { })
                break;

            default:
                break;
        }
    }

    const changeDevice = (deviceAddress) => {
        if (!deviceAddress) {
            window.uiu.api.bl_disable_audio().then(() => {
                reset();
            })
        } else {
            setMessage("Connecting...")

            window.uiu.api.bl_disable_audio().then(() => {
                setCurrent(false)
                setStatus("paused")
                setTrack({})

                window.uiu.api.bl_connect(deviceAddress).then(r => {

                    if (r.device !== null) {
                        window.uiu.api.bl_enable_audio(deviceAddress).then(() => {
                            execControlCommand("play")
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

    const reset = () => {
        setCurrent(false)
        setMessage("Disconnected")
        setStatus("paused")
        setTrack({
            Duration: 0
        })
        setPosition(0)
    }

    return (
        <Grid container spacing={3}>
            <Grid item xs={4}>
                <Paper className={classes.songImg}>
                    <LibraryMusicIcon fontSize="large" />
                </Paper>
            </Grid>
            <Grid item xs={8} className={classes.trackInfo}>
                <Typography variant="h5">{track && track.Title ? track.Title : "Onbekend"}</Typography>
                <Typography variant="subtitle1">{track && track.Artist ? track.Artist : "Onbekend"}</Typography>
                <Typography variant="h5">{message}</Typography>
            </Grid>
            <Grid item xs={12}>
                <Box display="flex" alignItems="center" className={classes.trackProgress}>
                    <Box minWidth={35}>
                        <Typography variant="body2">{millisToMinutesAndSeconds(position)}</Typography>
                    </Box>
                    <Box width="100%" mr={1}>
                        <LinearProgress variant="determinate" value={track && track.Duration > 0 ? (position / track.Duration) * 100 : 0} />
                    </Box>
                    <Box minWidth={35}>
                        <Typography variant="body2">{millisToMinutesAndSeconds(track ? track.Duration : 0)}</Typography>
                    </Box>
                </Box>
            </Grid>
            <Grid item xs={12} className={classes.controlsContainer}>
                <DeviceSelector devices={connected} current={current} onChange={changeDevice} disabled={message === "Connecting..."} />
                <PlayerControls playing={status === "playing"} onClick={execControlCommand} disabled={message === "Connecting..." || message === "Disconnected"} />
            </Grid>
        </Grid>
    )
}
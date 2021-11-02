import React, { useEffect } from 'react';
import Container from '@material-ui/core/Container';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import SwipeableViews from 'react-swipeable-views';
import Box from '@material-ui/core/Box';
import { makeStyles } from '@material-ui/core/styles';

import './App.css';
import { Player } from './components/player/player';
import { BluetoothPage } from './components/bluetooth/bluetoothPage'
import { CustomThemeContext } from './components/theme/customThemeProvider';
import { Fade, Grid, LinearProgress } from '@material-ui/core';
import { NavigationBar } from './components/navigation/navigationBar';
import MusicNote from '@material-ui/icons/MusicNote';
import Bluetooth from '@material-ui/icons/Bluetooth';


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          {children}
        </Box>
      )}
    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    backgroundColor: theme.palette.background.paper
  },
  views: {
    flexGrow: 1,
    padding: theme.spacing(0, 4)
  },
  loadingContainer: {
    height: "100vh",
    backgroundColor: theme.palette.background.paper
  }
}))

function App(props) {
  const classes = useStyles(props);
  const [navValue, setNavValue] = React.useState(0);
  const [pyReady, setPyReady] = React.useState(window.uiu._ready);
  const [progress, setProgress] = React.useState(0);
  const [done, setDone] = React.useState(false);
  const [fade, setFade] = React.useState(true);
  const { currentTheme, setTheme } = React.useContext(CustomThemeContext)

  const handleNavigation = (newValue) => {
    if (newValue === 0) {
      window.uiu.api.bl_adapter_discovery(false).then(() => { })
    }
    setNavValue(newValue);
  }

  const handleThemeToggle = () => {
    setTheme(currentTheme === "light" ? "dark" : "light")
  }

  useEffect(() => {
    window.addEventListener('uiuready', () => {
      setPyReady(true)
      finalizeLoad()
    })

    if (pyReady) {
      finalizeLoad()
    }
  }, [pyReady])

  const finalizeLoad = () => {
    setProgress(33)

    window.uiu.api.settings_get("theme").then(result => {
      console.log(result.value)
      setTheme(result.value)
    })

    window.uiu.api.bl_adapter_discoverable(true).then(() => {
      setProgress(66)

      window.uiu.api.bl_adapter_discovery(false).then(() => {
        setProgress(100)

        setTimeout(() => {
          setFade(false);
        }, 500)
        setTimeout(() => {
          setDone(true)
        }, 1000)
        
      })
    })
  }

  if (!done) {
    return (
      <Grid container justifyContent='center' alignItems='center' className={classes.loadingContainer}>
        <Grid item xs={12}>
          <Fade in={fade}>
            <LinearProgress variant='buffer' value={progress} valueBuffer={0}/>
          </Fade>
        </Grid>
      </Grid>

    )
  }
  return (
    <Container className={classes.root} disableGutters>
      {/* <Fade in={true} appear={true}> */}
        <SwipeableViews
          index={navValue}
          className={classes.views}
          onChangeIndex={handleNavigation}>

          <TabPanel value={navValue} index={0}>
            <Player></Player>
          </TabPanel>

          <TabPanel value={navValue} index={1}>
            <BluetoothPage></BluetoothPage>
          </TabPanel>

        </SwipeableViews>

        <NavigationBar value={navValue} onNavigation={handleNavigation} theme={currentTheme} onTheme={handleThemeToggle}>
          <BottomNavigationAction label="Muziek" value={0} icon={<MusicNote />} />
          <BottomNavigationAction label="Bluetooth" value={1} icon={<Bluetooth />} />
        </NavigationBar>

      {/* </Fade> */}
    </Container>
  );
}

export default App;

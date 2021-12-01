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
import { NavigationBar } from './components/navigation/navigationBar';
import MusicNote from '@material-ui/icons/MusicNote';
import Bluetooth from '@material-ui/icons/Bluetooth';
import SettingsIcon from '@material-ui/icons/Settings';
import { LoadingScreen } from './components/loading/loadingScreen';
import { SettingsPage } from './components/settings/settingsPage';
import frontLed from './components/api/frontled';
import { ApiSocketContext } from './components/api/apiSocket';
import { Clock } from './components/clock';
import { Pulldown } from './components/pulldownMenu/pulldown';
import { Paper } from '@material-ui/core';
import LocalParkingIcon from '@material-ui/icons/LocalParking';
import { Camera } from './components/camera';

function TabPanel(props) {
  const { children, value, index, p, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
      style={{
        height: "100%"
      }}
    >
      {value === index && (
        <Box p={p} height="100%">
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
    backgroundColor: theme.palette.background.default
  },
  views: {
    flexGrow: 1,
    height: "100%"
  },
  topbar: {
    backgroundColor: theme.palette.background.paper
  }
}))

function App(props) {
  const classes = useStyles(props);
  const [navValue, setNavValue] = React.useState(0);
  const [progress, setProgress] = React.useState(0);
  const [done, setDone] = React.useState(false);
  const [fade, setFade] = React.useState(true);
  const { currentTheme, setTheme } = React.useContext(CustomThemeContext)

  const { api } = React.useContext(ApiSocketContext)
  const [pyReady, setPyReady] = React.useState(api.ready);

  const handleNavigation = (newValue) => {
    if (newValue === 0) {
      api.bl_adapter_discovery(false).then(() => { })
    }
    setNavValue(newValue);
  }

  useEffect(() => {
    api.onReady(result => {
      setPyReady(result)

      if (result) {
        finalizeLoad()
      }
    })

    api.connect()
  }, [])

  const finalizeLoad = () => {
    const steps = 5
    setProgress(100 / steps * 1)

    api.settings_get("theme")
      .then(result => {
        console.log(result.value)
        setTheme(result.value)

        setProgress(100 / steps * 2)
        return api.bl_adapter_discoverable(true)
      })
      .then(() => {

        setProgress(100 / steps * 3)
        return api.bl_adapter_discovery(false)
      })
      .then(() => {

        setProgress(100 / steps * 4)
        return frontLed.setup(api)
      })
      .then(() => {

        setProgress(100 / steps * 5)
        setTimeout(() => {
          setFade(false);
        }, 500)
        setTimeout(() => {
          setDone(true)
        }, 1000)

      })
  }

  if (!done) {
    return (
      <LoadingScreen progress={progress} fade={fade} />
    )
  }
  return (
    <Container className={classes.root} disableGutters>
      {/* <Fade in={true} appear={true}> */}
      
      <Paper square elevation={2}>
        <Clock />
      </Paper>
      
      <Pulldown />

      <SwipeableViews
        index={navValue}
        className={classes.views}
        onChangeIndex={handleNavigation}
        disableLazyLoading={true}
        resistance={true}
        disabled={navValue === 3}
        slideStyle={{
          height: "100%"
        }}
        containerStyle={{
          height: "100%"
        }}
      >

        <TabPanel value={navValue} index={0} p={3}>
          <Player />
        </TabPanel>

        <TabPanel value={navValue} index={1} p={3}>
          <BluetoothPage />
        </TabPanel>

        <TabPanel value={navValue} index={2}>
          <Camera />
        </TabPanel>

        <TabPanel value={navValue} index={3} p={3}>
          <SettingsPage />
        </TabPanel>

      </SwipeableViews>

      <NavigationBar value={navValue} onNavigation={handleNavigation}>
        <BottomNavigationAction label="Muziek" value={0} icon={<MusicNote />} />
        <BottomNavigationAction label="Bluetooth" value={1} icon={<Bluetooth />} />
        <BottomNavigationAction label="Parkeren" value={2} icon={<LocalParkingIcon />} />
        <BottomNavigationAction label="Instellingen" value={3} icon={<SettingsIcon />} />
      </NavigationBar>

      {/* </Fade> */}
    </Container>
  );
}

export default App;

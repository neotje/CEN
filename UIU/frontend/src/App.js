import React, { useEffect } from 'react';
import Container from '@material-ui/core/Container';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import SwipeableViews from 'react-swipeable-views';
import Box from '@material-ui/core/Box';
import { makeStyles } from '@material-ui/core/styles';
import MusicNoteIcon from '@material-ui/icons/MusicNote';
import BluetoothIcon from '@material-ui/icons/Bluetooth';

import './App.css';
import { Player } from './components/player/player';
import { BluetoothPage } from './components/bluetooth/bluetoothPage'
import { CustomThemeContext } from './components/theme/customThemeProvider';
import { Switch } from '@material-ui/core';
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
  }
}))

function App(props) {
  const classes = useStyles(props);
  const [navValue, setNavValue] = React.useState(0);
  const [pyReady, setPyReady] = React.useState(window.uiu._ready);
  const { currentTheme, setTheme } = React.useContext(CustomThemeContext)

  const handleNavigation = (newValue) => {
    if (newValue === 0) {
      window.uiu.api.bl_adapter_discovery(false).then(() => { })
    }
    setNavValue(newValue);
  }

  const handleThemeToggle = () => {
    setTheme(currentTheme == "light" ? "dark" : "light")
  }

  useEffect(() => {
    window.addEventListener('uiuready', () => {
      setPyReady(true)
    })

    if (pyReady) {
      window.uiu.api.bl_adapter_discoverable(true).then(() => {
        window.uiu.api.bl_adapter_discovery(false).then(() => { })
      })
    }
  }, [])

  if (!pyReady) {
    return (
      <div>loading...</div>
    )
  }
  return (
    <Container className={classes.root} disableGutters>
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

    </Container>
  );
}

export default App;

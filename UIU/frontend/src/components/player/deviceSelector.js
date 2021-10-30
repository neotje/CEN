import { MenuItem, Select } from "@material-ui/core"
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles({
    root: {
        alignSelf: "center",
        position: "absolute",
        left: 0
    }
})

export function DeviceSelector(props) {
    const classes = useStyles()

    const devices = props.devices ? props.devices : []
    const current = props.current && devices.length > 0 ? props.current : { Address: 0 }
    const onChange = props.onChange ? props.onChange : (v) => { }
    const disabled = props.disabled ? props.disabled : false

    const handleOnChange = (e) => {
        const deviceAddress = e.target.value

        if (deviceAddress === 0) {
            onChange(false)
        } else {
            onChange(deviceAddress)
        }
    }

    return (
        <Select className={classes.root} value={current.Address} onChange={handleOnChange} disabled={disabled}>
            <MenuItem key={999} value={0}>uitschakelen</MenuItem>
            {
                devices.map((device, i) => {
                    return <MenuItem key={i} value={device.Address}>{device.Name}</MenuItem>
                })
            }
        </Select>
    )
}

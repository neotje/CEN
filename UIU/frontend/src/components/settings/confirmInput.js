import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@material-ui/core"

export function ConfirmInput(props) {
    let { title, body, open, onClick } = props

    open = open ? open : false
    onClick = onClick ? onClick : (confirmed) => { }

    const handleCancel = (e) => {
        onClick(false)
    }

    const handleConfirm = (e) => {
        onClick(true)
    }

    return (
        <Dialog open={open} onClose={handleCancel}>
            <DialogTitle> {title} </DialogTitle>
            <DialogContent>
                <DialogContentText>
                    {body}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button autoFocus onClick={handleCancel} color="secondary">Nee</Button>
                <Button onClick={handleConfirm} color="primary">Ja</Button>
            </DialogActions>
        </Dialog>
    )
}
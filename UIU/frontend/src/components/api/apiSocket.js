import React from "react"

const ON_API_CONNECTED = "onApiConnected"
const ON_API_READY = "onApiReady"
const ON_API_RETURN = "onApiReturn"
const DEFAULT_ADDRESS = "ws://127.0.0.1:2888"

export class ApiSocket {
    /** @type {WebSocket} */
    _socket = undefined
    /** @type {string} */
    _address = undefined

    /**
     * @param {boolean} detail 
     * @returns {Event}
     */
    _connectedEvent(detail) {
        return new CustomEvent(ON_API_CONNECTED, { detail })
    }

    /**
     * @param {boolean} detail 
     * @returns {Event}
     */
    _readyEvent(detail) {
        return new CustomEvent(ON_API_READY, { detail })
    }

    /**
     * @param {object} detail 
     * @returns {Event}
     */
    _returnEvent(detail) {
        return new CustomEvent(ON_API_RETURN, { detail })
    }

    _connected = false
    _ready = false

    get ready() {
        return this._ready
    }

    reconnect = true

    _returnValues = {}
    api = {}

    /**
     * @constructor
     * @param {string} address
     */
    constructor(address = DEFAULT_ADDRESS) {
        this._address = address
    }

    connect() {
        if (this.ready) {return}
        console.log("Api socket trying to connect to:", this._address)
        this._socket = new WebSocket(this._address)

        this._socket.addEventListener("open", (e) => {
            this._onopen(e)
        })
        this._socket.addEventListener("close", (e) => {
            this._onclose(e)
        })
        this._socket.addEventListener("error", (e) => {
            this._onerror(e)
        })
        this._socket.addEventListener("message", (e) => {
            this._onmessage(e)
        })
    }

    /**
     * @param {EventListenerOrEventListenerObject} listener 
     */
    onConnected(listener) {
        window.addEventListener(ON_API_CONNECTED, listener, false)
    }

    /**
     * @param {EventListenerOrEventListenerObject} listener 
     */
    onReady(listener) {
        window.addEventListener(ON_API_READY, listener, false)
    }

    /**
     * 
     * @param {string} name 
     * @param {Array<string>} params 
     */
    _expose(name, params) {
        console.debug("Api socket exposing:", name)
        const body = `
            const __id = (Math.random() + '').substring(2);
            var promise = new Promise((resolve, reject) => {
              this._checkValue("${name}", __id, resolve, reject);
            });
            this._call("${name}", arguments, __id);
            return promise
            `

        this[name] = new Function(params, body)
        this._returnValues[name] = {}
    }

    /**
     * @param {string} funcName Function name to call
     * @param {object} params 
     * @param {string} id 
     */
    _call(funcName, params, id) {
        console.debug("Api Socket calling: ", funcName);

        if (!this._ready) {
            throw new Error("Api Socket is not ready!")
        }

        this._socket.send(JSON.stringify({
            action: "call",
            id,
            function: funcName,
            params
        }))
    }

    _checkValue(funcName, id, resolve, reject) {
        window.addEventListener(ON_API_RETURN, (e) => {
            var detail = e.detail;

            // on api return event and funcName and id are the same
            // then resolve promise
            if (detail.function === funcName && detail.id === id) {
                if (detail.isError) {
                    var pyError = detail.content;
                    var error = new Error(pyError.message);

                    error.name = pyError.name;
                    error.stack = pyError.stack;
                    console.error(error);

                    window.removeEventListener(ON_API_RETURN, this)
                    resolve(error);
                } else {
                    resolve(detail.content);
                }
            }
        })
    }

    _onopen(e) {
        this._connected = true
        window.dispatchEvent(this._connectedEvent(this._connected))
    }

    /**
     * @param {MessageEvent} e 
     */
    _onmessage(e) {
        var content = JSON.parse(e.data)

        switch (content.action) {
            case "expose":
                this._expose(content.name, content.params)
                break;

            case "return":
                console.debug("Api socket got return action:", content.function)
                window.dispatchEvent(this._returnEvent(content))
                break;

            case "ready":
                console.log("Api socket is ready")
                this._ready = true
                window.dispatchEvent(this._readyEvent(this._ready))
                break

            default:
                break
        }
    }

    /**
     * When socket is close try to reconnect if this.reconnect is true
     * @param {CloseEvent} e 
     */
    _onclose(e) {
        console.log("Api socket closed")
        this._connected = false
        this._ready = false

        window.dispatchEvent(this._connectedEvent(this._connected))
        window.dispatchEvent(this._readyEvent(this._ready))

        if (this.reconnect) {
            setTimeout(this.connect, 1000)
        }
    }

    _onerror(e) {
        console.error('Api socket encountered error: ', e.message, 'Closing socket');
        this._socket.close()
    }
}

export const ApiSocketContext = React.createContext({
    api: new ApiSocket
})

export function ApiSocketProvider(props) {
    const { children } = props

    const address = props.address ? props.address : DEFAULT_ADDRESS
    const socket = new ApiSocket(address)

    const contextValue = {
        api: socket
    }

    return (
        <ApiSocketContext.Provider value={contextValue}>
            {children}
        </ApiSocketContext.Provider>
    )
}
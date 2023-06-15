// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
let client = null

/**
 * this demo uses EMQX Public MQTT Broker (https://www.emqx.com/en/mqtt/public-mqtt5-broker), here are the details:
 *
 * Broker host: broker.emqx.io
 * TCP Port: 1883
 * SSL/TLS Port: 8883
 * WebSocket port: 8083
 * WebSocket over TLS/SSL port: 8084
 */

const options = {
  keepalive: 30,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  connectTimeout: 30 * 1000, // ms
  reconnectPeriod: 4000, // ms
  // for more options, please refer to https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options
}

let currentHeart = 0;



//  protocol->port    mqtt: 1883; mqtts: 8883; ws: 8083; wss: 8084
function onProtocolChange() {
  switch (connection.protocol.value) {
    case 'mqtt':
      connection.port.value = 1883
      pathIpt.style.display = 'none'
      fileArea.style.display = 'none'
      break
    case 'mqtts':
      connection.port.value = 8883
      pathIpt.style.display = 'none'
      fileArea.style.display = 'block'
      break
    case 'ws':
      connection.port.value = 8083
      pathIpt.style.display = 'block'
      fileArea.style.display = 'none'
      break
    case 'wss':
      connection.port.value = 8084
      pathIpt.style.display = 'block'
      fileArea.style.display = 'block'
      break
    default:
      break
  }
}

// create MQTT connection
function onConnect() {

  // options.clientId =
  //   clientId.value ||
  //   `emqx_electron_${Math.random().toString(16).substring(2, 10)}`

  /**
   * By default, EMQX allows clients to connect without authentication.
   * https://docs.emqx.com/en/enterprise/v4.4/advanced/auth.html#anonymous-login
   */
  console.log('connecting mqtt client')

  /**
   * if protocol is "mqtt", connectUrl = "mqtt://broker.emqx.io:1883"
   * if protocol is "mqtts", connectUrl = "mqtts://broker.emqx.io:8883"
   * if protocol is "ws", connectUrl = "ws://broker.emqx.io:8083/mqtt"
   * if protocol is "wss", connectUrl = "wss://broker.emqx.io:8084/mqtt"
   *
   * /mqtt: MQTT-WebSocket uniformly uses /path as the connection path,
   * which should be specified when connecting, and the path used on EMQX is /mqtt.
   *
   * Note: Here we use the mqtts or wss protocol with TLS one-way authentication,
   * which only verifies the server's certificate and does not verify the client's certificate.
   * If you require two-way authentication, please use TLS two-way authentication.
   *
   * for more details about "mqtt.connect" method & options,
   * please refer to https://github.com/mqttjs/MQTT.js#mqttconnecturl-options
   */
  client = mqtt.connect("mqtt://192.168.0.150:1883", options)

  // https://github.com/mqttjs/MQTT.js#event-connect
  client.on('connect', () => {
    console.log("Connected to broker")
    client.subscribe("bpm")
  })

  // https://github.com/mqttjs/MQTT.js#event-reconnect
  client.on('reconnect', () => {
    console.log('Reconnecting...')
  })

  // https://github.com/mqttjs/MQTT.js#event-error
  client.on('error', (err) => {
    console.error('Connection error: ', err)
    client.end()
  })

  // https://github.com/mqttjs/MQTT.js#event-message
  client.on('message', (topic, message) => {
    console.log(message.toString())
    const txt = document.getElementById("val")
    txt.innerHTML = message.toString()
    const im = document.getElementById("Cont1")
    const msgNum = parseInt(message.toString())
    if(msgNum >= currentHeart + 10) {
      currentHeart = msgNum
      document.getElementById("Cont1").style.animationDuration = 60/msgNum + "s"
    } else if(msgNum <= currentHeart - 10) {
      currentHeart = msgNum
      document.getElementById("Cont1").style.animationDuration = 60/msgNum + "s"
    } 
  })
}



onConnect();
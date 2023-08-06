import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: countdown

//  When need to change timerFinishedText
    property alias finishedText: timerFinishedText

//  Width of the line
    property var lineWidth: 2
//  Initial time
    property var time: 600
//  Current time left
    property var timeLeft: time
//  Is timer ready
    property bool ready: true
//  Using this property can change the component according to the state
    property bool finished: false
//  Time in seconds, that was elapsed before timer started. Use this when timer was started in the past
    property int timeElapsedOnStart: 0
//  Is timer running
    readonly property bool running: timer.timeStart != null

//  Timer signal on finish
    signal timerFinished()

    onReadyChanged: canvas.position = ready ? 0 : 2 * Math.PI

//  Start the timer
    function start() {
        timerFinishedItem.visible = false
        canvas.position = 0
        timeLeft = time - timeElapsedOnStart
        timer.start()
    }

//  Stop the timer
    function stop() {
        timerFinishedItem.visible = false
        timer.stop()
        timer.timeStart = null
        canvas.position = 0
        timeLeft = time
    }

//  Show finish timer state
    function finish() {
        timerFinished()
        canvas.position = 2 * Math.PI
        timer.stop()
        timer.timeStart = null
        timerFinishedItem.visible = true
    }

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleTimeName: ""
    /* ---------------------------------------------------- */

    implicitWidth: 64
    implicitHeight: width

    Column {
        id: timeLeftItem

        anchors.centerIn: canvas

        visible: !timerFinishedItem.visible

        DS3.Text {
            anchors.horizontalCenter: parent.horizontalCenter

            text: {
                var min = Math.floor(timeLeft / 60)
                var sec = timeLeft % 60
                return min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
            }
            style: ui.ds3.text.body.MRegular
            color: countdown.ready ? ui.ds3.figure.interactive : ui.ds3.figure.disabled

            /* ------------------------------------------------ */
            /* desktop tests */
            Accessible.name: countdown.accessibleTimeName
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ------------------------------------------------ */
        }
    }

    Column {
        id: timerFinishedItem

        anchors.centerIn: canvas

        spacing: 8
        visible: false

        onVisibleChanged: {
            if (visible) {
                timerFinishedAnimation.start()
                finished = true
            } else {
                finished = false
            }
        }

        ParallelAnimation {
            id: timerFinishedAnimation

            NumberAnimation { target: timerFinishedText; property: "opacity"; from: 0; to: 1; duration: 300 }
        }

        DS3.Text {
            id: timerFinishedText

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.positiveContrast
            text: tr.ok
        }
    }

    Timer {
        id: timer

        property var timeStart: null

        interval: 100
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            if (!timeStart) {
                timeStart = Date.now() - timeElapsedOnStart * 1000
            } else {
                let timeElapsed = (Date.now() - timeStart) / 1000
                if (timeElapsed >= time) {
                    timeLeft = 0
                }
                else {
                    timeLeft = Math.ceil(time - timeElapsed)
                    canvas.position = 2 * Math.PI * (Date.now() - timeStart) / 1000 / time
                }
            }
        }
    }

    Canvas {
        id: canvas

        readonly property int radius: canvas.width / 2
        property double position: countdown.ready ? 0 : 2 * Math.PI

        onPositionChanged: canvas.requestPaint()

        width: parent.width
        height: width

        antialiasing: true
        rotation: -90

        Behavior on position {
            NumberAnimation {
                duration: timer.timeStart == null ? 500 : 100
            }
        }

        onPaint: {
            var centreX = canvas.width / 2.0
            var centreY = canvas.height / 2.0

            var ctx = canvas.getContext('2d')
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            ctx.lineWidth = lineWidth

            ctx.beginPath()
            ctx.strokeStyle = ui.colors.interactive
            ctx.arc(centreX, centreY, radius - ctx.lineWidth / 2, 2 * Math.PI, position, true)
            ctx.stroke()

            ctx.beginPath()
            ctx.strokeStyle = finished ? ui.ds3.figure.positiveContrast : ui.colors.disabled
            ctx.arc(centreX, centreY, radius - ctx.lineWidth / 2, position, 0, true)
            ctx.stroke()
        }
    }
}

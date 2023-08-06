import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: countdown

//  When need to change timerFinishedText
    property alias finishedText: timerFinishedText.text
//  Width of the line
    property var lineWidth: 4
//  Initial time
    property var time: 600
//  Current time left
    property var timeLeft: time
//  Is timer ready
    property bool ready: true
//  Using this property can change the component according to the state
    property bool finished: false
//  If true, the timer should get finished status after time is over. Otherwise, the timer will just stop
    property bool autoFinish: true
//  Is timer running
    readonly property bool running: timer.timeStart != null

    onReadyChanged: canvas.position = ready ? 0 : 2 * Math.PI

//  Start the timer
    function start() {
        if (!running) {
            timerFinishedItem.visible = false
            canvas.position = 0
            timeLeft = time
            timer.start()
            finished = false
        }
    }

//  Stop the timer
    function stop() {
        timerFinishedItem.visible = false
        timer.stop()
        timer.timeStart = null
        canvas.position = 0
        timeLeft = time
        finished = false
    }

//  Show finish timer state
    function finish() {
        canvas.position = 2 * Math.PI
        timer.stop()
        timer.timeStart = null
        timerFinishedItem.visible = true
        finished = true
    }

    implicitWidth: 247
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
            style: ui.ds3.text.title.LBold
            color: countdown.ready ? ui.ds3.figure.interactive : ui.ds3.figure.disabled
        }

        DS3.Text {
            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.time_remaining
            color: countdown.ready ? ui.ds3.figure.secondary : ui.ds3.figure.disabled
            style: ui.ds3.text.body.MRegular
        }
    }

    Column {
        id: timerFinishedItem

        anchors.centerIn: canvas

        spacing: 8
        visible: false

        onVisibleChanged: {
            if (visible) timerFinishedAnimation.start()
        }

        ParallelAnimation {
            id: timerFinishedAnimation

            NumberAnimation { target: timerFinishedCircle; property: "scale"; from: 0; to: 1; duration: 300 }
            NumberAnimation { target: timerFinishedText; property: "opacity"; from: 0; to: 1; duration: 300 }
        }

        Rectangle {
            id: timerFinishedCircle

            width: 40
            height: 40

            anchors.horizontalCenter: parent.horizontalCenter

            radius: 20
            color: ui.ds3.figure.positiveContrast

            DS3.Icon {
                id: timerFinishedIcon

                anchors.centerIn: parent

                source: "qrc:/resources/images/Athena/common_icons/Check-M.svg"
                color: ui.ds3.figure.inverted
            }
        }

        DS3.Text {
            id: timerFinishedText

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            text: tr.signal_strength_ok
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
                timeStart = Date.now()
            } else {
                let timeElapsed = (Date.now() - timeStart) / 1000
                if (timeElapsed >= time) {
                    timeLeft = 0
                    if (autoFinish) {
                        countdown.finish()
                    } else {
                        timer.stop()
                        canvas.position = 2 * Math.PI
                    }
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
            ctx.strokeStyle = ui.colors.disabled
            ctx.arc(centreX, centreY, radius - ctx.lineWidth / 2, position, 0, true)
            ctx.stroke()
        }
    }
}

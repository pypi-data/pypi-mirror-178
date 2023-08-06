import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {

// Spinner size
    enum ImageSize {
        S,    // 16x16
        M,    // 24x24
        L     // 32x32
    }

    property var size: DS3.Spinner.ImageSize.L
//  Property need for pixel size
    readonly property int sizeInPixels: {
        switch (size) {
            case DS3.Spinner.ImageSize.S: 16;
            break;
            case DS3.Spinner.ImageSize.M: 24;
            break;
            case DS3.Spinner.ImageSize.L: 32;
            break;
        }
    }
    property alias finishedAnimation: finalAnimation

    function finalize() {
        finalAnimationTimer.start()
    }

    width: sizeInPixels
    height: sizeInPixels

    SequentialAnimation {
        id: finalAnimation

        running: false

        NumberAnimation { target: finishCircle; property: "border.width"; to: width / 2; duration: 300}
        NumberAnimation { target: checkMarkSource; property: "scale"; to: 1; duration: 200 }
    }

    Item {
        id: spinnerItem

        anchors.fill: parent

        property real arcBegin: 0            // start arc angle in degree
        property real arcEnd: 270            // end arc angle in degree
        property real lineWidth: 2          // width of the line

        onArcBeginChanged: canvas.requestPaint()
        onArcEndChanged: canvas.requestPaint()

        Canvas {
            id: canvas

            anchors.fill: parent

            onPaint: {
                var ctx = getContext("2d")
                var x = width / 2
                var y = height / 2
                var start = Math.PI * (parent.arcBegin / 180)
                var end = Math.PI * (parent.arcEnd / 180)
                ctx.reset();

                ctx.beginPath();
                ctx.arc(x, y, (width / 2) - parent.lineWidth / 2, end, start, false)
                ctx.lineWidth = spinnerItem.lineWidth
                ctx.strokeStyle = ui.ds3.figure.disabled
                ctx.stroke()
                ctx.beginPath();
                ctx.arc(x, y, (width / 2) - parent.lineWidth / 2, start, end, false)
                ctx.strokeStyle = ui.ds3.figure.interactive
                ctx.stroke()
            }
        }

        Timer {
            id: rotationTimer

            interval: 25
            repeat: true
            triggeredOnStart: true
            running: true

            onTriggered: {
                spinnerItem.rotation += 9
                if (spinnerItem.rotation == 360) spinnerItem.rotation = 0
            }
        }

        Timer {
            id: finalAnimationTimer

            interval: 25
            repeat: true

            onTriggered: {
                spinnerItem.arcEnd += 9
                if (spinnerItem.arcEnd == 360) {
                    rotationTimer.stop()
                    finalAnimationTimer.stop()
                    finalAnimation.start()
                }
            }
        }
    }

    Rectangle {
        id: finishCircle

        anchors.fill: parent

        color: ui.ds3.figure.transparent
        radius: parent.width
        border {
            color: ui.ds3.figure.interactive
            width: 0
        }
    }

    DS3.Image {
        id: checkMarkSource

        width: size == DS3.Spinner.ImageSize.L ? 16 : 12
        height: size == DS3.Spinner.ImageSize.L ? 16 : 12

        anchors.centerIn: parent

        scale: 0
        source: size == DS3.Spinner.ImageSize.L ?
            "qrc:/resources/images/Athena/spinner_icons/Check-S.svg" :
            "qrc:/resources/images/Athena/spinner_icons/Check-XS.svg"
    }
}

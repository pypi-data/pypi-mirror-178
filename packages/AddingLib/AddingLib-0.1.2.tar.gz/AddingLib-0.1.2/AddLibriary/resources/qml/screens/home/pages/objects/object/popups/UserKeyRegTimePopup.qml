import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 410

    modal: true
    focus: true

    closePolicy: Popup.NoAutoClose

    property int roomIndex: 0

    property int timerTime: 30
    property var text: ""

    function pad(num, size){ return ('000000000' + num).substr(-size); }

    Timer {
        id: regTimer
        running: false
        interval: 1000
        repeat: true
        onTriggered: {
            textCircle.text = "00:" +  pad(timerTime, 2)
            timerTime -= 1
            timeCircle.arcBegin += 12

            if (timerTime == 0) {
                regTimer.running = false
                return
            }
        }
    }

    Rectangle {
        width: 360
        height: 410
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxTimeCircle {
            id: timeCircle
            anchors {
                top: parent.top
                topMargin: 36
                horizontalCenter: parent.horizontalCenter
            }
            size: 180
            colorCircle: "#60e3ab"
            colorBackground: "#E6E6E6"
            arcBegin: 0
            arcEnd: 360
            lineWidth: 8
            showBackground: true
        }

        Text {
            id: textCircle
            font.family: roboto.name
            font.pixelSize: 24
            color: ui.colors.green1
            text: tr.waiting
            anchors.centerIn: timeCircle
        }

        Text {
            width: parent.width - 60
            id: textLabel
            font.family: roboto.name
            font.pixelSize: 12
            color: ui.colors.light1
            opacity: 0.9
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
            anchors.top: timeCircle.bottom
            anchors.topMargin: 32
            anchors.horizontalCenter: parent.horizontalCenter
            text: popup.text
        }

        MouseArea {
            id: cancelArea
            width: parent.width
            height: 48
            anchors.bottom: parent.bottom

            focus: true
            Keys.onEscapePressed: clicked(true)

            onClicked: {
                client.reg_key_cancel()
                popup.close()
            }

            Text {
                color: ui.colors.green1
                font.family: roboto.name
                font.pixelSize: 14
                anchors.centerIn: parent
                text: tr.cancel
            }

            Rectangle {
                width: parent.width
                height: 1
                color: ui.colors.light1
                opacity: 0.2
                anchors.top: parent.top
            }
        }
    }

    Connections {
        target: client
        onDeviceSearchClose: {
            popup.close()
        }

        onRegStartTimer: {
            regTimer.start()
        }

        onActionFailed: {
            popup.close()
        }
    }
}
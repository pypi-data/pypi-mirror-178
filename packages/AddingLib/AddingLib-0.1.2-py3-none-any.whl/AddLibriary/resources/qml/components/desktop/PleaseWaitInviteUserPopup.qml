import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 320
    height: 200

    modal: true
    focus: true

    closePolicy: Popup.NoAutoClose

    Rectangle {
        width: 320
        height: 200
        anchors.fill: parent
        color: "#070707"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.9

        SequentialAnimation {
            running: opened
            loops: Animation.Infinite
            NumberAnimation {
                target: logoIco;
                property: "anchors.verticalCenterOffset";
                to: -20;
                duration: 1000;
                easing.type: Easing.OutInQuart
            }
            NumberAnimation {
                target: logoIco;
                property: "anchors.verticalCenterOffset";
                to: 20;
                duration: 1000;
                easing.type: Easing.OutInQuart
            }
        }

        Column {
            anchors.fill: parent

            Item {
                width: parent.width
                height: 3

                Rectangle {
                    id: topLine
                    anchors.centerIn: parent
                    width: 0
                    height: 1
                }
            }

            Item {
                width: parent.width
                height: 120
                Image {
                    id: logoIco
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    source: "qrc:/resources/images/desktop/icons/ic-logo-firstscreen@2x.png"
                }
            }

            Item {
                width: parent.width
                height: 48

                Text {
                    text: tr.request_send
                    color: ui.colors.light1
                    font.family: roboto.name
                    font.pixelSize: 14
                    anchors.centerIn: parent
                }
            }
        }
    }
}
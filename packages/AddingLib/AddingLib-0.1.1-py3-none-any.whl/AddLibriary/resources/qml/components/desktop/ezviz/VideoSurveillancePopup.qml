import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 320
    height: 380

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        focus: true

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.video_surveillance
        }

        Column {
            id: column
            width: popup.width
            anchors {
                top: closeItem.bottom
                topMargin: 16
                bottom: actionItem.top
            }

            AjaxListItemNew {
                id: ezvizItem
                width: parent.width
                height: 56
                mainText: "Hikvision/Safire"
                miniText: ezviz.username

                mouseArea.onClicked: {
                    if (ezviz.username == "") {
                        Popups.ezviz_login_popup()
                    } else {
                        Popups.ezviz_popup()
                    }
                }
            }
        }

        Item {
            id: actionItem
            width: parent.width
            height: 48

            anchors.bottom: parent.bottom

            Rectangle {
                anchors.top: parent.top
                height: 1
                width: parent.width
                color: ui.colors.light1
                opacity: 0.1
            }

            Text {
                anchors.centerIn: parent
                text: tr.ok
                color: ui.colors.green1
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                width: parent.width
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    popup.close()
                }
            }
        }
    }
}

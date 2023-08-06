import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 320
    height: 340

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var roomIndex: null
    property var rooms

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        focus: true

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.add_camera
        }

        Column {
            id: column
            width: popup.width
            anchors {
                top: closeItem.bottom
                topMargin: 16
                bottom: parent.bottom
            }

            AjaxListItemNew {
                id: rtspItem
                width: parent.width
                height: 56
                mainText: "RTSP Camera"
                miniText: ""

                mouseArea.onClicked: {
                    popup.close()
                    addCameraPopup(roomIndex, rooms)
                }
            }

            AjaxListItemNew {
                id: hikvisionItem
                width: parent.width
                height: 56
                mainText: "Hikvision"
                miniText: ""  // ezviz.username

                enabled: false
                opacity: enabled ? 1 : 0.6

                mouseArea.onClicked: {
                    if (ezviz.username == "") {
                        Popups.ezviz_login_popup()
                        return
                    }
                    addHikvisionSafireCameraPopup(roomIndex, 2)
                }
            }

            AjaxListItemNew {
                id: safireItem
                width: parent.width
                height: 56
                mainText: "Safire"
                miniText: ""  // ezviz.username

                enabled: false
                opacity: enabled ? 1 : 0.6

                mouseArea.onClicked: {
                    if (ezviz.username == "") {
                        Popups.ezviz_login_popup()
                        return
                    }
                    addHikvisionSafireCameraPopup(roomIndex, 5)
                }
            }
        }
    }

    /*
    Connections {
        target: ezviz

        onEzvizActionSuccess: {
            popup.close()
        }
    }
    */
}

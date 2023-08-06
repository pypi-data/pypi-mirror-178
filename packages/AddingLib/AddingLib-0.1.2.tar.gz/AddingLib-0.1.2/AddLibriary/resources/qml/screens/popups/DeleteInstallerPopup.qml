import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: popup
    objectName: "deleteInstallerPopup"
    width: 360
    height: 120 + moveText.height

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape

    anchors.centerIn: parent

    property var settings: null
    property var mode: null
    property var reloadSignal: null
    property var insertData: null

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Custom.FontText {
            id: moveText
            text: popup.mode == "facility" ? util.insert(tr.delete_installer_from_object, ["", insertData.employee, insertData.facility]) : util.insert(tr.cancel_access_to_object, ["", insertData.employee, insertData.facility])
            width: parent.width - 64
            height: contentHeight
            color: ui.colors.light3
            font.pixelSize: 16
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft
            anchors {
                top: parent.top
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        Item {
            width: parent.width
            height: 80
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    right: parent.right
                }
            }

            Anime.SharinganLoader {
                id: anim
                radius: 13
                color: ui.colors.red1
                useCircle: true
                visible: !popup.enabled
                anchors.centerIn: parent
                anchors.verticalCenterOffset: -4
            }

            Item {
                width: 136
                height: 40
                visible: popup.enabled
                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.cancel
                    color: ui.colors.white
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.close()
                    }
                }
            }

            Item {
                width: 136
                height: 40
                visible: popup.enabled
                anchors {
                    right: parent.right
                    rightMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.delete
                    color: ui.colors.red1
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.enabled = false

                        app.installers_module.delete_facility_employee_permission(settings)
                    }
                }
            }
        }
    }

    Connections {
        target: app.installers_module

        onDeleteFacilityEmployeePermissionSuccess: {
            if (popup.reloadSignal) popup.reloadSignal()
            popup.close()
        }

        onDeleteFacilityEmployeePermissionFailed: {
            popup.close()
        }
    }
}

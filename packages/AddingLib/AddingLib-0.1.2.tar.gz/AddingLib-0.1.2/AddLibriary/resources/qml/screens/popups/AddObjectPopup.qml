import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "addObjectPopup"
    width: 384
    height: header.height + body.height + btnSaveItem.height + 48
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    signal reDashInsertResult(string new_text, int pos)

    property var connectionsAdd: false
    property var hubId: ""
    property var name: ""
    property var number: ""
    property var hubCompanyBindingState: ""

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        radius: 8
        color: ui.colors.dark3
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.a911_add_object
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors {
                    right: parent.right
                    bottom: parent.bottom
                }
            }
        }

        ColumnLayout {
            id: body
            width: parent.width - 64
            anchors{
                top: header.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8
            }

            Rectangle{
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8
            }

            Rectangle{
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8
            }
        }

        Item {
            id: btnSaveItem
            width: parent.width
            height: 88
            anchors {
                top: body.bottom
                topMargin: 24
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors.right: parent.right
            }

            Custom.Button {
                id: btnSave
                width: parent.width - 64
                text: tr.next
                enabledCustom: objectName.valueText.control.text != "" && objectNumber.valueText.control.text != ""
                anchors.centerIn: parent

                onClicked: {
                    var settings = {}
                    settings["binding_state"] = hubCompanyBindingState
                    settings["registration_number"] = objectNumber.valueText.control.text
                    settings["name"] = objectName.valueText.control.text
                    settings["hub_id"] = objectHubId.valueText.control.text

                    popup.enabled = false
                    loading = true

                    app.company_module.create_channel(settings)
                }
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
            btnSave.loading = false
            popup.enabled = true
        }
    }
}
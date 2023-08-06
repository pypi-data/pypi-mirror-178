import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import ajax.plugin.video 1.0

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3


AjaxPopup {
    id: popup
    objectName: "addAltObjectPopup"
    width: 384
    height: header.height + body.height + btnSaveItem.height + 48
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    signal reDashInsertResult(string new_text, int pos)

    property var mode: null

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
                Layout.preferredHeight: 300
                Layout.topMargin: 8
                clip: true

                visible: true

                VideoPlayer {
                    anchors.fill: parent
                    id : videoItem
                }
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
                //enabledCustom: idField.control.text.length == 23 && objectName.valueText.control.text != "" && (objectNumber.valueText.control.text != "" || popup.mode == "hub")
                anchors.centerIn: parent

                onClicked: {
                    var settings = {}


                        app.hub_management_module.add_hub(settings)
                }
            }
        }
    }

    Connections {
        target: app

        onActionFailed: {
            btnSave.loading = false
            popup.enabled = true
        }
    }

    Connections {
        target: app.facility_module

        onCreateFacilitySuccess: {
            // to open edit tab: objectsStack.currentObjectIndex = -3
            var editModeIndex = companyAccess.OBJECT_CARD_EDIT ? -3 : -2

            app.facility_module.get_facility(facility_id, editModeIndex)
            app.facility_module.clear_model()
            popup.close()
        }
    }

    Connections {
        target: app.hub_management_module

        onAddHubSuccess: {
            app.facility_module.get_facility(facility_id, -2)
            app.facility_module.clear_model()
            popup.close()
        }
    }
}

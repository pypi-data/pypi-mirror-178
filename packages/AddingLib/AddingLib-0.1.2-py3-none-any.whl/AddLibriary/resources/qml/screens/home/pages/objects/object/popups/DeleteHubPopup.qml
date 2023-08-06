import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS3/" as DS3


AjaxPopup {
    id: popup
    width: 390
    height: 600

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var user: null
    property var sideMargin: 24

    Rectangle {
        width: 390
        height: 600
        
        radius: 12
        color: ui.backgrounds.base

        DS3.NavBarModal {
            id: deleteDeviceBar

            headerText: tr.unpair_device

            /* -------------------------------------------- */
            /* desktop tests */
            accessibleIcoName: "delete-hub_" + hub.hub_id + "_close_button"
            accessibleTextName: "delete-hub_" + hub.hub_id + "_header_text"
            /* -------------------------------------------- */
        }

        Image {
            id: imageRect

            property var nothing: {
                imageRect.source = Images.get_image(device.obj_type, "Medium", device.color)
                if (hub.hub_type == "YAVIR") {
                    imageRect.source = Images.get_image("yavir_hub", "Medium")
                } else if (hub.hub_type == "YAVIR_PLUS") {
                    imageRect.source = Images.get_image("yavir_hub_plus", "Medium")
                } else if (hub.hub_type == "HUB_FIBRA") {
                    imageRect.source = Images.get_image("fibra_hub", "Medium", device.color)
                }
            }

            anchors {
                top: deleteDeviceBar.bottom
                topMargin: 64
                horizontalCenter: parent.horizontalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-hub_" + hub.hub_id + "_image"
            Accessible.description: source
            Accessible.role: Accessible.Graphic
            /* ---------------------------------------------------- */
        }

        DS3.Text {
            id: hubNameLabel

            width: parent.width - sideMargin

            anchors {
                top: imageRect.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            text: hub.name
            style: ui.ds3.text.body.MRegular
            horizontalAlignment: Text.AlignHCenter

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-hub_" + hub.hub_id + "_name"
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }

        DS3.Text {
            id: infoLabel

            width: parent.width - sideMargin

            text: util.insert(tr.remove_hub_from_this_account, [hub.name])
            style: ui.ds3.text.body.MRegular
            horizontalAlignment: Text.AlignHCenter
            color: ui.ds3.figure.nonessential
            anchors {
                top: hubNameLabel.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-hub_" + hub.hub_id + "_warning"
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }

        DS3.ButtonContained {
            id: deleteButton

            width: parent.width - sideMargin * 2

            anchors {
                bottom: parent.bottom
                bottomMargin: sideMargin
                horizontalCenter: parent.horizontalCenter
            }
            text: tr.delete

            onClicked: {
                Popups.please_wait_popup()
                app.hub_management_module.delete_user(hub.current_user, hub.hub_id)
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-hub_" + hub.hub_id + "_button"
            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
            Accessible.role: Accessible.Button
            Accessible.checkable: visible && enabled
            Accessible.onPressAction: {
                if (!Accessible.checkable) return
                deleteButton.clicked(true)
            }
            /* ---------------------------------------------------- */
        }
    }

    Connections {
        target: app
        onAltActionSuccess: {
            popup.close()
        }
    }
}
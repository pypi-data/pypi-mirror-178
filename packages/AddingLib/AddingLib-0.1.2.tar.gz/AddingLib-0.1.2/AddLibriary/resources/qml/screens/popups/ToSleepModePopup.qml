import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "toSleepModePopup"
    width: 328
    height: 480
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    property var facilityId: null

    modal: true
    focus: true

    anchors.centerIn: parent

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        clip: true
        radius: 10
        color: ui.colors.dark3
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.a911_go_to_sleep_mode + "?"
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Item {
            id: body
            width: parent.width - 64
            anchors {
                top: header.bottom
                topMargin: 32
                bottom: confirmButtonItem.top
                bottomMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            Item {
                width: parent.width
                height: 40

                Custom.TextField {
                    id: minutesField
                    width: parent.width
                    height: 40
                    placeHolderText: "1 - 300"
                    control.leftPadding: 16
                    control.validator: RegExpValidator { regExp: /^([1-9]|[1-8][0-9]|9[0-9]|[12][0-9]{2}|300)$/ }
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -4
                    }
                }
            }

            Column {
                width: parent.width
                height: parent.height - 48
                spacing: 8
                anchors.bottom: parent.bottom

                Repeater {
                    model: [tr.a911_1_minute, tr.a911_5_minutes, tr.a911_15_minutes, tr.a911_30_minutes]

                    delegate: Rectangle {
                        width: parent.width
                        height: 40
                        radius: 10
                        color: ui.colors.dark1

                        property var selected: {
                            if (index == 0 && minutesField.control.text == "1") return true
                            if (index == 1 && minutesField.control.text == "5") return true
                            if (index == 2 && minutesField.control.text == "15") return true
                            if (index == 3 && minutesField.control.text == "30") return true
                            return false
                        }

                        Custom.FontText {
                            text: modelData
                            width: parent.width - 16
                            height: parent.height
                            color: ui.colors.light3
                            font.pixelSize: 16
                            wrapMode: Text.NoWrap
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                left: parent.left
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Image {
                            sourceSize.width: 40
                            sourceSize.height: 40
                            source: "qrc:/resources/images/icons/a-success-icon.svg"
                            visible: selected
                            anchors.right: parent.right
                        }

                        Custom.HandMouseArea {
                            onClicked: {
                                if (index == 0) minutesField.control.text = "1"
                                if (index == 1) minutesField.control.text = "5"
                                if (index == 2) minutesField.control.text = "15"
                                if (index == 3) minutesField.control.text = "30"
                            }
                        }
                    }
                }
            }
        }

        Item {
            id: confirmButtonItem
            width: parent.width
            height: 96
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors.right: parent.right
            }

            Custom.Button {
                id: confirmButton
                text: tr.confirm
                width: parent.width - 64
                enabledCustom: minutesField.control.text != ""
                anchors.centerIn: parent

                onClicked: {
                    loading = true

                    app.facility_module.set_sleep_mode(popup.facilityId, minutesField.control.text)
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
            confirmButton.loading = false
        }
    }
}

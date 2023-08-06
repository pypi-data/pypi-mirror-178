import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/"



AjaxPopup {
    id: popup
    width: 360
    height: bodyRect.height
    Rectangle {
        anchors.fill: parent
        color: "transparent"
    }
    modal: true
    focus: true

    property var malfunctions_data: null
    property var incident: null
    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        id: bodyRect
        width: 360

        focus: true

        Keys.onEnterPressed: {
            okArea.clicked(true)
        }

        Keys.onReturnPressed: {
            okArea.clicked(true)
        }

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        height: {
            var viewHeight = closeItem.height + listView.contentHeight + doAction.height + needToCheck.height + 30
            return viewHeight > 500 ? 500 : viewHeight
        }
        color: "#252525"

        AjaxPopupCloseHeader {
            id: closeItem
            label: malfunctions_data.action == null ? tr.information : tr.attention
        }

        View {
            width: popup.width
            anchors {
                top: closeItem.bottom
                topMargin: 15
                bottom: doAction.top
                bottomMargin: 15
            }

            ListView {
                id: listView
                anchors.fill: parent
                model: malfunctions_data.malfunctions
                clip: true

                delegate: Item {
                    width: listView.width
                    height: textBodyField.height + 5

                    Text {
                        id: textBodyMarker
                        width: 12
                        text: "•"
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignLeft
                        anchors {
                            verticalCenter: parent.verticalCenter
                            right: textBodyField.left
                            rightMargin: 0
                        }
                    }

                    Text {
                        id: textBodyField
                        width: parent.width - 64
                        text: modelData.charAt(0).toUpperCase() + modelData.slice(1)
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 12
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignLeft
                        textFormat: Text.RichText
                        wrapMode: Text.WordWrap
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 48
                        }
                    }
                }
            }
        }

        Item {
            id: doAction
            width: parent.width
            height: visible ? 48 : 0
            visible: malfunctions_data.override
            property var isPro: !appUser.company_id
            anchors.bottom: needToCheck.top

            Rectangle {
                anchors.top: parent.top
                height: 1
                width: parent.width
                color: ui.colors.light1
                opacity: 0.1
            }

            Text {
                id: doActionText
                anchors.centerIn: parent
                text: tr.arm
                color: "#f64347"
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                width: parent.width
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }

            MouseArea {
                id: repeaterAction
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    repeaterAction.enabled = false
                    security_timer.start()

                    if (malfunctions_data.group != null) {
                        if (incident) {
                            var grs = incident.management.groups
                        } else {
                            var grs = doAction.isPro ? appCompany.pro_hubs_model.current_hub.management.groups : appCompany.current_facility.management.groups
                        }
                        var group_object = grs.get_group(malfunctions_data.group)
                        app.hub_management_module.perform_group_security_action(group_object, true, incident)
                    } else {
                        app.hub_management_module.perform_security_action(malfunctions_data.action, true, incident)
                    }
                }

                Timer {
                    id: security_timer
                    running: false
                    repeat: false
                    interval: 1000
                    onTriggered: repeaterAction.enabled = true
                }
            }
        }

        Item {
            id: needToCheck
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
                id: needToCheckText
                anchors.centerIn: parent
                text: malfunctions_data.action == null ? tr.ok : tr.i_will_check
                color: malfunctions_data.action == null ? "#60e3ab" : "#fdfdfd"
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                width: parent.width
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }

            MouseArea {
                id: okArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    popup.close()
                }
            }
        }

    }

    Connections {
        target: app
        onActionSuccess: {
            popup.close()
        }
    }
}
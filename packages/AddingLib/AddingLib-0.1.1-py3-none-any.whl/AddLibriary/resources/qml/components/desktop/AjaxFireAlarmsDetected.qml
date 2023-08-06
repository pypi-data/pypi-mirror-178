import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups

AjaxPopup {
    id: popup
    width: 360
    height: {
        let popupHeight = closeItem.height + 8 + 24 + buttonGroup.height

        if (scrollView.contentHeight > 582) return popupHeight + 582
        return popupHeight + scrollView.contentHeight

    }

    property var todo: null
    property var mtr_devices: null

    signal resetPower()

    property var management: null
    property var actionsEnabled: {
        if (!appUser.company_id || !popup.management) return true
        return companyAccess.HUB_INTERCONNECT_PROCESS && popup.management.facility_access
    }

    destructOnClose: false

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        focus: true

        Keys.onEnterPressed: {
            save.clicked(true)
        }

        Keys.onReturnPressed: {
            save.clicked(true)
        }

        AjaxPopupCloseHeader {
            id: closeItem
            fontSize: 16
            label: tr.fire_alarm_is_detected
        }

        ScrollView {
            id: scrollView

            clip: true
            width: parent.width

            anchors {
                top: closeItem.bottom
                topMargin: 8
                bottom: buttonGroup.top
                bottomMargin: 24
            }

            ScrollBar.vertical: ScrollBar {
                id: control
                policy: {
                    if (scrollView.height < scrollView.contentHeight) {
                        return ScrollBar.AlwaysOn
                    }
                    return ScrollBar.AlwaysOff
                }
                anchors.top: parent.top
                anchors.right: scrollView.right
                anchors.rightMargin: 34
                anchors.bottom: parent.bottom

                contentItem: Rectangle {
                    implicitWidth: 2
                    implicitHeight: 100
                    radius: width / 2
                    color: control.pressed ? "#81e889" : "#9e9e9e"
                    opacity: 0.6
                }

                background: Rectangle {
                    implicitWidth: 2
                    implicitHeight: 100
                    color: "#575757"
                }
            }

            Column {
                id: content

                width: parent.width
                spacing: 16

                Repeater {
                    id: mtrRepeater

                    width: parent.width
                    model: mtr_devices

                    Column {
                        width: parent.width

                        Text {
                            id: mtrName

                            text: `${mtr_devices[index].name}:`

                            width: contentWidth
                            height: contentHeight
                            color: ui.colors.light1
                            font.family: roboto.name
                            font.pixelSize: 14
                            lineHeight: 1.43
                            wrapMode: Text.Wrap
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Column {
                            id: column

                            width: parent.width
                            spacing: 0

                            Repeater {
                                id: fireRepeater
                                model: mtrRepeater.model[index].wired_fire_devices
                                width: parent.width

//                                anchors {
//                                    top: parent.top
//                                    topMargin: 16
//                                }

                                Text {
                                    id: contentTextItem

                                    text: util.insert(tr.alt_in_alt, [modelData.name, modelData.room])
                                    width: contentWidth
                                    height: contentHeight
                                    color: ui.colors.middle1
                                    font.family: roboto.name
                                    font.pixelSize: 12
                                    lineHeight: 1.33
                                    wrapMode: Text.Wrap
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                }
                            }
                        }
                    }
                }

                Text {
                    id: resetDevicesText

                    text: tr.fire_alarm_is_detected_info

                    width: parent.width - 64
                    height: contentHeight
                    color: ui.colors.middle1
                    font.family: roboto.name
                    font.pixelSize: 12
                    lineHeight: 1.33

                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }


        AjaxSaveCancel {
            id: buttonGroup
            anchors.bottom: parent.bottom

            saveArea.enabled: popup.actionsEnabled
            saveArea.opacity: saveArea.enabled ? 1 : 0.4

            cancelArea.onClicked: {
                popup.close()
            }

            saveText: tr.fire_alarm_reset
            saveArea.onClicked: {
                popup.todo()
            }
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            resetPower()
            popup.close()
        }
    }
}

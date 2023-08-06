import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/js/desktop/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 300

    modal: true
    focus: true

    property var fire_alarms: null

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var management: null
    property var actionsEnabled: {
        if (!appUser.company_id || !popup.management) return true
        return companyAccess.HUB_INTERCONNECT_PROCESS && popup.management.facility_access
    }

    Rectangle {
        width: 360
        height: 300
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.attention
        }

        View {
            width: popup.width
            anchors {
                top: closeItem.bottom
                bottom: alarmSilence.top
            }

            ListView {
                id: listView
                anchors.fill: parent
                model: {
                    return fire_alarms
                }
                clip: true
                
                delegate: Item {
                    width: listView.width
                    height: textBodyField.height
                    Text {
                        id: textBodyField
                        width: parent.width - 32
                        anchors.centerIn: parent
                        text: {
                            if (modelData) return (index+1).toString() + ".  " + util.insert(tr.alt_in_alt, [modelData.name, modelData.room_name])
                            return modelData
                        }
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignHCenter
                        textFormat: Text.RichText
                        wrapMode: Text.WordWrap
                    }
                }

                header: Item {
                    width: listView.width
                    visible: {
                        if (listView.model.length > 0) return true
                        return false
                    }
                    height: (visible) ? 20 : 0
                    Text {
                        width: parent.width
                        anchors.centerIn: parent
                        text: tr.alarm_smoke_detected + ":"
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignHCenter
                        textFormat: Text.RichText
                        wrapMode: Text.WordWrap
                    }
                }

                footer: Item {
                    width: listView.width
                    height: interconnectedAlarmText.height + interconnectedAlarmSecondText.height + 16
                    Text {
                        id: interconnectedAlarmText

                        width: parent.width
                        anchors {
                            top: parent.top
                            topMargin: 8
                        }
                        text: tr.interconnected_audible_alarm_is_activated
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignHCenter
                        textFormat: Text.RichText
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        id: interconnectedAlarmSecondText

                        width: parent.width
                        anchors {
                            top: interconnectedAlarmText.bottom
                            topMargin: 8
                        }
                        text: tr.interconnected_audible_alarm_is_activated_with_permissions
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignHCenter
                        textFormat: Text.RichText
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
        
        Item {
            id: alarmSilence
            width: parent.width
            height: 48

            enabled: popup.actionsEnabled
            opacity: enabled ? 1 : 0.4

            anchors.bottom: totalSilence.top

            Rectangle {
                anchors.top: parent.top
                height: 1
                width: parent.width
                color: ui.colors.light1
                opacity: 0.1
            }

            Text {
                id: alarmSilenceText
                anchors.centerIn: parent
                text: tr.silence_interconnected_alarms
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
                    Popups.confirm_or_cancel(
                        tr.are_you_sure_interconnect,
                        tr.are_you_sure_interconnect_info,
                        function todo() {
                            app.hub_management_module.mute_fire_detectors("ALL_FIRE_DETECTORS_EXCEPT_TRIGGERED")
                        },
                        tr.interconnect_off_short
                    )
                }
            }
        }

        Item {
            id: totalSilence
            width: parent.width
            height: 48

            enabled: popup.actionsEnabled
            opacity: enabled ? 1 : 0.4

            anchors.bottom: parent.bottom

            Rectangle {
                anchors.top: parent.top
                height: 1
                width: parent.width
                color: ui.colors.light1
                opacity: 0.1
            }

            Text {
                id: totalSilenceText
                anchors.centerIn: parent
                text: tr.silence_all_detectors
                color: "#f64347"
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
                    Popups.confirm_or_cancel(
                        tr.are_you_sure_interconnect_all,
                        tr.are_you_sure_interconnect_all_info,
                        function todo() {
                            app.hub_management_module.mute_fire_detectors("ALL_FIRE_DETECTORS")
                        },
                        tr.interconnect_off_short
                    )
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
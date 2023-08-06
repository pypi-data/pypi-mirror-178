import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/" as CustomDesktop
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/utils.js" as Utils


Rectangle {
    color: ui.colors.dark4
    Layout.minimumWidth: incidentPage.width
    Layout.maximumWidth: incidentPage.width
    Layout.fillHeight: true
    Layout.minimumHeight: gridLayout.implicitHeight + gridLayout.rows * 8
    Layout.maximumHeight: gridLayout.implicitHeight + gridLayout.rows * 8

    RowLayout {
        width: parent.width

        Rectangle {
            Layout.minimumWidth: 72
            Layout.maximumWidth: 72
            Layout.fillHeight: true
            color: "transparent"
            border.color: ui.colors.white
            border.width: 0

            Item {
                width: 72
                height: 72

                enabled: incident.management.devices.hub

                Image {
                    id: hubPseudoRect
                    sourceSize.width: 40
                    sourceSize.height: 40
                    source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                    anchors {
                        left: parent.left
                        leftMargin: 16
                        top: parent.top
                        topMargin: 16
                    }

                    visible: !pdItem.visible

                    Connections {
                        target: incident.management.devices.hub

                        onDataChanged: {
                            hubPseudoRect.repaint_state_icon()
                        }
                    }

                    Connections {
                        target: incident
                        onIs_in_sleep_modeChanged: {
                            hubPseudoRect.repaint_state_icon()
                        }
                    }

                    Connections {
                        target: incident.management.devices
                        onHubChanged: {
                            hubPseudoRect.repaint_state_icon()
                        }
                    }

                    function repaint_state_icon() {
                        if (incident.is_in_sleep_mode) {
                            stateIcon.sourceSize.width = 48
                            stateIcon.sourceSize.height = 48
                            stateIcon.source = "qrc:/resources/images/icons/icon-incident-a-icon-sleep.svg"
                            return
                        }
                        stateIcon.sourceSize.width = 24
                        stateIcon.sourceSize.height = 24

                        var st = ""
                        if (!incident || !incident.management || !incident.management.devices || !incident.management.devices.hub) {
                            stateIcon.source = ""
                            return
                        }
                        if (incident.management.devices.hub.groups_enabled) {
                            st = incident.management.devices.hub.state_with_groups
                        } else {
                            st = incident.management.devices.hub.state
                        }

                        stateIcon.source = Utils.get_data_hub_state(st)[0]
                    }

                    Image {
                        id: stateIcon
                        sourceSize.width: 24
                        sourceSize.height: 24
                        anchors.centerIn: parent
                    }
                }

                Image {
                    id: pdItem
                    sourceSize.width: 40
                    sourceSize.height: 40
                    source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                    anchors {
                        left: parent.left
                        leftMargin: 16
                        top: parent.top
                        topMargin: 16
                    }

                    visible: incident && !incident.is_in_sleep_mode && tsaState > 1

                    property var tsaState: incident && incident.management && incident.management.devices && incident.management.devices.hub && incident.management.devices.hub.firmware_version_dec >= 209100 ? incident.management.devices.hub.two_stage_arming_progress_status : 0
                    property var oldTsaState: 0

                    onTsaStateChanged: {
                        if (pdItem.tsaState != pdItem.oldTsaState) {
                            pdItem.oldTsaState = pdItem.tsaState
                            pdItem.handle_timer()
                        }
                    }

                    property int timerTime: incident && incident.management && incident.management.devices && incident.management.devices.hub ? incident.management.devices.hub.exit_timer_expiration_diff : 0
                    property var arm_timer: {
                        if (pdItem.tsaState == 2) {
                            return incident.management.devices.hub.app_exit_timer
                        } else if (pdItem.tsaState == 3) {
                            return incident.management.devices.hub.second_stage_exit_timer
                        } else if (pdItem.tsaState == 5) {
                            return incident.management.devices.hub.second_stage_exit_timer
                            // ???
                            // return hub.second_stage_exit_timer
                        }
                        return 0
                    }

                    function handle_timer() {
                        if (pdItem.tsaState == 4) return

                        if ((pdItem.tsaState > 1 && pdItem.tsaState != 5 && !timer.running) || (pdItem.tsaState == 5 && timer.running)) {
                            pdItem.timerTime = incident.management.devices.hub.exit_timer_expiration_diff
                            timeCircle.arcBegin = timer.seconds_to_arc(pdItem.arm_timer) * (pdItem.arm_timer - pdItem.timerTime)
                            timer.start()
                        } else {
                            timer.stop()
                            timeCircle.arcBegin = 0
                        }
                    }

                    Timer {
                        id: timer
                        running: false
                        interval: 1000
                        repeat: true
                        triggeredOnStart: true

                        function seconds_to_arc(seconds) {
                            return 360 / seconds
                        }

                        onTriggered: {

                            pdItem.timerTime -= 1
                            timeCircle.arcBegin = timer.seconds_to_arc(pdItem.arm_timer) * (pdItem.arm_timer - pdItem.timerTime)

                            if (pdItem.timerTime == 0) {
                                timer.stop()

                                timeCircle.arcBegin = 0
                                return
                            }
                        }

                        Component.onCompleted: {
                            if (pdItem.tsaState == 4) return

                            if ((pdItem.tsaState > 1 && pdItem.tsaState != 5 && !timer.running) || (pdItem.tsaState == 5 && timer.running)) {

                                timeCircle.arcBegin = timer.seconds_to_arc(pdItem.arm_timer) * (pdItem.arm_timer - incident.management.devices.hub.exit_timer_expiration_diff)

                                timer.start()
                            }
                        }
                    }

                    Item {
                        id: timeCircleField

                        width: 36
                        height: 36

                        anchors.centerIn: parent
                    }

                    CustomDesktop.AjaxAltTimeCircle {
                        id: timeCircle

                        anchors.fill: timeCircleField

                        size: 36
                        visible: timer.running

                        colorCircle: {
                            if (pdItem.tsaState == 2) {
                                return ui.colors.red1
                            } else if (pdItem.tsaState == 3 || pdItem.tsaState == 5) {
                                return ui.colors.lime1
                            }
                            return "transparent"
                        }

                        arcBegin: 0
                        arcEnd: 360
                        lineWidth: 1
                        colorBackground: "transparent"
                        showBackground: true
                        isPie: true
                        opacityPie: 0.4
                        addCircleToPie: true
                    }

                    Image {
                        sourceSize.width: 24
                        sourceSize.height: 24

                        anchors.centerIn: parent

                        source: {
                            if (pdItem.tsaState == 2) {
                                return "qrc:/resources/images/icons/tsa-red.svg"
                            } else if (pdItem.tsaState == 3) {
                                return "qrc:/resources/images/icons/tsa-green.svg"
                            } else if (pdItem.tsaState == 4) {
                                return "qrc:/resources/images/icons/tsa-yellow.svg"
                            } else if (pdItem.tsaState == 5) {
                                return "qrc:/resources/images/icons/tsa-green.svg"
                            }

                            return ""
                        }
                    }
                }

                Rectangle {
                    id: maskSourceRect

                    width: 40
                    height: 40
                    visible: false
                    color: ui.colors.yellow1

                    anchors.fill: pdItem
                }

                OpacityMask {
                    anchors.fill: maskSourceRect
                    source: maskSourceRect
                    maskSource: pdItem
                    opacity: 0.5
                    visible: pdItem.visible && pdItem.tsaState == 4
                }

                Custom.Triangle {
                    rotation: 0
                    scale: 0.8
                    visible: incident.status == "PROCESSING"
                    anchors {
                        left: hubPseudoRect.right
                        leftMargin: 4
                        verticalCenter: hubPseudoRect.verticalCenter
                    }
                }

                Custom.HandMouseArea {
                    enabled: incident.status == "PROCESSING"
                    onClicked: {
                        if (mouse.button === Qt.LeftButton)
                            contextMenu.popup(16, parent.height - 8)
                    }

                    Custom.ChangeMode {
                        id: contextMenu
                        management: incident.management
                        facility_id: incident.facility_id
                        incident_item: incident

                        Connections {
                            target: parent

                            onVisibleChanged: {
                                if (!visible) contextMenu.close()
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: "transparent"
            border.color: ui.colors.white
            border.width: 0

            GridLayout {
                id: gridLayout

                anchors {
                    top: parent.top
                    topMargin: 16
                }
                width: parent.width
                columns: 2
                rowSpacing: 8
                columnSpacing: 16
                rows: 7

                Custom.FontText {
                    Layout.minimumWidth: 104
                    Layout.maximumWidth: 104
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignRight
                    text: tr.object_number
                    font.pixelSize: 12
                    color: ui.colors.middle1
                    opacity: 0.6
                }

                Custom.FontText {
                    Layout.minimumWidth: 128
                    Layout.fillWidth: true
                    text: {
                        if (!incident) return ui.empty
                        if (!incident.facility) return ui.empty
                        if (!incident.facility.facility_general_info) return ui.empty
                        if (!incident.facility.facility_general_info.registration_number) return ui.empty

                        return incident.facility.facility_general_info.registration_number
                    }
                    color: ui.colors.white
                }

                Custom.FontText {
                    Layout.minimumWidth: 104
                    Layout.maximumWidth: 104
                    Layout.fillWidth: true
                    text: tr.a911_title
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                    color: ui.colors.middle1
                    opacity: 0.6
                }

                Custom.FontText {
                    Layout.minimumWidth: 128
                    Layout.fillWidth: true
                    text: {
                        if (!incident) return ui.empty
                        if (!incident.facility) return ui.empty
                        if (!incident.facility.facility_general_info) return ui.empty
                        if (!incident.facility.facility_general_info.name) return ui.empty

                        return incident.facility.facility_general_info.name
                    }
                    font.pixelSize: 18
                    wrapMode: Text.Wrap
                    color: ui.colors.white
                }

                Item {
                    Layout.alignment: Qt.AlignCenter
                    Layout.fillWidth: true
                    Layout.columnSpan: 2
                    Layout.minimumHeight: 12

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.middle1
                        opacity: 0.3
                        anchors.centerIn: parent
                    }
                }

                Custom.FontText {
                    Layout.minimumWidth: 104
                    Layout.maximumWidth: 104
                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                    Layout.fillWidth: true
                    text: tr.address
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                    color: ui.colors.middle1
                    opacity: 0.6
                }

                Custom.FontText {
                    Layout.minimumWidth: 128
                    Layout.maximumHeight: contentHeight
                    Layout.fillWidth: true
                    text: {
                        if (!incident) return ui.empty
                        if (!incident.facility) return ui.empty
                        if (!incident.facility.facility_general_info) return ui.empty
                        if (!incident.facility.facility_general_info.address) return ui.empty
                        if (!incident.facility.facility_general_info.address.address_line1) return ui.empty

                        var cityValue = incident.facility.facility_general_info.address.city ? incident.facility.facility_general_info.address.city + ", " : ""
                        return cityValue + incident.facility.facility_general_info.address.address_line1
                    }
                    color: ui.colors.white
                    wrapMode: Text.Wrap

                    lineHeight: 1.0
                }

                Item {
                    Layout.alignment: Qt.AlignCenter
                    Layout.fillWidth: true
                    Layout.columnSpan: 2
                    Layout.minimumHeight: 12

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.middle1
                        opacity: 0.3
                        anchors.centerIn: parent
                    }
                }

//                Custom.FontText {
//                    Layout.minimumWidth: 104
//                    Layout.maximumWidth: 104
//                    Layout.fillWidth: true
//                    text: tr.a911_director
//                    horizontalAlignment: Text.AlignRight
//                    font.pixelSize: 12
//                    color: ui.colors.middle1
//                    opacity: 0.6
//                }
//
//                Custom.FontText {
//                    Layout.minimumWidth: 128
//                    Layout.fillWidth: true
//                    text: "Elon Reeve Musk"
//                    color: ui.colors.white
//                }

                Custom.FontText {
                    Layout.minimumWidth: 104
                    Layout.maximumWidth: 104
                    Layout.fillWidth: true
                    text: tr.phone
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                    color: ui.colors.middle1
                    opacity: 0.6
                }

                Custom.FontText {
                    Layout.minimumWidth: 128
                    Layout.fillWidth: true
                    text: incident.phone_numbers
                    wrapMode: Text.WordWrap
                    color: ui.colors.white
                }

                Custom.FontText {
                    Layout.minimumWidth: 104
                    Layout.maximumWidth: 104
                    Layout.fillWidth: true
                    text: tr.a911_schedule
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                    color: ui.colors.middle1
                    opacity: 0.6
                }

                Custom.FontText {
                    id: scheduleItem
                    Layout.minimumWidth: 128
                    Layout.fillWidth: true
                    color: ui.colors.white
                    wrapMode: Text.WordWrap
                    text: {
                        if (!incident) return tr.a911_no_schedule
                        if (!incident.facility) return tr.a911_no_schedule
                        if (!incident.facility.facility_general_info) return tr.a911_no_schedule
                        if (!incident.facility.facility_general_info.detect_off_schedule_disarm) return tr.a911_no_schedule

                        var temp = scheduleItem.getText()
                        return temp ? temp : tr.a911_no_schedule
                    }

                    property var weekdaysData: {
                        "MONDAY": 1,
                        "TUESDAY": 2,
                        "WEDNESDAY": 3,
                        "THURSDAY": 4,
                        "FRIDAY": 5,
                        "SATURDAY": 6,
                        "SUNDAY": 0
                    }

                    function createDay(dayName, template, locale=Locale.ShortFormat) {
                        var temp = application.locale.dayName(weekdaysData[dayName], Locale.ShortFormat)
                        var temp = temp.charAt(0).toUpperCase() + temp.slice(1)
                        return template.replace(dayName, temp);
                    }

                    function getText() {
                        if (!incident) return ""
                        if (!incident.facility) return ""
                        if (!incident.facility.facility_general_info) return ""
                        if (!incident.facility.facility_general_info.schedule) return ""

                        var temp = util.normalize_schedule(incident.facility.facility_general_info.schedule)
                        var weekdaysText = ""

                        for (var i = 0; i < temp.length; i++) {
                            var template = util.normalize_schedule_display(temp[i].weekdays)
                            for (var j = 0; j < temp[i].weekdays.length; j++) {
                                template = scheduleItem.createDay(temp[i].weekdays[j], template)
                            }
                            template += ": " + temp[i].time.from + "-" + temp[i].time.to
                            weekdaysText += "; " + template
                        }
                        weekdaysText = weekdaysText.slice(2)
                        return weekdaysText
                    }
                }

                Custom.FontText {
                    Layout.minimumWidth: 104
                    Layout.maximumWidth: 104
                    Layout.fillWidth: true
                    text: tr.password
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                    color: ui.colors.middle1
                    opacity: 0.6
                }

                Custom.FontText {
                    Layout.minimumWidth: 128
                    Layout.fillWidth: true
                    rightPadding: 32
                    maximumLineCount: 2
                    wrapMode: Text.WrapAnywhere
                    color: ui.colors.white
                    text: {
                        if (!incident) return ui.empty
                        if (!incident.facility) return ui.empty
                        if (!incident.facility.facility_general_info) return ui.empty
                        if (!incident.facility.facility_general_info.false_alarm_password) return ui.empty

                        return "<span style='color: #60e3ab'>" + incident.facility.facility_general_info.false_alarm_password + "</span>"
                    }
                }
            }
        }
    }
}
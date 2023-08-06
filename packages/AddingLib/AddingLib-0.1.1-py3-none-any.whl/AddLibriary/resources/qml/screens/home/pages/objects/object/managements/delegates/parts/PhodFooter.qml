import QtQuick 2.12
import QtQuick.Controls 2.13
import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    id: phodFooter

    property bool cancelBinding: false
    property var companyPhodAccessMode: device.company_phod_access["access_mode"]
    property bool showFooter: {
        if (!appUser.company_id) return device.show_pod_button
        if (!__phod_company_features__) return false
        if (device.class_name == "camera") return true
        return ["allowed_always", "allowed_when_armed", "allowed_after_alarm"].includes(companyPhodAccessMode)
    }
//  Initial time
    property var stopTimestamp: device.company_phod_access["data"]["capture_photo_available_until"]
//  Current time left
    property var timeLeft: null

    width: parent.width
    height: showFooter ?
        Math.max(buttonTitle.height, photoButton.height) + 16 :
        0

    anchors {
        horizontalCenter: parent.horizontalCenter
        bottom: parent.bottom
    }

    Connections {
        target: hub

        onDataChanged: {
            showFooter = appUser.company_id ?
                __phod_company_features__ && (device.class_name == "camera" || ["allowed_always", "allowed_when_armed", "allowed_after_alarm"].includes(companyPhodAccessMode)) :
                device.show_pod_button
            if (stopTimestamp >= new Date().getTime() / 1000) {
                photoButton.enabled = true
                timer.start()
            }
        }
    }

    visible: showFooter

    Rectangle {
        width: parent.width - 32
        height: showFooter ? 1 : 0

        anchors.horizontalCenter: parent.horizontalCenter

        color: list.currentIndex == index ? ui.ds3.bg.highest : deviceDelegate.selectedColor
    }

    DS3.AtomTitle {
        id: buttonTitle

        property bool showLock: {
            if (!appUser.company_id) return false  // Pro
            return ["not_allowed", "forbidden_until_armed", "allowed_when_armed", "allowed_after_alarm"].includes(companyPhodAccessMode)  // Employee
        }
        property bool lockIsOpen: ["allowed_always", "allowed_when_armed", "allowed_after_alarm"].includes(companyPhodAccessMode)

        anchors {
            left: parent.left
            leftMargin: 16
            right: photoButton.left
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        title: tr.photo_by_request
        subtitle: {
            if (!showLock) return ""
            if (companyPhodAccessMode == "allowed_after_alarm") {
                if (stopTimestamp >= new Date().getTime() / 1000) {
                    var hours = Math.floor(timeLeft / 3600)
                    var min = Math.floor(timeLeft / 60) % 60
                    var sec = timeLeft % 60
                    return hours.toString().padStart(2, "0") + ":" + min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
                } else {
                    return util.insert(tr.x_min_after_alarm_desktop, [device.company_phod_access["data"]["configured_time_to_capture_photo_minutes"]])
                }
            }
            return ["forbidden_until_armed", "allowed_when_armed"].includes(companyPhodAccessMode) ?
                tr.only_when_armed_permission :
                util.insert(tr.x_min_after_alarm_desktop, [device.company_phod_forbidden_until_armed_access_minutes])
        }

        subtitleIcon {
            height: visible ? 16 : 0

            source: lockIsOpen ?
                "qrc:/resources/images/Athena/common_icons/Unlock-S.svg" :
                "qrc:/resources/images/Athena/common_icons/Lock-S.svg"
            color: ui.ds3.figure.base
            visible: showLock
        }
    }

    Timer {
        id: timer

        interval: 1000
        repeat: true
        triggeredOnStart: true

        onTriggered: {
            if (Date.now() / 1000 >= stopTimestamp) {
                timeLeft = 0
                buttonTitle.lockIsOpen = false
                buttonTitle.subtitle = util.insert(tr.x_min_after_alarm_desktop, [device.company_phod_access["data"]["configured_time_to_capture_photo_minutes"]])
                photoButton.enabled = false
                stop()
            }
            else {
                timeLeft = Math.ceil(stopTimestamp - Date.now() / 1000)
            }
        }
    }

    DS3.ButtonMini {
        id: photoButton

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        onClicked: {
            if (!device.online) return
            if (appUser.company_id) {  // Employee
                var data = {
                    "hub_id": hub.hub_id,
                    "device_id": device.device_id,
                    "device_type": {
                        "0d": 1,
                        "18": 2,
                    }[device.obj_type] || 0
                }
                app.hub_management_module.capture_PHOD_by_company(data)
            } else {
                app.hub_management_module.device_command(device, 27)  // pro
            }
        }

        source: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"
        enabled: (!appUser.company_id && device.show_pod_button) || buttonTitle.lockIsOpen  // Pro || Employee cases
        opacity: enabled ? 1 : 0.3
    }
}
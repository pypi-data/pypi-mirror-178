import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13


import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/qml/components/desktop" as CustomDesktop

Menu {
    id: contextMenu
    modal: true
    width: {
        if (!management || !management.devices.hub) return 0
        return management.devices.hub.groups_enabled ? 850 : 204
    }

    property var management: null
    property var facility_id: null
    property var incident_item: null
    property var facility_item: null

    readonly property var currentUser: management && management.devices
        && management.devices.hub && management.devices.hub.current_user

    readonly property bool anyAccess: armAccess || disarmAccess || nightModeAccess
                                      || alarmButtonAccess || chimeActivationAccess || groupsNightModeEnabled
    readonly property bool armAccess: !!(currentUser && currentUser.arm_access)
    readonly property bool disarmAccess: !!(currentUser && currentUser.disarm_access)
    readonly property bool nightModeAccess: !!(currentUser && currentUser.night_mode_access)
    readonly property bool alarmButtonAccess: !!(currentUser && currentUser.alarm_button_access)
    readonly property bool chimeActivationAccess: !!(currentUser && currentUser.chimes_activation_access)
    readonly property bool groupsNightModeEnabled: !!(management && management.devices && management.devices.hub && management.devices.hub.groups_night_mode_enabled)

    property var monitoringRequested: {
        if (!facility_item) return false
        if (!facility_item.data) return false
        if (!facility_item.data.status) return false

        return facility_item.data.status == "MONITORING_REQUESTED"
    }

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.0
        width: application.width
        height: application.height
        x: -16
        y: -70
        z: -99
    }

    onVisibleChanged: {
        if (!management.devices.hub.groups_enabled) {
            loader.sourceComponent = controlWithoutGroups
            return
        }
        loader.sourceComponent = controlWithGroups
    }

    Connections {
        target: management ? management.devices.hub : null

        onGroups_enabledChanged: {
            if (!management || !management.devices.hub.groups_enabled) {
                loader.sourceComponent = controlWithoutGroups
                return
            }
            loader.sourceComponent = controlWithGroups
        }
    }

    Loader {
        id: loader
    }

    Component {
        id: controlWithGroups

        Rectangle {
            id: body
            width: 700
            height: column.height
            radius: 8
            color: ui.colors.dark2

            Column {
                id: column
                width: body.width

                Item {
                    width: column.width
                    height: 64

                    Custom.FontText {
                        text: tr.group_mode_title
                        color: ui.colors.light3
                        opacity: 0.8
                        font.pixelSize: 16
                        anchors.centerIn: parent
                    }

                    Item {
                        id: groupTsaStatus
                        width: parent.width - 64
                        height: visible ? 32 : 0

                        clip: true
                        visible: tsaState > 1
                        property var tsaState: management && management.devices && management.devices.hub && management.devices.hub.firmware_version_dec >= 209100 ? management.devices.hub.two_stage_arming_progress_status : 0

                        anchors {
                            left: parent.left
                            leftMargin: 32
                            bottom: parent.bottom
                            bottomMargin: 8
                        }

                        Custom.FontText {
                            width: parent.width
                            height: parent.height
                            font.pixelSize: 12
                            wrapMode: Text.Wrap
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            maximumLineCount: 2
                            verticalAlignment: Text.AlignBottom
                            horizontalAlignment: Text.AlignLeft
                            anchors {
                                left: parent.left
                                bottom: parent.bottom
                            }

                            text: {
                                if (groupTsaStatus.tsaState == 2) {
                                    return tr.arming_in_progress
                                } else if (groupTsaStatus.tsaState == 3) {
                                    return tr.arming_in_progress
                                } else if (groupTsaStatus.tsaState == 4) {
                                    return tr.arming_incomplete
                                } else if (groupTsaStatus.tsaState == 5) {
                                    return tr.arming_in_progress
                                }

                                return ""
                            }

                            color: {
                                if (groupTsaStatus.tsaState == 2) {
                                    return ui.colors.red1
                                } else if (groupTsaStatus.tsaState == 3) {
                                    return ui.colors.lime1
                                } else if (groupTsaStatus.tsaState == 4) {
                                    return ui.colors.yellow1
                                } else if (groupTsaStatus.tsaState == 5) {
                                    return ui.colors.lime1
                                }

                                return "transparent"
                            }
                        }
                    }

                    CustomDesktop.AjaxChimesControl {
                        anchors {
                            right: parent.right
                            rightMargin: 32
                            verticalCenter: parent.verticalCenter
                        }
                    }
                }

                Item {
                    width: column.width
                    height: nightModeRect.height

                    Rectangle {
                        id: nightModeRect
                        color: "transparent"
                        property var borderColor: groupsNightModeEnabled ? ui.colors.green1 : ui.colors.light3

                        Rectangle {
                            height: 1
                            color: nightModeRect.borderColor
                            anchors {
                                top: parent.top
                                left: parent.left
                                right: parent.right
                            }

                            enabled: nightRect.enabled
                            opacity: enabled ? 1 : 0.3
                        }

                        Rectangle {
                            width: 1
                            color: nightModeRect.borderColor
                            anchors {
                                top: parent.top
                                bottom: parent.bottom
                                left: parent.left
                            }

                            enabled: nightRect.enabled
                            opacity: enabled ? 1 : 0.3
                        }

                        Rectangle {
                            width: 1
                            color: nightModeRect.borderColor
                            anchors {
                                top: parent.top
                                bottom: parent.bottom
                                right: parent.right
                            }

                            enabled: nightRect.enabled
                            opacity: enabled ? 1 : 0.3
                        }

                        Rectangle {
                            height: 1
                            color: nightModeRect.borderColor
                            anchors {
                                top: parent.bottom
                                left: parent.left
                                right: nightRect.left
                            }

                            enabled: nightRect.enabled
                            opacity: enabled ? 1 : 0.3
                        }

                        Rectangle {
                            height: 1
                            color: nightModeRect.borderColor
                            anchors {
                                top: parent.bottom
                                left: nightRect.right
                                right: parent.right
                            }

                            enabled: nightRect.enabled
                            opacity: enabled ? 1 : 0.3
                        }

                        anchors {
                            left: parent.left
                            right: parent.right
                            margins: 32
                            topMargin: 0
                        }

                        Custom.Button {
                            id: nightRect
                            width: 195
                            height: 40
                            radius: 8
                            color: groupsNightModeEnabled ? ui.colors.green1 : ui.colors.dark1
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: -20
                            anchors.horizontalCenter: parent.horizontalCenter
                            z: 99

                            enabled: contextMenu.nightModeAccess
                            opacity: enabled ? 1 : 0.3
                            textButton.color: transparent ? color : ui.colors.black
                            backgroundItem.color: transparent ? "transparent" : color
                            backgroundItem.opacity: 1
                            backgroundItem.border.color: color

                            onClicked: {
                                nightRect.enabled = false
                                security_timer.start()
                                if (groupsNightModeEnabled) {
                                    app.hub_management_module.perform_security_action("PARTIAL_DISARM", false, incident_item)
                                } else {
                                    app.hub_management_module.perform_security_action("PARTIAL_ARM", false, incident_item)
                                }
                            }

                            Timer {
                                id: security_timer
                                running: false
                                repeat: false
                                interval: 1000
                                onTriggered: nightRect.enabled = true
                            }

                            Item {
                                anchors.fill: parent

                                Image {
                                    sourceSize.width: 24
                                    sourceSize.height: 24
                                    width: 24
                                    height: 24
                                    source: groupsNightModeEnabled
                                        ? "qrc:/resources/images/icons/night-mode-dark.svg"
                                        : "qrc:/resources/images/desktop/button_icons/night-mode-light.svg"
                                    anchors {
                                        left: parent.left
                                        leftMargin: 6
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Custom.FontText {
                                    text: tr.part_arm
                                    color: groupsNightModeEnabled ? ui.colors.black : ui.colors.light3
                                    width: parent.width - 12 - 24
                                    anchors.centerIn: parent
                                    anchors.horizontalCenterOffset: {
                                        if (truncated) return 12
                                        return 0
                                    }
                                    textFormat: Text.PlainText
                                    elide: Text.ElideRight
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }

                        height: {
                            if (gridView.contentHeight > (application.height - 364)) return application.height - 364
                            return gridView.contentHeight + 32
                        }

                        GridView {
                            id: gridView
                            cellWidth: (parent.width - 24) / 3
                            cellHeight: 64
                            clip: true

                            opacity: enabled ? 1 : 0.5

                            model: management ? management.filtered_groups : []

                            ScrollBar.vertical: ScrollBar {
                                policy: {
                                    if (gridView.contentHeight > gridView.height) return ScrollBar.AlwaysOn
                                    return ScrollBar.AlwaysOff
                                }
                                anchors.right: parent.right
                                anchors.rightMargin: 0
                            }

                            delegate: Item {
                                id: groupDelegate
                                width: (nightModeRect.width - 24) / 3
                                height: 48

                                property var armed: group.state == "ARMED"

                                property var tsaEnabled: management && management.devices && management.devices.hub ? management.devices.hub.firmware_version_dec >= 209100 && management.devices.hub.groups_enabled : false

                                enabled: (!armed && contextMenu.armAccess)
                                    || (armed && contextMenu.disarmAccess)

                                Custom.Button {
                                    id: groupButton
                                    width: parent.width - 8
                                    height: 40
                                    color: armed ? ui.colors.green1 : ui.colors.light1
                                    transparent: true

                                    onClicked: {
                                        app.hub_management_module.perform_group_security_action(group, false, incident_item)
                                    }

                                    Item {
                                        anchors.fill: parent

                                        Image {
                                            sourceSize.width: 24
                                            sourceSize.height: 24
                                            width: 24
                                            height: 24
                                            source: {
                                                if (groupDelegate.tsaEnabled && group.two_stage_arming_status > 1) {
                                                    if (group.two_stage_arming_status == 2) {
                                                        return "qrc:/resources/images/icons/tsa-red.svg"
                                                    } else if (group.two_stage_arming_status == 3) {
                                                        return "qrc:/resources/images/icons/tsa-green.svg"
                                                    } else if (group.two_stage_arming_status == 4) {
                                                        return "qrc:/resources/images/icons/tsa-yellow.svg"
                                                    } else if (group.two_stage_arming_status == 5) {
                                                        return "qrc:/resources/images/icons/tsa-green.svg"
                                                    }
                                                }

                                                if (armed) return "qrc:/resources/images/icons/a-hub-status-icon-armed.svg"
                                                return "qrc:/resources/images/icons/a-hub-status-icon-disarmed.svg"
                                            }
                                            anchors {
                                                left: parent.left
                                                leftMargin: 6
                                                verticalCenter: parent.verticalCenter
                                            }
                                        }

                                        Custom.FontText {
                                            text: group.name
                                            color: armed ? ui.colors.green1 : ui.colors.light3
                                            width: parent.width - 12 - 24
                                            anchors.centerIn: parent
                                            anchors.horizontalCenterOffset: {
                                                if (truncated) return 12
                                                return 0
                                            }
                                            textFormat: Text.PlainText
                                            elide: Text.ElideRight
                                            horizontalAlignment: Text.AlignHCenter
                                        }
                                    }
                                }

                                ColorOverlay {
                                    anchors.fill: groupButton
                                    source: groupButton
                                    opacity: 0.7
                                    color: {
                                        if (groupDelegate.tsaEnabled && group.two_stage_arming_status <= 1) return "transparent"

                                        if (group.two_stage_arming_status == 2) {
                                            return ui.colors.red1
                                        } else if (group.two_stage_arming_status == 3) {
                                            return ui.colors.lime1
                                        } else if (group.two_stage_arming_status == 4) {
                                            return ui.colors.yellow1
                                        } else if (group.two_stage_arming_status == 5) {
                                            return ui.colors.lime1
                                        }

                                        return "transparent"
                                    }
                                }
                            }

                            anchors {
                                fill: parent
                                margins: 12
                                rightMargin: 6
                            }
                        }
                    }
                }

                Item {
                    width: parent.width
                    height: 128

                    Rectangle {
                        color: "transparent"
                        height: 64

                        anchors {
                            left: parent.left
                            leftMargin: 32
                            right: parent.right
                            rightMargin: 32
                            verticalCenter: parent.verticalCenter
                            verticalCenterOffset: 16
                        }

                        RowLayout {
                            anchors.fill: parent
                            spacing: 8

                            Custom.Button {
                                id: armButtonIncident
                                Layout.preferredWidth: 194
                                Layout.preferredHeight: 40

                                enabled: contextMenu.armAccess
                                opacity: enabled ? 1 : 0.3
                                textButton.color: transparent ? color : ui.colors.black
                                backgroundItem.color: transparent ? "transparent" : color
                                backgroundItem.opacity: 1
                                backgroundItem.border.color: color

                                onClicked: {
                                    armButtonIncident.enabled = false
                                    security_timer2.start()
                                    app.hub_management_module.perform_security_action("ARM", false, incident_item)
                                }

                                Timer {
                                    id: security_timer2
                                    running: false
                                    repeat: false
                                    interval: 1000
                                    onTriggered: armButtonIncident.enabled = true
                                }

                                Item {
                                    anchors.fill: parent

                                    Image {
                                        sourceSize.width: 24
                                        sourceSize.height: 24
                                        width: 24
                                        height: 24
                                        source: {
                                            return "qrc:/resources/images/icons/a-hub-status-icon-armed-light.svg"
                                        }
                                        anchors {
                                            left: parent.left
                                            leftMargin: 6
                                            verticalCenter: parent.verticalCenter
                                        }
                                    }

                                    Custom.FontText {
                                        text: tr.arm
                                        color: ui.colors.black
                                        width: parent.width - 12 - 24
                                        anchors.centerIn: parent
                                        anchors.horizontalCenterOffset: {
                                            if (truncated) return 12
                                            return 8
                                        }
                                        textFormat: Text.PlainText
                                        elide: Text.ElideRight
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                            Custom.Button {
                                Layout.preferredWidth: 194
                                Layout.preferredHeight: 40
                                color: ui.colors.light1

                                enabled: contextMenu.disarmAccess
                                opacity: enabled ? 1 : 0.3
                                textButton.color: transparent ? color : ui.colors.black
                                backgroundItem.color: transparent ? "transparent" : color
                                backgroundItem.opacity: 1
                                backgroundItem.border.color: color

                                onClicked: {
                                    app.hub_management_module.perform_security_action("DISARM", false, incident_item)
                                }

                                Item {
                                    anchors.fill: parent

                                    Image {
                                        sourceSize.width: 24
                                        sourceSize.height: 24
                                        width: 24
                                        height: 24
                                        source: {
                                            return "qrc:/resources/images/icons/a-hub-status-icon-disarmed-light.svg"
                                        }
                                        anchors {
                                            left: parent.left
                                            leftMargin: 6
                                            verticalCenter: parent.verticalCenter
                                        }
                                    }

                                    Custom.FontText {
                                        text: tr.disarm
                                        color: ui.colors.black
                                        width: parent.width - 12 - 24
                                        anchors.centerIn: parent
                                        anchors.horizontalCenterOffset: {
                                            if (truncated) return 12
                                            return 0
                                        }
                                        textFormat: Text.PlainText
                                        elide: Text.ElideRight
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                            Custom.Button {
                                transparent: true
                                color: ui.colors.red1
                                Layout.preferredWidth: 194
                                Layout.preferredHeight: 40

                                enabled: alarmButtonAccess
                                opacity: enabled ? 1 : 0.3
                                textButton.color: transparent ? color : ui.colors.black
                                backgroundItem.color: transparent ? "transparent" : color
                                backgroundItem.opacity: 1
                                backgroundItem.border.color: color

                                onClicked: {
                                    Popups.hub_alarm_countdown_popup("PANIC", false, incident_item)
                                }

                                Item {
                                    anchors.fill: parent

                                    Image {
                                        sourceSize.width: 24
                                        sourceSize.height: 24
                                        width: 24
                                        height: 24
                                        source: {
                                            return "qrc:/resources/images/facilities/status/icon-a-hub-status-icon-panic.svg"
                                        }
                                        anchors {
                                            left: parent.left
                                            leftMargin: 6
                                            verticalCenter: parent.verticalCenter
                                        }
                                    }

                                    Custom.FontText {
                                        text: tr.panic
                                        color: ui.colors.red1
                                        width: parent.width - 12 - 24
                                        anchors.centerIn: parent
                                        anchors.horizontalCenterOffset: {
                                            if (truncated) return 12
                                            return 0
                                        }
                                        textFormat: Text.PlainText
                                        elide: Text.ElideRight
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }

                            Item {
                                visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE
                                Layout.fillWidth: true
                            }

                            FontText {
                                visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE

                                Layout.preferredWidth: contentWidth
                                text: tr.a911_sleeping
                                font.pixelSize: 14
                                font.bold: true
                                color: ui.colors.light3

                                opacity: enabled ? 1 : 0.5
                            }

                            Toggle {
                                visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE
                                Layout.preferredWidth: 40

                                enabled: !contextMenu.monitoringRequested
                                opacity: enabled ? 1 : 0.5

                                checked: {
                                    if (!incident_item && !facility_item) return false
                                    return incident_item ? incident_item.is_in_sleep_mode : facility_item.is_in_sleep_mode
                                }

                                mouseArea.onClicked: {
                                    if (!checked) {
                                        Popups.to_sleep_mode_popup(facility_id)
                                    } else {
                                        app.facility_module.disabled_sleep_mode(facility_id)
                                    }

                                }
                            }

                            Item {
                                visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE
                                Layout.preferredWidth: 10
                            }
                        }
                    }
                }
            }
        }
    }

    Component {
        id: controlWithoutGroups

        Rectangle {
            width: contextMenu.width
            height: noGroupTsaStatus.tsaState > 1 ? column.height + 64 : column.height + 32
            radius: 8
            color: ui.colors.dark2

            Item {
                id: noGroupTsaStatus
                width: parent.width
                height: visible ? 32 : 0

                clip: true
                visible: tsaState > 1
                property var tsaState: management && management.devices && management.devices.hub && management.devices.hub.firmware_version_dec >= 209100 ? management.devices.hub.two_stage_arming_progress_status : 0

                anchors {
                    top: parent.top
                    topMargin: 4
                }

                Custom.FontText {
                    width: parent.width - 16
                    height: parent.height
                    font.pixelSize: 12
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    maximumLineCount: 2
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 8
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (noGroupTsaStatus.tsaState == 2) {
                            return tr.arming_in_progress
                        } else if (noGroupTsaStatus.tsaState == 3) {
                            return tr.arming_in_progress
                        } else if (noGroupTsaStatus.tsaState == 4) {
                            return tr.arming_incomplete
                        } else if (noGroupTsaStatus.tsaState == 5) {
                            return tr.arming_in_progress
                        }

                        return ""
                    }

                    color: {
                        if (noGroupTsaStatus.tsaState == 2) {
                            return ui.colors.red1
                        } else if (noGroupTsaStatus.tsaState == 3) {
                            return ui.colors.lime1
                        } else if (noGroupTsaStatus.tsaState == 4) {
                            return ui.colors.yellow1
                        } else if (noGroupTsaStatus.tsaState == 5) {
                            return ui.colors.lime1
                        }

                        return "transparent"
                    }
                }
            }

            Column {
                id: column
                width: parent.width

                anchors {
                    top: parent.top
                    topMargin: noGroupTsaStatus.visible ? 40 : 16
                }

                Repeater {
                    model: {
                        var model = [
                            {
                                icon: "qrc:/resources/images/icons/a-hub-status-icon-armed.svg",
                                text: tr.arm,
                                enabled: armAccess
                            },
                            {
                                icon: "qrc:/resources/images/icons/a-hub-status-icon-disarmed.svg",
                                text: tr.disarm,
                                enabled: disarmAccess
                            },
                            {
                                icon: "qrc:/resources/images/icons/night-mode.svg",
                                text: tr.part_arm,
                                enabled: nightModeAccess
                            },
                            {
                                icon: "qrc:/resources/images/desktop/button_icons/panic.svg",
                                text: tr.panic,
                                enabled: alarmButtonAccess
                            },
                        ]

                        if (
                            management && management.devices.hub
                            && management.devices.hub.chimes_available
                            && management.devices.hub.chimes_status != "NOT_READY"
                        ) model.push({
                            icon: management.devices.hub.chimes_status == "HALF_READY"
                                ? "qrc:/resources/images/desktop/chimes/BellWarning-24.svg"
                                : management.devices.hub.chimes_status == "NOT_ENABLED"
                                ? "qrc:/resources/images/desktop/chimes/BellGrey-24.svg"
                                : "qrc:/resources/images/desktop/chimes/BellFilledSoundGrey-24.svg",
                            text: tr.chime_navbar_button,
                            enabled: chimeActivationAccess
                        })
                        return model
                    }

                    Rectangle {
                        width: parent.width
                        height: 40
                        color: ui.colors.dark1

                        opacity: enabled ? 1 : 0.5
                        enabled: modelData.enabled

                        Item {
                            id: repeaterAction
                            anchors.fill: parent
                            HandMouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    var command = modelData.text
                                    if (command == tr.part_arm)
                                        command = "PARTIAL_ARM"
                                    else if (command == tr.disarm)
                                        command = "DISARM"
                                    else if (command == tr.arm)
                                        command = "ARM"
                                    else if (command == tr.panic)
                                        command = "PANIC"
                                    else if (command == tr.chime_navbar_button) {
                                        if (management.devices.hub.chimes_status == "HALF_READY")
                                            return PopupsDesk.chimes_activation_popup()
                                        PopupsDesk.please_wait_popup()
                                        app.chimes_module.hub_chimes_action(
                                            management.devices.hub.chimes_status != "ENABLED",
                                            incident_item
                                        )
                                    }

                                    if (command == "PANIC") {
                                        Popups.hub_alarm_countdown_popup(command, false, incident_item)
                                    } else {
                                        repeaterAction.enabled = false
                                        security_timer3.start()
                                        app.hub_management_module.perform_security_action(command, false, incident_item)
                                    }
                                }
                            }

                            Timer {
                                id: security_timer3
                                running: false
                                repeat: false
                                interval: 1000
                                onTriggered: repeaterAction.enabled = true
                            }

                            Image {
                                id: statusIcon

                                sourceSize.width: 24
                                sourceSize.height: 24
                                source: modelData.icon

                                anchors {
                                    left: parent.left
                                    leftMargin: 6
                                    verticalCenter: parent.verticalCenter
                                }
                            }

                            FontText {
                                width: parent.width
                                text: modelData.text
                                font.pixelSize: 14
                                color: ui.colors.light3

                                anchors {
                                    left: statusIcon.right
                                    leftMargin: 6
                                    verticalCenter: parent.verticalCenter
                                }
                            }
                        }
                        Rectangle { color: ui.colors.black; width: parent.width; height: 1; anchors.bottom: parent.bottom }
                    }
                }

                Item {
                    height: 16
                    width: parent.width
                }

                Rectangle {
                    visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE
                    width: parent.width
                    height: 40
                    color: ui.colors.dark1

                    Rectangle { color: ui.colors.black; width: parent.width; height: 1; anchors.bottom: parent.bottom }

                    RowLayout {
                        anchors.fill: parent

                        Item {
                            Layout.preferredWidth: 8
                            Layout.fillHeight: true
                        }

                        FontText {
                            Layout.fillWidth: true
                            text: tr.a911_sleeping
                            font.pixelSize: 16
                            font.bold: true
                            color: ui.colors.light3

                            visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE
                            enabled: !contextMenu.monitoringRequested
                            opacity: enabled ? 1 : 0.5
                        }

                        Toggle {
                            Layout.preferredWidth: 40
                            toggleWidth: 40
                            toggleHeight: 20

                            visible: companyAccess.INCIDENTS_SLEEP_MODE_TOGGLE
                            enabled: !contextMenu.monitoringRequested
                            opacity: enabled ? 1 : 0.5

                            checked: {
                                if (!incident_item && !facility_item) return false
                                return incident_item ? incident_item.is_in_sleep_mode : facility_item.is_in_sleep_mode
                            }

                            mouseArea.onClicked: {
                                if (!checked) {
                                    Popups.to_sleep_mode_popup(facility_id)
                                } else {
                                    app.facility_module.disabled_sleep_mode(facility_id)
                                }
                            }
                        }

                        Item {
                            Layout.preferredWidth: 16
                            Layout.fillHeight: true
                        }
                    }
                }
            }
        }
    }
    Connections {
        target: app
        onActionSuccess: {
            if (!management.devices.hub.groups_enabled) {
                contextMenu.close()
            }
        }
    }
    Connections {
        target: app.hub_management_module
        onMalfunctionsFound: {
            if (contextMenu.visible) {
                PopupsDesk.malfunctions_popup(jsonData, incident_item)
                contextMenu.close()
            }
        }
    }
}
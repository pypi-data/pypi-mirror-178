import QtQuick 2.14
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/" as CustomDesktop
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/qml/screens/home/pages/objects/object/DeclineServices/"

Rectangle {
    id: panel
    clip: true
    color: ui.colors.dark4
    Layout.fillWidth: true
    Layout.minimumHeight: 72
    Layout.maximumHeight: 240
    Layout.preferredHeight: fullView ? 240 : 72

    ParallelAnimation {
        id: viewAnim
        onFinished: {
            fullView = !fullView
        }

        PropertyAnimation {
            target: panel
            to: fullView ? 72 : 240
            duration: 200
            property: "Layout.preferredHeight"
        }

        PropertyAnimation {
            target: arrowImage
            to: fullView ? 90 : -90
            duration: 200
            property: "rotation"
        }
    }

    Item {
        id: mainPart
        width: parent.width
        height: 72

        RowLayout {
            clip: true
            spacing: 16
            width: parent.width - 36
            height: parent.height
            anchors {
                left: parent.left
                leftMargin: 16
            }

            Item {
                id: changeButtons
                Layout.minimumWidth: 64
                Layout.maximumWidth: 64
                Layout.minimumHeight: 40
                Layout.maximumHeight: 40
                Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                property var activeUntil: facility.active_until === 0
                property var hub: appCompany.current_facility && appCompany.current_facility.management && appCompany.current_facility.management.devices && appCompany.current_facility.management.devices.hub ? appCompany.current_facility.management.devices.hub : null
                enabled: hub

                Connections {
                    target: appCompany.current_facility ? appCompany.current_facility.management.devices.hub : null

                    onDataChanged: {
                        changeButtons.activeUntilChanged()
                    }
                }

                Connections {
                    target: appCompany.current_facility ? appCompany.current_facility : null

                    onDataChanged: {
                        changeButtons.activeUntilChanged()
                    }
                }

                Image {
                    sourceSize.width: 40
                    sourceSize.height: 40
                    source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                    anchors.left: parent.left

                    visible: !pdItem.visible

                    Connections {
                        target: changeButtons

                        onActiveUntilChanged: {
                            if (facility.is_in_sleep_mode) {
                                stateIcon.sourceSize.width = 48
                                stateIcon.sourceSize.height = 48
                                stateIcon.source = "qrc:/resources/images/icons/icon-incident-a-icon-sleep.svg"
                                return
                            }

                            if (!changeButtons.activeUntil) {
                                stateIcon.source = "qrc:/resources/images/icons/delete.svg"
                                stateIcon.sourceSize.width = 40
                                stateIcon.sourceSize.height = 40
                                return
                            }

                            if (changeButtons.hub) {
                                var st
                                if (changeButtons.hub.groups_enabled) {
                                    st = changeButtons.hub.state_with_groups
                                } else {
                                    st = changeButtons.hub.state
                                }
                                stateIcon.source = Utils.get_data_hub_state(st)[0]
                                stateIcon.sourceSize.width = 24
                                stateIcon.sourceSize.height = 24
                            }

                        }
                    }

                    Connections {
                        target: appCompany.current_facility ? appCompany.current_facility.management.devices : null

                        onHubChanged: {
                            stateIcon.sourceSize.width = 24
                            stateIcon.sourceSize.height = 24

                            if (facility.is_in_sleep_mode) {
                                stateIcon.sourceSize.width = 48
                                stateIcon.sourceSize.height = 48
                                stateIcon.source = "qrc:/resources/images/icons/icon-incident-a-icon-sleep.svg"
                                return
                            } else if (!changeButtons.activeUntil) {
                                stateIcon.source = "qrc:/resources/images/icons/delete.svg"
                                stateIcon.sourceSize.width = 40
                                stateIcon.sourceSize.height = 40
                                return
                            }

                            if (!changeButtons.hub) return

                            var st
                            if (changeButtons.hub.groups_enabled) {
                                st = changeButtons.hub.state_with_groups
                            } else {
                                st = changeButtons.hub.state
                            }
                            stateIcon.source = Utils.get_data_hub_state(st)[0]
                        }
                    }

                    Connections {
                        target: facility
                        onIs_in_sleep_modeChanged: {
                            changeButtons.activeUntilChanged()
                        }
                    }

                    Image {
                        id: stateIcon
                        sourceSize.width: 24
                        sourceSize.height: 24
                        anchors.centerIn: parent
                    }

                    Timer {
                        repeat: true
                        running: true
                        interval: 1000
                        onTriggered: {
                            facility.sleepModeChanged()
                        }
                    }
                }

                Image {
                    id: pdItem
                    sourceSize.width: 40
                    sourceSize.height: 40
                    source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                    anchors.left: parent.left

                    visible: !facility.is_in_sleep_mode && changeButtons.activeUntil && tsaState > 1

                    property var tsaState: contextMenu.management && contextMenu.management.devices && contextMenu.management.devices.hub && contextMenu.management.devices.hub.firmware_version_dec >= 209100 ? contextMenu.management.devices.hub.two_stage_arming_progress_status : 0
                    property var oldTsaState: 0

                    onTsaStateChanged: {
                        if (pdItem.tsaState != pdItem.oldTsaState) {
                            pdItem.oldTsaState = pdItem.tsaState
                            pdItem.handle_timer()
                        }
                    }

                    property int timerTime: contextMenu.management && contextMenu.management.devices && contextMenu.management.devices.hub ? contextMenu.management.devices.hub.exit_timer_expiration_diff : 0
                    property var arm_timer: {
                        if (pdItem.tsaState == 2) {
                            return contextMenu.management.devices.hub.app_exit_timer
                        } else if (pdItem.tsaState == 3) {
                            return contextMenu.management.devices.hub.second_stage_exit_timer
                        } else if (pdItem.tsaState == 5) {
                            return contextMenu.management.devices.hub.second_stage_exit_timer
                            // ???
                            // return hub.second_stage_exit_timer
                        }
                        return 0
                    }

                    function handle_timer() {
                        if (pdItem.tsaState == 4) return

                        if ((pdItem.tsaState > 1 && pdItem.tsaState != 5 && !timer.running) || (pdItem.tsaState == 5 && timer.running)) {
                            pdItem.timerTime = contextMenu.management.devices.hub.exit_timer_expiration_diff
                            timeCircle.arcBegin = timer.seconds_to_arc(pdItem.arm_timer) * (pdItem.arm_timer - pdItem.timerTime)
                            timer.reset()
                            timer.start()
                        } else {
                            timer.stop()
                            timeCircle.arcBegin = 0
                        }
                    }

                    Timer {
                        id: timer

                        property var timeOnStart: null
                        property var timeElapsed: 0
                        property var time: 0

                        function reset() {
                            time = pdItem.timerTime
                            timeOnStart = Date.now() / 1000
                            timeElapsed = 0
                        }

                        running: false
                        interval: 100
                        repeat: true
                        triggeredOnStart: true

                        function seconds_to_arc(seconds) {
                            return 360 / seconds
                        }

                        onTriggered: {
                            timeElapsed = Math.round(Date.now() / 1000 - timeOnStart)
                            pdItem.timerTime = time - timeElapsed + 1
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

                                timeCircle.arcBegin = timer.seconds_to_arc(pdItem.arm_timer) * (pdItem.arm_timer - contextMenu.management.devices.hub.exit_timer_expiration_diff)

                                timer.reset()
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
                        lineWidth: 2
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

                Item {
                    width: 24
                    height: parent.height
                    anchors.right: parent.right

                    visible: contextMenu.anyAccess

                    Custom.Triangle {
                        visible: changeButtons.activeUntil
                        rotation: 0
                        scale: 0.8
                        anchors.centerIn: parent
                    }
                }

                Custom.HandMouseArea {
                    visible: changeButtons.activeUntil
                    onClicked: {
                         if (mouse.button === Qt.LeftButton)
                            contextMenu.popup(0, parent.height + 8)
                    }
                }

                Custom.ChangeMode {
                    id: contextMenu
                    management: appCompany.current_facility ? appCompany.current_facility.management : null
                    facility_id: appCompany.current_facility ? appCompany.current_facility.id : ""
                    facility_item: appCompany.current_facility
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Custom.FontText {
                    width: parent.width
                    height: 20
                    text: {
                        var data = util.colorize("№  ", ui.colors.middle3)
                        return facility.data.facility_general_info ? data + facility.data.facility_general_info.registration_number : data + ui.empty
                    }
                    color: ui.colors.light3
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }

                Custom.FontText {
                    width: parent.width
                    height: 32
                    text: facility.data.facility_general_info ? facility.data.facility_general_info.name : facility.data.hub_id
                    color: ui.colors.light3
                    font.pixelSize: 24
                    font.bold: true
                    maximumLineCount: 1
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        bottom: parent.bottom
                        bottomMargin: 8
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    source: "qrc:/resources/images/facilities/info/home.svg"
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }
                }

                Custom.FontText {
                    width: parent.width - 42
                    text: facility.address ? facility.address : ui.empty
                    color: ui.colors.light3
                    font.pixelSize: 14
                    font.weight: Font.Light
                    elide: Text.ElideRight
                    wrapMode: Text.Wrap
                    textFormat: Text.PlainText
                    maximumLineCount: 3
                    horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                    anchors {
                        left: parent.left
                        leftMargin: 40
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                id: editRestoreButton
                Layout.minimumWidth: 160
                Layout.maximumWidth: 160
                Layout.minimumHeight: 48
                Layout.maximumHeight: 48
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                property var restoreMode: [1, 2, 3, 4, 5, 6, 7].includes(facility.scheduled_removal)

                visible: {
                    if (!editRestoreButton.restoreMode && !!facility.editable_fields.length)
                        return true
                    if (editRestoreButton.restoreMode && (
                        companyAccess.OBJECT_MONITORING_DELETE || companyAccess.OBJECT_INSTALLATION_DELETE
                    )) return true
                    return false
                }

                Custom.Button {
                    id: editButton
                    width: parent.width
                    text: editRestoreButton.restoreMode ? tr.restore_object : tr.object_settings_desktop
                    textButton.wrapMode: Text.Wrap
                    transparent: true
                    color: ui.colors.green1
                    loading_background_color: "transparent"
                    anchors.centerIn: parent
                    anim.anchors.verticalCenterOffset: 0

                    onClicked: {
                        if (editRestoreButton.restoreMode) {
                            editButton.loading = true
                            app.facility_module.restore_facilities([facility.data.hub_id])
                            return
                        }

                        editObjectLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/EditObject.qml")
                    }

                    Component.onCompleted: {
                        if (editRestoreButton.restoreMode) return

                        if (editRestoreButton.visible && objectsStack.currentObjectIndex == -3) {
                            editButton.clicked(true)
                        }
                    }
                }

                Connections {
                    target: app.facility_module

                    onScheduleChannel911RemovalSuccess: {
                        objectsStack.currentObjectIndex = -1
                    }

                    onRemoveChannel911Success: {
                        objectsStack.currentObjectIndex = -1
                    }
                }
            }

            DeclineServiceButton {
                accessibleServices: facility.data.provided_services.filter(
                    (service) => {
                        return {
                            MONITORING: companyAccess.OBJECT_MONITORING_DELETE && facility.data.channel_state != "INACTIVE",
                            INSTALLATION: companyAccess.OBJECT_INSTALLATION_DELETE && management.facility_access
                        }[service]
                    }
                )
            }

            Custom.Button {
                Layout.minimumWidth: 138
                Layout.maximumWidth: 138
                Layout.minimumHeight: 40
                Layout.maximumHeight: 40
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
                visible: !changeButtons.activeUntil
                transparent: true
                text: tr.restore_object
                onClicked: {
                    app.facility_module.restore_removed(facility.id)
                }
            }

            Rectangle {
                Layout.minimumWidth: 64
                Layout.maximumWidth: 64
                Layout.minimumHeight: 40
                Layout.maximumHeight: 40
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
                visible: changeButtons.activeUntil
                radius: height / 2
                color: "transparent"
                border.width: 1
                border.color: ui.colors.light3

                Custom.HandMouseArea {
                    onClicked: {
                        viewAnim.start()
                    }
                }

                Image {
                    id: arrowImage
                    source: "qrc:/resources/images/icons/right-arrow-white.svg"
                    sourceSize.width: 12
                    sourceSize.height: 21
                    rotation: fullView ? -90 : 90
                    anchors.centerIn: parent
                }
            }
        }

        Rectangle {
            anchors.fill: parent
            color: ui.colors.dark4
            visible: facility.data.company_id == "" || !facility.id

            MouseArea { anchors.fill: parent }

            RowLayout {
                clip: true
                spacing: 16
                width: parent.width - 36
                height: parent.height
                anchors {
                    left: parent.left
                    leftMargin: 16
                }

                Item {
                    Layout.minimumWidth: 64
                    Layout.maximumWidth: 64
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

                    Image {
                        sourceSize.width: 40
                        sourceSize.height: 40
                        source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                        anchors.left: parent.left

                        Image {
                            sourceSize.width: 40
                            sourceSize.height: 40
                            opacity: 0.8
                            source: "qrc:/resources/images/icons/a-logo-pro.svg"
                            anchors {
                                centerIn: parent
                                verticalCenterOffset: 1
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Custom.FontText {
                        width: parent.width
                        height: 20
                        text: {
                            var temp = tr.a911_from + " "
                            if (!facility.data.created_date) return temp + ui.empty
                            if (!facility.data.created_date.seconds) return temp + ui.empty

                            var newDate = new Date(facility.data.created_date.seconds * 1000)
                            newDate = newDate.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.ShortFormat))
                            return temp + newDate
                        }
                        color: ui.colors.middle3
                        font.pixelSize: 14
                        font.capitalization: Font.AllLowercase
                        font.weight: Font.Light
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignLeft
                        anchors {
                            top: parent.top
                            topMargin: 12
                            left: parent.left
                        }
                    }

                    Custom.FontText {
                        width: parent.width
                        height: 32
                        text: facility.data.hub_id
                        color: ui.colors.light3
                        font.pixelSize: 24
                        font.bold: true
                        maximumLineCount: 1
                        textFormat: Text.PlainText
                        elide: Text.ElideRight
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignLeft
                        anchors {
                            left: parent.left
                            bottom: parent.bottom
                            bottomMargin: 8
                        }
                    }
                }

                Item {
                    Layout.minimumWidth: 336
                    Layout.maximumWidth: 336
                    Layout.fillHeight: true

                    Connections {
                        target: app.facility_module

                        onDeleteHubCompanyBindingSuccess: {
                            objectsStack.currentObjectIndex = -1
                        }
                    }

                    Item {
                        width: 160
                        height: parent.height
                        anchors {
                            left: parent.left
                            verticalCenter: parent.verticalCenter
                        }

                        enabled: companyAccess.OBJECT_MONITORING_DELETE
                        opacity: enabled ? 1 : 0.3

                        Custom.Button {
                            width: parent.width
                            text: tr.reject
                            transparent: true
                            color: ui.colors.red1
                            anchors.centerIn: parent

                            onClicked: PopupsDesk.popupByPath(
                                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                                    title: tr.a911_delete_object_permanently,
                                    text: tr.delete_object_permanently_description_911,
                                    firstButtonText: tr.stop_monitoring_button,
                                    firstButtonCallback: () => {
                                        app.bindings_module.reject_monitoring_application(facility.hub_id || "")
                                    },
                                    isFirstButtonRed: true,
                                    secondButtonText: tr.cancel,
                                    isVertical: true
                                }
                            )
                        }
                    }

                    Item {
                        width: 160
                        height: parent.height
                        anchors {
                            right: parent.right
                            verticalCenter: parent.verticalCenter
                        }

                        Custom.Button {
                            width: parent.width
                            text: tr.accept
                            transparent: true
                            color: ui.colors.green1
                            anchors.centerIn: parent

                            enabled: companyAccess.OBJECTS_MONITORING_REQUEST_FROM_USER_APPROVE
                                && companyAccess.OBJECTS_MONITORING_REQUEST_FROM_INSTALLER_APPROVE
                            opacity: enabled ? 1 : 0.3

                            onClicked: {
                                var settingsData = {}

                                settingsData["hub_id"] = facility.hub_id
                                settingsData["registration_number"] = facility.number
                                settingsData["name"] = facility.name
                                settingsData["facility_id"] = facility.id

                                Popups.create_911_channel_popup(settingsData)
                            }
                        }
                    }
                }
            }
        }
    }

    Item {
        id: additionalPart
        clip: true
        width: parent.width - 96
        anchors {
            top: parent.top
            topMargin: 72
            right: parent.right
            bottom: parent.bottom
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark1
        }

        GridLayout {
            width: parent.width - 32
            height: 136
            clip: true
            columns: 2
            rows: 4
            anchors {
                left: parent.left
                leftMargin: 8
                verticalCenter: parent.verticalCenter
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Custom.FontText {
                    width: parent.width
                    height: 24
                    text: {
                        var data = util.colorize(tr.a911_contract + ":  ", ui.colors.middle3)

                        if (!facility.data.facility_general_info) return data + ui.empty
                        if (facility.data.facility_general_info.agreement && facility.data.facility_general_info.agreement.number) {
                            return data + facility.data.facility_general_info.agreement.number
                        }
                        return data + ui.empty
                    }
                    color: ui.colors.light3
                    maximumLineCount: 1
                    font.pixelSize: 16
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Image {
                    source: "qrc:/resources/images/facilities/info/phone.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    width: parent.width - 32
                    height: 20
                    text: {
                        if (!facility.data.facility_general_info) return ui.empty
                        var phones = util.join(facility.data.facility_general_info.phone_numbers, "number")
                        return phones ? phones : ui.empty
                    }
                    color: ui.colors.light3
                    maximumLineCount: 1
                    textFormat: Text.PlainText
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Image {
                    source: "qrc:/resources/images/facilities/info/ok.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    width: parent.width - 32
                    height: 20
                    text: {
                        var s1 = util.colorize(tr.a911_from + "  ", ui.colors.middle3)
                        var s2 = util.colorize("  " +  tr.a911_to + "  ", ui.colors.middle3)
                        var startDate = ""
                        var endDate = ""
                        if (!facility.data.facility_general_info) {
                            startDate = ui.empty
                            endDate = ui.empty
                            return s1 + startDate + s2 + endDate
                        }
                        if (!facility.data.facility_general_info.agreement) {
                            startDate = ui.empty
                            endDate = ui.empty
                            return s1 + startDate + s2 + endDate
                        }

                        if (!facility.data.facility_general_info.agreement.signing_date) {
                            startDate = ui.empty
                        } else if (!facility.data.facility_general_info.agreement.signing_date.seconds) {
                            startDate = ui.empty
                        } else {
                            startDate = new Date(facility.data.facility_general_info.agreement.signing_date.seconds * 1000)
                            startDate = startDate.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.ShortFormat))
                        }

                        if (!facility.data.facility_general_info.agreement.termination_date) {
                            endDate = ui.empty
                        } else if (!facility.data.facility_general_info.agreement.termination_date.seconds) {
                            endDate = ui.empty
                        } else {
                            endDate = new Date(facility.data.facility_general_info.agreement.termination_date.seconds * 1000)
                            endDate = endDate.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.ShortFormat))
                        }

                        return s1 + startDate + s2 + endDate
                    }
                    color: ui.colors.light3
                    maximumLineCount: 1
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Image {
                    source: "qrc:/resources/images/facilities/info/mail.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    width: parent.width - 32
                    height: 20
                    text: {
                        if (!facility.data.facility_general_info) return ui.empty
                        var phones = util.join(facility.data.facility_general_info.email_addresses, "email")
                        return phones ? phones : ui.empty
                    }
                    color: ui.colors.light3
                    maximumLineCount: 1
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Image {
                    source: "qrc:/resources/images/facilities/info/man.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    width: parent.width - 32
                    height: 20
                    text: {
                        if (!facility.data.facility_general_info) return ui.empty
                        if (facility.data.facility_general_info.agreement && facility.data.facility_general_info.agreement.companyLegalName) {
                            return facility.data.facility_general_info.agreement.companyLegalName
                        }
                        return ui.empty
                    }
                    color: ui.colors.light3
                    maximumLineCount: 1
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                id: scheduleItem
                Layout.fillWidth: true
                Layout.fillHeight: true

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
                    if (!facility.data.facility_general_info) return ""
                    if (!facility.data.facility_general_info.schedule) return ""

                    var temp = util.normalize_schedule(facility.data.facility_general_info.schedule)
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

                Image {
                    source: "qrc:/resources/images/facilities/info/clock.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    width: parent.width - 32
                    height: 20
                    text: {
                        if (!facility) return tr.a911_no_schedule
                        if (!facility.data) return tr.a911_no_schedule
                        if (!facility.data.facility_general_info) return tr.a911_no_schedule
                        if (!facility.data.facility_general_info.detect_off_schedule_disarm) return tr.a911_no_schedule

                        var temp = scheduleItem.getText()
                        return temp ? temp : tr.a911_no_schedule
                    }
                    color: ui.colors.light3
                    maximumLineCount: 1
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Image {
                    source: "qrc:/resources/images/facilities/info/key.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    width: parent.width - 32
                    height: 20
                    text: facility.data.facility_general_info ? facility.data.facility_general_info.false_alarm_password : ui.empty
                    color: ui.colors.light3
                    maximumLineCount: 1
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }
        }
    }
}
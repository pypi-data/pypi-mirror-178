import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    property var sideMargin: 24
    property var devEnable: true

    Connections {
        target: app

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    color: ui.ds3.bg.base

    Loader {
        id: verificationModeLoader

        anchors.fill: parent

        source: ""
        z: 3
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            let changes_list = [
                protocolPicker.currentIndex,
                ipAddressField.atomInput.text,
                portField.atomInput.text,
                secondaryIpAddressField.atomInput.text,
                secondaryPortField.atomInput.text,
                ethernetField.checked,
                gprsField.checked,
                wifiField.checked,
                reportField.checked,
                sendCoordinates.checked
            ]
            if (protocolPicker.currentIndex == 0) {
                changes_list.push(alarmAsMalfunctionWhenArming.checked)
            }
            if (protocolPicker.currentIndex == 1) {
                changes_list.push(
                    siaAccountNumber.atomInput.text,
                    connectOnDemand.checked,
                    siaEncryption.checked
                )
            }
            if (reportField.checked) {
                changes_list.push(pingPeriod.value)
            }
            if (siaEncryption.checked) {
                changes_list.push(siaEncryptionKey.atomInput.text)
            }
            return changes_list
        }
    }

    DS3.NavBarModal {
        id: monitoringSettingsBar

        headerText: tr.monitoring_station
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: monitoringSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: protocolPicker

                property int current: hub.cms_protocol == "CID" ? 0 : 1

                model: [tr.ajax_translator, tr.sia]
                atomTitle.title: tr.protocol
                enabled: devEnable
                currentIndex: current

                onCurrentIndexChanged: {
                    current = currentIndex
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: siaAccountNumber

                visible: protocolPicker.currentIndex == 1
                atomInput {
                    label: tr.account_number
                    text: hub.sia_account_number
                    validator: RegExpValidator { regExp: ui.regexes.object_number }
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: siaAccountNumber.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: connectOnDemand

                width: parent.width

                title: tr.connect_on_demand
                checked: hub.cms_connection_mode == 2
                visible: protocolPicker.currentIndex == 1
            }
        }

        DS3.Spacing {
            height: connectOnDemand.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.primary_ip
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.special.SectionCaps
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            id: primaryIpBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: ipAddressField

                atomInput {
                    label: tr.ip_address
                    placeholderText: "0.0.0.0"
                    text: hub.cms_address
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                    required: false
                }
            }

            DS3.InputSingleLine {
                id: portField

                atomInput {
                    label: tr.port
                    placeholderText: "0"
                    text: hub.cms_port
                    validator: RegExpValidator { regExp: ui.regexes.port }
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            text: tr.secondary_ip
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.special.SectionCaps
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            id: reserveIpBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: secondaryIpAddressField

                atomInput {
                    label: tr.ip_address
                    placeholderText: "0.0.0.0"
                    text: hub.cms_address_reserve
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                    required: false
                }
            }

            DS3.InputSingleLine {
                id: secondaryPortField

                atomInput {
                    label: tr.port
                    placeholderText: "0"
                    text: hub.cms_port_reserve
                    validator: RegExpValidator { regExp: ui.regexes.port }
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: ethernetField

                width: parent.width

                title: tr.log_types_1
                checked: hub.eth_cms_enabled
            }

            DS3.SettingsSwitch {
                id: gprsField

                width: parent.width

                title: tr.gprs
                checked: hub.gprs_cms_enabled
            }

            DS3.SettingsSwitch {
                id: wifiField

                width: parent.width

                title: tr.log_types_2
                checked: hub.cms_wifi_enabled
                visible: hub.hub_type == "HUB_PLUS" || hub.hub_type == "HUB_2_PLUS"
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: tr.choose_the_channel_to_send_the_alarms_to_the_central_monitoring_station
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.body.MRegular
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: reportField

                width: parent.width

                title: tr.periodic_test
                checked: hub.cms_ping_period_seconds != 0
            }

            DS3.SettingsSliderValue {
                id: pingPeriod

                property var additionalModel: [60, 300, 600, 900, 1800, 2700, 3600, 7200, 10800, 21600, 43200, 86400]

                model: ["1 " + tr.min, "5 " + tr.mins, "10 " + tr.mins, "15 " + tr.mins, "30 " + tr.mins, "45 " + tr.mins, "1 " + tr.hr, "2 " + tr.hrs, "3 " + tr.hrs, "6 " + tr.hrs, "12 " + tr.hrs, "24 " + tr.hrs]
                visible: reportField.checked
                title: tr.monitoring_station_ping_interval_min
                value: hub.cms_ping_period_seconds ? model[additionalModel.indexOf(hub.cms_ping_period_seconds)] : 0
            }
        }

        DS3.Spacing {
            height: alarmAsMalfunctionWhenArming.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: {
                if (hub.firmware_version_dec >= 207002) {
                    if (protocolPicker.currentIndex == 0 && hub.arm_prevention_mode == 2) {
                        return true
                    }
                }
                return false
            }

            DS3.SettingsSwitch {
                id: alarmAsMalfunctionWhenArming

                width: parent.width

                title: tr.alarm_as_malfunction_when_arming
                checked: hub.alarm_as_malfunction_when_arming
            }
        }

         DS3.Text {
            width: parent.width

            text: tr.alarm_as_malfunction_when_arming_desc
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.body.MRegular
            visible: alarmAsMalfunctionWhenArming.visible
        }

        DS3.Spacing {
            height: siaEncryption.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.sia_encryption
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.special.SectionCaps
            visible: siaEncryption.visible
        }

        DS3.Spacing {
            height: siaEncryption.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            id: encryptionBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: protocolPicker.currentIndex == 1

            DS3.SettingsSwitch {
                id: siaEncryption

                width: parent.width

                title: tr.sia_encryption
                checked: ["AES128", "AES256"].includes(hub.sia_encryption_type)
            }

            DS3.InputPassword {
                id: siaEncryptionKey

                visible: siaEncryption.checked
                atomInput {
                    label: tr.sia_encryption_key
                    text: hub.sia_encryption_key
                    validator: RegExpValidator { regExp: /^([a-zA-Z0-9!""#$%&'()*+,-./:;<=>?@[\]^_`{|}~]){16}|([a-zA-Z0-9!""#$%&'()*+,-./:;<=>?@[\]^_`{|}~]){32}$/ }
                    required: enabled
                }
            }
        }

        DS3.Spacing {
            height: sendCoordinates.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: sendCoordinates

                width: parent.width

                title: tr.send_panic_coordinates
                checked: hub.send_panic_button_location
                visible: hub.send_panic_button_location_available
            }
        }

        DS3.Spacing {
            height: sendCoordinates.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.send_panic_coordinates_hint
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.body.MRegular
            visible: sendCoordinates.visible
        }

        DS3.Spacing {
            height: reportZoneRestore.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsNavigationTitlePrimary {
                id: reportZoneRestore

                title: tr.report_zone_restore
                visible: hub.firmware_version_dec >= 209100

                onEntered: {
                    verificationModeLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/monitoring/ReportZoneRestore.qml")
                }
            }
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            let notValid = []

            if (!ipAddressField.isValid) {
                notValid.push(primaryIpBlock)
            }
            if (!portField.isValid) {
                notValid.push(primaryIpBlock)
            }
            if (!secondaryIpAddressField.isValid) {
                notValid.push(reserveIpBlock)
            }
            if (!secondaryPortField.isValid) {
                notValid.push(reserveIpBlock)
            }
            if (siaEncryption.checked && !siaEncryptionKey.isValid) {
                notValid.push(encryptionBlock)
            }

            if (notValid.length) return userSettings.scrollBar.scrollTo(notValid[0].y)

            var settings = {
                "cms": {
                    "address": ipAddressField.atomInput.text,
                    "port": parseInt(portField.atomInput.text),
                    "address_reserve": secondaryIpAddressField.atomInput.text,
                    "port_reserve": parseInt(secondaryPortField.atomInput.text),
                    "ping_period_seconds": reportField.checked ? pingPeriod.additionalModel[pingPeriod.model.indexOf(pingPeriod.value)] : 0,
                    "ethernet_enabled": ethernetField.checked,
                    "gprs_enabled": gprsField.checked,
                    "sia_encryption_type": siaEncryption.checked ? "AES128" : "OFF",
                    "send_panic_button_location": sendCoordinates.checked,
                },
            }

            if (protocolPicker.current != (hub.cms_protocol == "CID" ? 0 : 1)) {
                settings["cms"]["protocol"] = protocolPicker.current == 0 ? "CID" : "SIA"
            }
            if (connectOnDemand.visible) {
                // in the proto 1 - ALWAYS_UP, 2 - ON_DEMAND
                settings["cms"]["connection_mode"] = connectOnDemand.checked ? 2 : 1
            }
            if (siaAccountNumber.visible) {
                settings["cms"]["sia_account_number"] = siaAccountNumber.atomInput.text.toUpperCase()
            }
            if (wifiField.visible) {
                settings["cms"]["wifi_enabled"] = wifiField.checked
            }
            if (siaEncryption.checked) {
                settings["cms"]["sia_encryption_key"] = siaEncryptionKey.atomInput.text
            }
            if (alarmAsMalfunctionWhenArming.visible) {
                // the absence of <cms> flag is not an error
                settings["alarm_as_malfunction_when_arming"] = alarmAsMalfunctionWhenArming.checked
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}

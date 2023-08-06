import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom


// QML ColumnLayout: Possible anchor loop detected on fill.


Rectangle {
    id: editBody
    color: ui.colors.dark3

    property var hubTimezone: hub ? hub.time_zone : ""
    property var editableFields: facility.editable_fields

    function createSettings(initial) {
        var settings = {}

        // object
        settings["name"] = objectBlock.blockLoader.item.nameField.valueText.control.text
        settings["registration_number"] = objectBlock.blockLoader.item.numberField.valueText.control.text

        // address
        settings["address"] = {}
        settings["address"]["address_line1"] = addressBlock.blockLoader.item.streetField.valueText.control.text
        settings["address"]["city"] = addressBlock.blockLoader.item.cityField.valueText.control.text
        settings["address"]["state"] = addressBlock.blockLoader.item.stateField.valueText.control.text
        settings["address"]["zip_code"] = addressBlock.blockLoader.item.zipCodeField.valueText.control.text

        if (addressBlock.blockLoader.item.countryField.currentFieldValue == "") {
            settings["address"]["country"] = ""
        } else {
            var code = util.get_country_code(addressBlock.blockLoader.item.countryField.originModel, addressBlock.blockLoader.item.countryField.currentFieldValue)
            if (code == "") {
                addressBlock.blockLoader.item.countryField.textField.valid = false
                scrollBarAnim.to = 0.15
                scrollBarAnim.start()
                return
            }
            settings["address"]["country"] = code
        }

        // contacts
        var phones = []
        contactsBlock.blockLoader.item.phonesField.listView.model.forEach(function(phone) {
            phones.push(phone)
        })
        var emails = []
        contactsBlock.blockLoader.item.emailsField.listView.model.forEach(function(email) {
            emails.push(email)
        })
        settings["phone_numbers"] = phones
        settings["email_addresses"] = emails

        // security
        if (securBlock.blockLoader.item.coordinatesField.visible) {
            settings["location"] = util.get_coordinates(securBlock.blockLoader.item.coordinatesField.valueText.control.text)
        }
        settings["false_alarm_password"] = securBlock.blockLoader.item.passwordField.valueText.control.text

        // agreement
        settings["agreement"] = {}
        settings["agreement"]["number"] = contractBlock.blockLoader.item.registrationField.valueText.control.text
        settings["agreement"]["companyLegalName"] = contractBlock.blockLoader.item.companyLegalNameField.valueText.control.text
        settings["agreement"]["notes"] = contractBlock.blockLoader.item.notesField.valueText.control.text

        if (contractBlock.blockLoader.item.startDate.date) {
            var startDate = contractBlock.blockLoader.item.startDate.date
            startDate = Date.fromLocaleString(application.locale, startDate, application.shortDateFormat)
            startDate = startDate.getTime() / 1000
            settings["agreement"]["signing_date"] = startDate
        }

        if (contractBlock.blockLoader.item.endDate.date) {
            var endDate = contractBlock.blockLoader.item.endDate.date
            endDate = Date.fromLocaleString(application.locale, endDate, application.shortDateFormat)
            endDate = endDate.getTime() / 1000
            settings["agreement"]["termination_date"] = endDate
        }

        settings["detect_off_schedule_disarm"] = scheduleBlock.blockLoader.item.detectDisarm.checked

        settings["schedule"] = scheduleBlock.blockLoader.item.scheduleModel
        settings["timezone_id"] = editBody.hubTimezone ? editBody.hubTimezone : facility.data.facility_general_info.timezone_id

        if (settings["timezone_id"] == "00") {
            settings["timezone_id"] = ""
        }

        return settings
    }

    property var action: null
    property var approve: false

    property var initialSettings: null

    Component.onCompleted: {
        editBody.initialSettings = editBody.createSettings(true)
    }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            spacing: 0
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 7
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 18

                ScrollView {
                    id: scrollView
                    clip: true
                    width: editBody.width
                    anchors {
                        top: parent.top
                        right: parent.right
                        bottom: parent.bottom
                    }

                    ScrollBar.vertical.policy: {
                        if (scrollView.contentHeight > scrollView.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }

                    PropertyAnimation {
                        id: scrollBarAnim
                        target: scrollView.ScrollBar.vertical
                        to: 0
                        duration: 300
                        property: "position"
                        property var action: null

                        onFinished: {
                            if (scrollBarAnim.action) {
                                scrollBarAnim.action()
                                scrollBarAnim.action = null
                            }
                        }
                    }

                    ColumnLayout {
                        spacing: 16
                        width: scrollView.parent.width
                        anchors {
                            top: parent.top
                            right: parent.right
                            bottom: parent.bottom
                        }

                        EditBlock {
                            id: objectBlock
                            name: tr.a911_object
                            Layout.topMargin: 44
                            Layout.maximumHeight: 260
                            enabled: blockLoader.item.nameField.enabled || blockLoader.item.numberField.enabled

                            contentData: Component {
                                Item {
                                    anchors.fill: parent

                                    property alias nameField: nameField
                                    property alias numberField: numberField
                                    Connections {
                                        target: app
                                        onUpdateCompanyInfoValidationError: {
                                            if (objectBlock.collapsed) {
                                                objectBlock.blockAnim.start()
                                            }
                                            if (result["2.1"]) {
                                                nameField.valueText.valid = false
                                                nameField.valueText.error = result["2.1"].message
                                            }
                                            if (result["2.2"]) {
                                                numberField.valueText.valid = false
                                                numberField.valueText.error = result["2.2"].message
                                            }
                                        }
                                    }
                                    Custom.TextFieldEdit {
                                        id: nameField

                                        property bool required: enabled

                                        width: parent.width
                                        key: tr.a911_title + (required ? ui.required : "")
                                        valueText.control.maximumLength: 200
                                        value: ""
                                        distance: 12
                                        enabled: editableFields.includes("name")

                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            value = facility.data.facility_general_info ? facility.data.facility_general_info.name : ""
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: numberField

                                        property bool required: enabled

                                        width: parent.width
                                        key: tr.object_number + (required ? ui.required : "")
                                        valueText.control.maximumLength: 10
                                        value: ""
                                        distance: 12
                                        enabled: editableFields.includes("registration_number")

                                        anchors {
                                            top: nameField.bottom
                                            topMargin: 24 - (nameField.valueText.error ? nameField.valueText.errorText.contentHeight + 6 : 0)
                                        }

                                        Component.onCompleted: {
                                            value = facility.data.facility_general_info ? facility.data.facility_general_info.registration_number : ""
                                        }
                                    }
                                }
                            }
                        }

                        EditBlock {
                            id: addressBlock

                            property bool addressRequired: enabled

                            name: tr.address
                            Layout.maximumHeight: blockLoader.item.trueHeight + 100
                            enabled: editableFields.includes("address")

                            contentData: Component {
                                Item {
                                    anchors.fill: parent

                                    property var trueHeight: streetField.valueText.height + countryField.height + cityField.height + 80

                                    property alias streetField: streetField
                                    property alias countryField: countryField
                                    property alias zipCodeField: zipCodeField
                                    property alias cityField: cityField
                                    property alias stateField: stateField

                                    Connections {
                                        target: app
                                        onUpdateCompanyInfoValidationError: {
                                            if (addressBlock.collapsed) {
                                                addressBlock.blockAnim.start()
                                            }
                                            if (result["2.3.5"]) {
                                                streetField.valueText.valid = false
                                                streetField.valueText.error = result["2.3.5"].message
                                            }
                                            if (result["2.3.3"]) {
                                                cityField.valueText.valid = false
                                                cityField.valueText.error = result["2.3.3"].message
                                            }
                                            if (result["2.3.2"]) {
                                                stateField.valueText.valid = false
                                                stateField.valueText.error = result["2.3.2"].message
                                            }
                                        }
                                    }

                                    Custom.TextAreaEdit {
                                        id: streetField
                                        width: parent.width
                                        key: tr.a911_street_house_office + (addressBlock.addressRequired ? ui.required : "")
                                        distance: 12
                                        valueText.maximumLength: 200
                                        valueText.control.wrapMode: Text.WordWrap
                                        valueText.control.verticalAlignment: TextInput.AlignTop
                                        valueText.preferredHeight: 80
                                        valueText.height: valueText.control.contentHeight + 24 < valueText.preferredHeight ? valueText.preferredHeight : valueText.control.contentHeight + 24
                                        valueText.control.height: valueText.control.contentHeight + 24 < valueText.preferredHeight - 8 ? valueText.preferredHeight - 8 : valueText.control.contentHeight + 24
                                        value: ""
                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                value = ""
                                                return
                                            }
                                            var address1 = facility.data.facility_general_info.address.address_line1
                                            var address2 = facility.data.facility_general_info.address.address_line2
                                            if (address1 && address2) {
                                                value = address1 + ", " + address2
                                                return
                                            }
                                            if (address1) {
                                                value = address1
                                                return
                                            }
                                            if (address2) {
                                                value = address2
                                            }
                                            value = ""
                                        }
                                    }

                                    Item {
                                        id: countryField
                                        width: parent.width / 2 - 8
                                        height: countryKeyText.contentHeight + countryValueText.height + 12
                                        anchors {
                                            top: streetField.bottom
                                            topMargin: 24
                                        }

                                        property var value: countryValueText.code
                                        property var originModel: countryValueText.originModel
                                        property var currentFieldValue: countryValueText.currentFieldValue

                                        property alias textField: countryValueText.textLabel

                                        Custom.FontText {
                                            id: countryKeyText
                                            text: tr.country
                                            width: parent.width
                                            color: ui.colors.white
                                            opacity: 0.5
                                            font.pixelSize: 14
                                            font.weight: Font.Light
                                            wrapMode: Text.WordWrap
                                            horizontalAlignment: Text.AlignLeft
                                            anchors {
                                                top: parent.top
                                                left: parent.left
                                            }
                                        }

                                        Custom.CountriesCombobox {
                                            id: countryValueText
                                            width: parent.width
                                            anchors {
                                                top: countryKeyText.bottom
                                                topMargin: 8
                                                left: parent.left
                                            }

                                            Connections {
                                                target: scrollView.ScrollBar.vertical

                                                onPositionChanged: {
                                                    countryValueText.popup.close()
                                                }
                                            }

                                            Component.onCompleted: {
                                                countryValueText.code = facility.data.facility_general_info ? facility.data.facility_general_info.address.country : ""
                                            }
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: zipCodeField
                                        width: parent.width / 2 - 8
                                        key: tr.a911_zip_code
                                        value: ""
                                        distance: 12
                                        valueText.control.maximumLength: 20
                                        anchors {
                                            top: streetField.bottom
                                            topMargin: 24
                                            right: parent.right
                                        }

                                        Component.onCompleted: {
                                            value = facility.data.facility_general_info ? facility.data.facility_general_info.address.zip_code : ""
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: cityField
                                        width: parent.width / 2 - 8
                                        key: tr.city + (addressBlock.addressRequired ? ui.required : "")
                                        value: ""
                                        distance: 12
                                        valueText.control.maximumLength: 100
                                        anchors {
                                            top: countryField.bottom
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            value = facility.data.facility_general_info ? facility.data.facility_general_info.address.city : ""
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: stateField
                                        width: parent.width / 2 - 8
                                        key: tr.a911_region + (addressBlock.addressRequired ? ui.required : "")
                                        valueText.control.maximumLength: 100
                                        value: ""
                                        distance: 12
                                        anchors {
                                            top: zipCodeField.bottom
                                            topMargin: 24
                                            right: parent.right
                                        }

                                        Component.onCompleted: {
                                            value = facility.data.facility_general_info ? facility.data.facility_general_info.address.state : ""
                                        }
                                    }
                                }
                            }
                        }

                        EditBlock {
                            id: contactsBlock
                            name: tr.contacts
                            Layout.maximumHeight: blockLoader.item.trueHeight + 100
                            enabled: blockLoader.item.phonesField.enabled || blockLoader.item.emailsField.enabled

                            contentData: Component {
                                Item {
                                    anchors.fill: parent

                                    property var trueHeight: Math.max(phonesField.height, emailsField.height)

                                    property alias phonesField: phonesField
                                    property alias emailsField: emailsField

                                    enabled: phonesField.enabled || emailsField.enabled

                                    Custom.PhonesEdit {
                                        id: phonesField
                                        maxPhoneNumbers: 5
                                        width: parent.width / 2 - 8
                                        key: tr.phone
                                        distance: 12
                                        withType: false
                                        model: facility.data.facility_general_info ? facility.data.facility_general_info.phone_numbers : []
                                        emptyField: true
                                        enabled: editableFields.includes("phone_numbers")
                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                            left: parent.left
                                        }
                                        Connections {
                                            target: app
                                            onUpdateCompanyInfoValidationError: {
                                                phonesField.errorsResult(result)
                                                if (phonesField.error) {
                                                    scrollBarAnim.to = 0.3
                                                    scrollBarAnim.start()
                                                }
                                            }
                                        }
                                    }

                                    Custom.EmailsEdit {
                                        id: emailsField
                                        maxPhoneNumbers: 5
                                        width: parent.width / 2 - 8
                                        key: "Email"
                                        distance: 12
                                        model: facility.data.facility_general_info ? facility.data.facility_general_info.email_addresses : []
                                        enabled: editableFields.includes("email_addresses")
                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                            right: parent.right
                                        }
                                        Connections {
                                            target: app
                                            onUpdateCompanyInfoValidationError: {
                                                emailsField.errorsResult(result)
                                                if (emailsField.error) {
                                                    scrollBarAnim.to = 0.3
                                                    scrollBarAnim.start()
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        EditBlock {
                            id: securBlock
                            name: tr.a911_security
                            Layout.maximumHeight: securBlock.blockLoader.item.coordinatesField.visible ? 260 : 176
                            enabled: blockLoader.item.coordinatesField.enabled || blockLoader.item.passwordField.enabled

                            contentData: Component {
                                Item {
                                    anchors.fill: parent

                                    property alias coordinatesField: coordinatesField
                                    property alias passwordField: passwordField

                                    Custom.TextFieldEdit {
                                        id: coordinatesField
                                        width: parent.width
                                        valueText.placeHolderText: "0.0, 0.0"
                                        visible: false
                                        key: tr.a911_object_coordinates
                                        value: ""
                                        distance: 12
                                        enabled: editableFields.includes("location")
                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                value = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.location) {
                                                value = ""
                                                return
                                            }
                                            value = facility.data.facility_general_info.location.latitude + ", " + facility.data.facility_general_info.location.longitude
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: passwordField
                                        width: parent.width
                                        key: tr.a911_code_word_for_alarm_cancellation
                                        valueText.control.maximumLength: 50
                                        value: ""
                                        distance: 12
                                        enabled: editableFields.includes("false_alarm_password")
                                        anchors {
                                            top: coordinatesField.visible ? coordinatesField.bottom : parent.top
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            value = facility.data.facility_general_info ? facility.data.facility_general_info.false_alarm_password : ""
                                        }
                                    }
                                }
                            }
                        }

                        EditBlock {
                            id: scheduleBlock
                            name: tr.a911_work_schedule
                            Layout.maximumHeight: blockLoader.item.trueHeight + 100
                            enabled: blockLoader.item.timezoneItem.enabled || blockLoader.item.detectDisarm.enabled

                            contentData: Component {
                                Item {
                                    anchors.fill: parent

                                    property var trueHeight: detectDisarm.checked ? scheduleBody.height : 48
                                    property var disableSaveButton: {
                                        if (!detectDisarm.checked) return false
                                        if (scheduleView.model.length == 0) return true

                                        for (var i = 0; i < scheduleView.model.length; i++) {
                                            if (!scheduleView.itemAtIndex(i)) return false
                                            if (!scheduleView.itemAtIndex(i).emptyDays) return false
                                        }
                                        return true
                                    }

                                    property alias timezoneItem: timezoneItem
                                    property alias detectDisarm: detectDisarm
                                    property alias scheduleModel: scheduleView.model

                                    Item {
                                        id: scheduleBody
                                        width: parent.width
                                        height: detectDisarmItem.height + timezoneItem.height + scheduleView.height + falseFooter.height + 64
                                        clip: true
                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                        }

                                        Rectangle {
                                            id: detectDisarmItem
                                            width: parent.width
                                            height: 40
                                            radius: 10
                                            color: ui.colors.dark1
                                            enabled: editableFields.includes("detect_off_schedule_disarm")
                                            anchors {
                                                top: parent.top
                                            }

                                            Custom.FontText {
                                                text: tr.a911_track_unarmed_disarming
                                                width: parent.width - 64
                                                color: ui.colors.light3
                                                font.pixelSize: 14
                                                font.weight: Font.Light
                                                wrapMode: Text.WordWrap
                                                horizontalAlignment: Text.AlignLeft
                                                anchors {
                                                    left: parent.left
                                                    leftMargin: 16
                                                    verticalCenter: parent.verticalCenter
                                                }
                                            }

                                            Custom.Toggle {
                                                id: detectDisarm

                                                checked: {
                                                    if (!facility.data.facility_general_info) return false
                                                    return facility.data.facility_general_info.detect_off_schedule_disarm
                                                }
                                                anchors {
                                                    top: parent.top
                                                    topMargin: 4
                                                    right: parent.right
                                                }

                                                mouseArea.onClicked: {
                                                    checked = !checked
                                                }
                                            }
                                        }

                                        DateBlock {
                                            id: timezoneItem
                                            width: parent.width
                                            text: tr.a911_object_local_time
                                            date: ""
                                            opacity: 0.5
                                            timezoneMode: true
                                            clearImage.visible: false
                                            visible: detectDisarm.checked
                                            enabled: editableFields.includes("timezone_id")
                                            anchors {
                                                top: detectDisarmItem.bottom
                                                topMargin: 24
                                            }

                                            onClearField: {
                                                currentTimezoneId = ""
                                            }

                                            property var warningShowed: timezoneItem.currentTimezoneId ? true : false

                                            onActiveFocusChanged: {
                                                if (!activeFocus) valid = true
                                            }

                                            property var currentTimezoneId: ""

                                            onCurrentTimezoneIdChanged: {
                                                timezoneItem.date = timezones.find(timezoneItem.currentTimezoneId)
                                            }

                                            dateArea.onClicked: {
                                                Popups.text_popup(tr.information, tr.default_timezone_popup)
                                                timezoneItem.warningShowed = true

                                                /*
                                                timezoneItem.valid = true
                                                function action(zoneId) {
                                                    timezoneItem.currentTimezoneId = zoneId
                                                }
                                                timezonesLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/Timezones.qml", {"action": action, "currentTimezoneId": timezoneItem.currentTimezoneId})
                                                */
                                            }

                                            Connections {
                                                target: timezones

                                                onTimezonesLoaded: {
                                                    if (editBody.hubTimezone) {
                                                        timezoneItem.currentTimezoneId = editBody.hubTimezone
                                                        return
                                                    }

                                                    if (!facility.data.facility_general_info) return
                                                    timezoneItem.currentTimezoneId = facility.data.facility_general_info.timezone_id
                                                }
                                            }

                                            Connections {
                                                target: editBody

                                                onHubTimezoneChanged: {
                                                    if (timezones.length && editBody.hubTimezone) {
                                                        timezoneItem.currentTimezoneId = editBody.hubTimezone
                                                        return
                                                    }

                                                    if (!facility.data.facility_general_info) return
                                                    timezoneItem.currentTimezoneId = facility.data.facility_general_info.timezone_id
                                                }
                                            }

                                            Component.onCompleted: {
                                                if (timezones.length && editBody.hubTimezone) {
                                                    timezoneItem.currentTimezoneId = editBody.hubTimezone
                                                    return
                                                }

                                                if (!facility.data.facility_general_info || !timezones.length) return
                                                timezoneItem.currentTimezoneId = facility.data.facility_general_info.timezone_id
                                            }
                                        }

                                        Rectangle {
                                            id: scheduleDivider
                                            width: parent.width
                                            height: 1
                                            color: ui.colors.white
                                            opacity: 0.1
                                            anchors {
                                                top: timezoneItem.bottom
                                                topMargin: 16
                                            }
                                        }

                                        Item {
                                            id: falseFooter
                                            width: parent.width
                                            height: visible ? 40 : 0
                                            visible: false  // !timezoneItem.currentTimezoneId
                                            anchors {
                                                top: scheduleDivider.bottom
                                                topMargin: 16
                                            }

                                            Rectangle {
                                                width: parent.width
                                                height: 40
                                                radius: height / 2
                                                color: ui.colors.dark1
                                                anchors.bottom: parent.bottom

                                                Image {
                                                    sourceSize.width: 40
                                                    sourceSize.height: 40
                                                    width: 24
                                                    height: 24
                                                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"
                                                    anchors.centerIn: parent

                                                    Custom.HandMouseArea {
                                                        onClicked: {
                                                            timezoneItem.forceActiveFocus(true)
                                                            timezoneItem.valid = false
                                                        }
                                                    }
                                                }
                                            }
                                        }

                                        ListView {
                                            id: scheduleView
                                            width: parent.width
                                            height: contentHeight  // timezoneItem.currentTimezoneId ? contentHeight : 0
                                            spacing: 16
                                            interactive: false
                                            visible: detectDisarm.checked  // && timezoneItem.currentTimezoneId
                                            anchors {
                                                top: scheduleDivider.bottom
                                                topMargin: 16
                                            }

                                            model: {
                                                if (!facility.data.facility_general_info) return []
                                                return util.normalize_schedule(facility.data.facility_general_info.schedule)
                                            }

                                            footer: Item {
                                                width: parent.width
                                                height: scheduleView.model && scheduleView.model.length > 0 ? 56 : 40

                                                Rectangle {
                                                    width: parent.width
                                                    height: 40
                                                    radius: height / 2
                                                    color: ui.colors.dark1
                                                    anchors.bottom: parent.bottom

                                                    Image {
                                                        sourceSize.width: 40
                                                        sourceSize.height: 40
                                                        width: 24
                                                        height: 24
                                                        source: "qrc:/resources/images/icons/control-a-plus-button.svg"
                                                        anchors.centerIn: parent

                                                        Custom.HandMouseArea {
                                                            onClicked: {
                                                                if (!timezoneItem.currentTimezoneId && !timezoneItem.warningShowed) {
                                                                    Popups.text_popup(tr.information, tr.default_timezone_popup)
                                                                    timezoneItem.warningShowed = true

                                                                    /*
                                                                    timezoneItem.forceActiveFocus(true)
                                                                    timezoneItem.valid = false
                                                                    return
                                                                    */
                                                                }
                                                                focus = true
                                                                var newWeekdays = {"weekdays": [], "time": {"from": "00:00", "to": "24:00"}}
                                                                scheduleView.model = scheduleView.model.concat([newWeekdays])
                                                            }
                                                        }
                                                    }
                                                }
                                            }

                                            delegate: Item {
                                                id: scheduleDayDelegate
                                                width: parent.width
                                                height: 40

                                                property var emptyDays: scheduleWeekdays.trueWeekdays.length == 0

                                                RowLayout {
                                                    spacing: 16
                                                    anchors.fill: parent

                                                    Item {
                                                        id: scheduleWeekdays
                                                        Layout.fillWidth: true
                                                        Layout.fillHeight: true

                                                        function updateModel() {
                                                            var scheduleViewVar = scheduleView
                                                            var indexVar = index

                                                            var temp = scheduleViewVar.model.slice(0, indexVar).concat([{"weekdays": trueWeekdays, "time": {"from": fromRectField.bodyText.text, "to": toRectField.bodyText.text}}])
                                                            scheduleViewVar.model = temp.concat(scheduleViewVar.model.slice(indexVar + 1, scheduleViewVar.model.length))
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

                                                        property var trueWeekdays: modelData.weekdays
                                                        property var weekdaysText: ""
                                                        property var weekdaysTextTemplate: ""

                                                        function createDay(dayName, template, locale=Locale.ShortFormat) {
                                                            var temp = application.locale.dayName(weekdaysData[dayName], Locale.ShortFormat)
                                                            var temp = temp.charAt(0).toUpperCase() + temp.slice(1)
                                                            return template.replace(dayName, temp);
                                                        }

                                                        onTrueWeekdaysChanged: {
                                                            weekdaysText = ""
                                                            weekdaysTextTemplate = util.normalize_schedule_display(trueWeekdays)

                                                            for (var i = 0; i < trueWeekdays.length; i++) {
                                                                weekdaysTextTemplate = scheduleWeekdays.createDay(trueWeekdays[i], weekdaysTextTemplate)
                                                            }
                                                            weekdaysText = weekdaysTextTemplate
                                                        }

                                                        Rectangle {
                                                            width: parent.width
                                                            height: 40
                                                            radius: 10
                                                            color: ui.colors.dark1

                                                            Custom.FontText {
                                                                width: parent.width - 24
                                                                height: parent.height
                                                                text: scheduleWeekdays.weekdaysText
                                                                color: ui.colors.white
                                                                opacity: 0.9
                                                                font.pixelSize: 14
                                                                horizontalAlignment: Text.AlignLeft
                                                                verticalAlignment: Text.AlignVCenter
                                                                anchors {
                                                                    left: parent.left
                                                                    leftMargin: 16
                                                                    verticalCenter: parent.verticalCenter
                                                                }
                                                            }

                                                            Custom.Triangle {
                                                                rotation: -90
                                                                anchors {
                                                                    right: parent.right
                                                                    rightMargin: 12
                                                                    verticalCenter: parent.verticalCenter
                                                                }
                                                            }

                                                            Custom.HandMouseArea {
                                                                id: weekdaysArea

                                                                onClicked: {
                                                                    function action() {
                                                                        Popups.schedule_menu_popup(scheduleWeekdays)
                                                                    }
                                                                    var to = (scheduleBlock.y + 100 + scheduleDayDelegate.y) / scrollView.contentHeight
                                                                    to = to + scrollView.ScrollBar.vertical.height / scrollView.contentHeight < 1 ? to : 0.95 - scrollView.ScrollBar.vertical.height / scrollView.contentHeight
                                                                    scrollBarAnim.action = action
                                                                    scrollBarAnim.to = to
                                                                    scrollBarAnim.start()
                                                                }
                                                            }
                                                        }
                                                    }

                                                    Item {
                                                        Layout.minimumWidth: 68
                                                        Layout.maximumWidth: 68
                                                        Layout.fillHeight: true

                                                        Rectangle {
                                                            id: fromRectField
                                                            width: parent.width
                                                            height: 40
                                                            radius: 10
                                                            color: ui.colors.dark1

                                                            property alias bodyText: fromRectFieldText

                                                            Custom.FontText {
                                                                id: fromRectFieldText
                                                                width: parent.width - 24
                                                                height: parent.height
                                                                text: modelData.time.from
                                                                color: ui.colors.white
                                                                opacity: 0.9
                                                                font.pixelSize: 14
                                                                horizontalAlignment: Text.AlignLeft
                                                                verticalAlignment: Text.AlignVCenter
                                                                anchors {
                                                                    left: parent.left
                                                                    leftMargin: 16
                                                                    verticalCenter: parent.verticalCenter
                                                                }
                                                            }

                                                            Custom.HandMouseArea {
                                                                id: weekdaysFromArea
                                                                cursorShape: Qt.IBeamCursor

                                                                onClicked: {
                                                                    Popups.schedule_time_popup(fromRectField, scheduleWeekdays)
                                                                }
                                                            }
                                                        }
                                                    }

                                                    Item {
                                                        Layout.minimumWidth: 68
                                                        Layout.maximumWidth: 68
                                                        Layout.fillHeight: true

                                                        Rectangle {
                                                            id: toRectField
                                                            width: parent.width
                                                            height: 40
                                                            radius: 10
                                                            color: ui.colors.dark1

                                                            property alias bodyText: toRectFieldText

                                                            Custom.FontText {
                                                                id: toRectFieldText
                                                                width: parent.width - 24
                                                                height: parent.height
                                                                text: modelData.time.to
                                                                color: ui.colors.white
                                                                opacity: 0.9
                                                                font.pixelSize: 14
                                                                horizontalAlignment: Text.AlignLeft
                                                                verticalAlignment: Text.AlignVCenter
                                                                anchors {
                                                                    left: parent.left
                                                                    leftMargin: 16
                                                                    verticalCenter: parent.verticalCenter
                                                                }
                                                            }

                                                            Custom.HandMouseArea {
                                                                id: weekdaysToArea
                                                                cursorShape: Qt.IBeamCursor

                                                                onClicked: {
                                                                    Popups.schedule_time_popup(toRectField, scheduleWeekdays)
                                                                }
                                                            }
                                                        }
                                                    }

                                                    Item {
                                                        Layout.minimumWidth: 40
                                                        Layout.maximumWidth: 40
                                                        Layout.fillHeight: true
                                                        Layout.leftMargin: -8

                                                        Image {
                                                            sourceSize.width: 40
                                                            sourceSize.height: 40
                                                            width: 24
                                                            height: 24
                                                            source: "qrc:/resources/images/icons/control-a-minus-button.svg"
                                                            anchors.centerIn: parent

                                                            Custom.HandMouseArea {
                                                                onClicked: {
                                                                    var scheduleViewVar = scheduleView
                                                                    var indexVar = index
                                                                    focus = true
                                                                    scheduleViewVar.model = scheduleViewVar.model.slice(0, indexVar).concat(scheduleViewVar.model.slice(indexVar + 1, scheduleViewVar.model.length))
                                                                }
                                                            }
                                                        }
                                                    }
                                                }

                                                Custom.HandMouseArea {
                                                    visible: !timezoneItem.warningShowed
                                                    onClicked: {
                                                        Popups.text_popup(tr.information, tr.default_timezone_popup)
                                                        timezoneItem.warningShowed = true
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        EditBlock {
                            id: contractBlock
                            name: tr.a911_contract
                            Layout.maximumHeight: blockLoader.item.trueHeight + 100
                            enabled: editableFields.includes("agreement")

                            contentData: Component {
                                Item {
                                    anchors.fill: parent

                                    property var trueHeight: registrationField.height + startDate.height + companyLegalNameField.height + notesField.valueText.height + 112 + (errorText.text ? errorText.height + 6 : 0)

                                    property alias registrationField: registrationField
                                    property alias startDate: startDate
                                    property alias endDate: endDate
                                    property alias companyLegalNameField: companyLegalNameField
                                    property alias notesField: notesField

                                    Connections {
                                        target: app
                                        onUpdateCompanyInfoValidationError: {
                                            if (contractBlock.collapsed) {
                                                contractBlock.blockAnim.start()
                                            }
                                            if (result["2.11.1"]) {
                                                registrationField.valueText.valid = false
                                                registrationField.valueText.error = result["2.11.1"].message
                                            }
                                            if (result["2.11"]) {
                                                startDate.valid = false
                                                endDate.valid = false
                                                errorText.text = result["2.11"].message
                                            }
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: registrationField
                                        width: parent.width
                                        key: tr.a911_contract_number
                                        valueText.control.maximumLength: 10
                                        value: ""
                                        distance: 12
                                        anchors {
                                            top: parent.top
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                value = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement) {
                                                value = ""
                                                return
                                            }
                                            value = facility.data.facility_general_info.agreement.number ? facility.data.facility_general_info.agreement.number : facility.data.facility_general_info.agreement.number
                                            return
                                        }
                                    }

                                    DateBlock {
                                        id: startDate
                                        width: parent.width / 2 - 8
                                        text: tr.a911_date_of_signing
                                        date: ""
                                        anchors {
                                            top: registrationField.bottom
                                            topMargin: 20
                                        }

                                        dateArea.onClicked: {
                                            startDate.valid = true
                                            endDate.valid = true
                                            errorText.text = ""

                                            function action(date) {
                                                startDate.date = date.toLocaleDateString(application.locale, application.shortDateFormat)
                                            }
                                            var selectedDate = startDate.date ? Date.fromLocaleDateString(application.locale, startDate.date, application.shortDateFormat) : ""
                                            var allowFuture = true
                                            Popups.calendar_popup(action, selectedDate, allowFuture)
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                date = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement) {
                                                date = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement.signing_date) {
                                                date = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement.signing_date.seconds) {
                                                date = ""
                                                return
                                            }
                                            var newDate = new Date(facility.data.facility_general_info.agreement.signing_date.seconds * 1000)
                                            date = newDate.toLocaleDateString(application.locale, application.shortDateFormat)
                                        }
                                    }

                                    DateBlock {
                                        id: endDate
                                        width: parent.width / 2 - 8
                                        text: tr.a911_valid_until
                                        date: ""
                                        anchors {
                                            top: registrationField.bottom
                                            topMargin: 20
                                            right: parent.right
                                        }

                                        dateArea.onClicked: {
                                            startDate.valid = true
                                            endDate.valid = true
                                            errorText.text = ""

                                            function action(date) {
                                                endDate.date = date.toLocaleDateString(application.locale, application.shortDateFormat)
                                            }
                                            var selectedDate = endDate.date ? Date.fromLocaleDateString(application.locale, endDate.date, application.shortDateFormat) : ""
                                            var allowFuture = true
                                            Popups.calendar_popup(action, selectedDate, allowFuture)
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                date = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement) {
                                                date = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement.termination_date) {
                                                date = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement.termination_date.seconds) {
                                                date = ""
                                                return
                                            }
                                            var newDate = new Date(facility.data.facility_general_info.agreement.termination_date.seconds * 1000)
                                            date = newDate.toLocaleDateString(application.locale, application.shortDateFormat)
                                        }
                                    }

                                    Custom.FontText {
                                        id: errorText
                                        width: parent.width
                                        height: text ? contentHeight : 0
                                        text: ""
                                        color: ui.colors.red2
                                        font.pixelSize: 12
                                        wrapMode: Text.WordWrap
                                        textFormat: Text.PlainText
                                        anchors {
                                            top: startDate.bottom
                                            topMargin: 6
                                        }
                                    }

                                    Custom.TextFieldEdit {
                                        id: companyLegalNameField
                                        width: parent.width
                                        key: tr.a911_contract_owner
                                        value: ""
                                        valueText.control.maximumLength: 200
                                        distance: 12
                                        anchors {
                                            top: errorText.bottom
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                value = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement) {
                                                value = ""
                                                return
                                            }
                                            value = facility.data.facility_general_info.agreement.companyLegalName
                                        }
                                    }

                                    Custom.TextAreaEdit {
                                        id: notesField
                                        width: parent.width
                                        key: tr.a911_contract_note
                                        distance: 12
                                        valueText.maximumLength: 200
                                        valueText.control.wrapMode: Text.Wrap
                                        valueText.control.verticalAlignment: TextInput.AlignTop
                                        valueText.preferredHeight: 80
                                        valueText.height: valueText.control.contentHeight + 24 < valueText.preferredHeight ? valueText.preferredHeight : valueText.control.contentHeight + 24
                                        valueText.control.height: valueText.control.contentHeight + 24 < valueText.preferredHeight - 8 ? valueText.preferredHeight - 8 : valueText.control.contentHeight + 24
                                        value: ""
                                        anchors {
                                            top: companyLegalNameField.bottom
                                            topMargin: 24
                                        }

                                        Component.onCompleted: {
                                            if (!facility.data.facility_general_info) {
                                                value = ""
                                                return
                                            }
                                            if (!facility.data.facility_general_info.agreement) {
                                                value = ""
                                                return
                                            }
                                            value = facility.data.facility_general_info.agreement.notes
                                        }
                                    }
                                }
                            }
                        }
                        EditBlock {
                            id: notificationBlock
                            name: tr.notifications
                            Layout.maximumHeight: 248
                            property var currentIndex: -1
                            property var customMinutesValue: ""
                            property var checkedSleepMode: false
                            visible: approve
                            contentData: Component {
                                id: notificationBlockComponent
                                Item {
                                    id: detectSleepModeComp
                                    property alias customMinutes: customMinutes
                                    width: parent.width
                                    height: 400
                                    anchors.fill: parent
                                    Rectangle {
                                        id: detectSleepMode
                                        width: parent.width
                                        height: 40
                                        radius: 10
                                        color: ui.colors.dark1
                                        anchors {
                                            top: parent.top
                                        }

                                        Custom.FontText {
                                            text: tr.object_in_sleep_mode
                                            width: parent.width - 64
                                            color: ui.colors.light3
                                            font.pixelSize: 14
                                            font.weight: Font.Light
                                            wrapMode: Text.WordWrap
                                            horizontalAlignment: Text.AlignLeft
                                            anchors {
                                                left: parent.left
                                                leftMargin: 16
                                                verticalCenter: parent.verticalCenter
                                            }
                                        }

                                        Custom.Toggle {
                                            id: detectSleepModeToggle

                                            checked: false
                                            anchors {
                                                top: parent.top
                                                topMargin: 4
                                                right: parent.right
                                            }

                                            mouseArea.onClicked: {
                                                checked = !checked
                                                notificationBlock.checkedSleepMode = checked
                                                if (checked) {
                                                    notificationBlock.currentIndex = 1
                                                } else {
                                                    customMinutes.control.text = ""
                                                    notificationBlock.currentIndex = -1
                                                }
                                            }
                                        }
                                    }
                                    Item {
                                        id: sleepDurationItem
                                        width: parent.width
                                        height: 66

                                        anchors {
                                            top: detectSleepMode.bottom
                                            // qrc:/resources/qml/screens/home/pages/objects/object/EditObject.qml:1249:37: QML QQuickItem: Cannot anchor to an item that isn't a parent or sibling.
                                            // bottom: repeater.bottom
                                            topMargin: 22
                                        }
                                        Custom.FontText {
                                            id: sleepDuration
                                            text: tr.sleep_mode_duration
                                            color: ui.colors.white
                                            opacity: 0.9
                                            height: 20
                                        }

                                        RowLayout {
                                            anchors {
                                                top: sleepDuration.bottom
                                                bottomMargin: 7
                                                left: parent.left
                                                right: parent.right
                                                bottom: parent.bottom
                                            }
                                            spacing: 4

                                            Item {
                                                Layout.minimumWidth: parent.width / 4 - 4
                                                Layout.maximumWidth: parent.width / 4 - 4
                                                Layout.preferredHeight: 40
                                                clip: true

                                                anchors {
                                                    verticalCenter: repeater.delegate.verticalCenter
                                                }

                                                Custom.TextField {
                                                    id: customMinutes
                                                    width: parent.width
                                                    background.height: 39
                                                    background.border.width: (control.activeFocus || !valid) ? 2 : 0

                                                    control.maximumLength: 3
                                                    color: ui.colors.dark1
                                                    placeHolderText: tr.minutes
                                                    enabled: notificationBlock.checkedSleepMode
                                                    anchors {
                                                        verticalCenter: parent.verticalCenter
                                                        verticalCenterOffset: 5
                                                    }
                                                    control.validator: RegExpValidator { regExp: /^([1-9]|[1-9][0-9]|[1-9][0-9][0-9])$/ }

                                                    control.onActiveFocusChanged: {
                                                        if (control.activeFocus) {
                                                            notificationBlock.currentIndex = -1
                                                        }
                                                    }

                                                    control.onTextChanged: {
                                                        notificationBlock.customMinutesValue = control.text
                                                        if (parseInt(control.text) < 1 || parseInt(control.text) > 300) {
                                                            valid = false
                                                            errorCustMinutes.visible = true
                                                            return
                                                        }
                                                        errorCustMinutes.visible = false
                                                    }
                                                }
                                            }


                                            Repeater {
                                                id: repeater
                                                model: [tr.a911_15_minutes, tr.a911_30_minutes, tr.a911_60_minutes]

                                                delegate: Rectangle {
                                                    Layout.minimumWidth: parent.width / 4 - 4
                                                    Layout.maximumWidth: parent.width /  4 - 4
                                                    Layout.minimumHeight: 39
                                                    Layout.maximumHeight: 39

                                                    color: ui.colors.dark1
                                                    radius: 10
                                                    border {
                                                        width: notificationBlock.currentIndex == index ? 2 : 0
                                                        color: notificationBlock.currentIndex == index ? ui.colors.white : "transparent"
                                                    }
                                                    Custom.HandMouseArea {
                                                        anchors.fill: parent
                                                        visible: notificationBlock.checkedSleepMode
                                                        onClicked: {
                                                            errorCustMinutes.visible = false
                                                            notificationBlock.currentIndex = index
                                                            customMinutes.control.focus = false
                                                            customMinutes.control.text = ""
                                                        }
                                                    }

                                                    Custom.FontText {
                                                        color: ui.colors.light3
                                                        text: repeater.model[index]
                                                        anchors {
                                                            verticalCenter: parent.verticalCenter
                                                            horizontalCenter: parent.horizontalCenter
                                                            left: parent.left
                                                            leftMargin: 12
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    Custom.FontText {
                                        id: errorCustMinutes
                                        width: parent.width
                                        text: tr.sleep_mode_duration_may_be
                                        visible: false
                                        color: ui.colors.red2
                                        anchors {
                                            left: parent.left
                                            top: sleepDurationItem.bottom
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.minimumHeight: 72
            Layout.maximumHeight: 72
            color: ui.colors.black

            Item {
                width: 496
                height: parent.height
                anchors.centerIn: parent

                Item {
                    width: parent.width / 2 - 4
                    height: parent.height
                    anchors.left: parent.left

                    Custom.Button {
                        width: parent.width
                        text: tr.save_scenario
                        anchors.centerIn: parent
                        enabledCustom: (
                                !objectBlock.blockLoader.item.nameField.required ||
                                objectBlock.blockLoader.item.nameField.valueText.control.text.length > 0
                            ) && (
                                !objectBlock.blockLoader.item.numberField.required ||
                                objectBlock.blockLoader.item.numberField.valueText.control.text.length > 0
                            ) && (
                                !addressBlock.addressRequired ||
                                addressBlock.blockLoader.item.streetField.valueText.control.text.length > 0 &&
                                addressBlock.blockLoader.item.cityField.valueText.control.text.length > 0 &&
                                addressBlock.blockLoader.item.stateField.valueText.control.text.length > 0
                            ) && !scheduleBlock.blockLoader.item.disableSaveButton


                        onClicked: {
                            parent.forceActiveFocus()

                            if (notificationBlock.customMinutesValue == "" && notificationBlock.currentIndex == -1 && notificationBlock.checkedSleepMode) {
                                notificationBlock.blockLoader.item.customMinutes.valid = false
                                scrollBarAnim.to = 0.85 - scrollView.ScrollBar.vertical.height / scrollView.contentHeight
                                scrollBarAnim.start()
                                return
                            }

                            var newSettings = editBody.createSettings(false)

                            var minutes = 0

                            if (facility.data.company_id === "" &&  notificationBlock.checkedSleepMode) {
                                if (notificationBlock.customMinutesValue) {
                                    minutes = parseInt(notificationBlock.customMinutesValue)
                                } else if (notificationBlock.currentIndex === 0) {
                                    minutes = 15
                                } else if (notificationBlock.currentIndex === 1) {
                                    minutes = 30
                                }  else if (notificationBlock.currentIndex === 2) {
                                    minutes = 60
                                }
                            }

                            app.facility_module.update_facility_general_info(newSettings, editBody.initialSettings, facility.version, minutes)

                            if (editBody.action && minutes === 0) {
                                if (!editBody.approve) editBody.action()
                            }
                        }
                        Connections {
                            target: app.facility_module
                            onUpdateGeneralFacilityInfoSuccess: {
                                if (editBody.action) {
                                    editBody.action()
                                }
                            }
                        }
                    }
                }

                Item {
                    width: parent.width / 2 - 4
                    height: parent.height
                    anchors.right: parent.right

                    Custom.Button {
                        width: parent.width
                        text: tr.cancel
                        transparent: true
                        color: ui.colors.light3
                        anchors.centerIn: parent

                        onClicked: {
                            editObjectLoader.source = ""

                            if (!facility || !facility.id) return
                            app.facility_module.get_current_facility(facility.id)
                        }
                    }
                }
            }
        }

        Connections {
            target: app

            onUpdateCompanyInfoValidationError: {
                if (result["2.1"] || result["2.2"]) {
                    scrollBarAnim.to = 0
                    scrollBarAnim.start()
                    return
                }
                if (result["2.3.5"] || result["2.3.3"] || result["2.3.4"]) {
                    scrollBarAnim.to = 0.14
                    scrollBarAnim.start()
                }
                if (result["2.11.1"] || result["2.11"]) {
                    scrollBarAnim.to = contractBlock.y / scrollView.contentHeight - 0.07
                    scrollBarAnim.start()
                }
                if (result["11"]) DesktopPopups.error_popup(result["11"].message)
                if (result["versioning_error_message"]) {
                    function continue_saving() {
                        parent.forceActiveFocus()

                        if (notificationBlock.customMinutesValue == "" && notificationBlock.currentIndex == -1 && notificationBlock.checkedSleepMode) {
                            notificationBlock.blockLoader.item.customMinutes.valid = false
                            scrollBarAnim.to = 0.85 - scrollView.ScrollBar.vertical.height / scrollView.contentHeight
                            scrollBarAnim.start()
                            return
                        }

                        var newSettings = editBody.createSettings(false)

                        var minutes = 0

                        if (facility.data.company_id === "" &&  notificationBlock.checkedSleepMode) {
                            if (notificationBlock.customMinutesValue) {
                                minutes = parseInt(notificationBlock.customMinutesValue)
                            } else if (notificationBlock.currentIndex === 0) {
                                minutes = 15
                            } else if (notificationBlock.currentIndex === 1) {
                                minutes = 30
                            }  else if (notificationBlock.currentIndex === 2) {
                                minutes = 60
                            }
                        }

                        app.facility_module.update_facility_general_info(newSettings, editBody.initialSettings, 0, minutes)

                        if (editBody.action && minutes === 0) {
                            if (!editBody.approve) editBody.action()
                        }
                    }

                    Popups.facility_versioning_popup(result["versioning_error_message"], continue_saving)
                }
            }
        }
    }

    Loader {
        id: timezonesLoader
        anchors.fill: parent
    }

    Connections {
        target: facility

        onActionSuccess: {
            editObjectLoader.source = ""
        }
    }

    Connections {
        target: app.facility_module

        onUpdateGeneralFacilityInfoSuccess: {
            if (objectsStack.actionAfterInfoUpdate) {
                objectsStack.actionAfterInfoUpdate()
            }
        }
    }

    Custom.BlockLoading {
        startSignals: [timezones.timezonesStartLoading]
        stopSignals: [timezones.timezonesLoaded, timezones.timezonesNotLoaded]
    }

    Component.onDestruction: {
        objectsStack.actionAfterInfoUpdate = null
    }
}

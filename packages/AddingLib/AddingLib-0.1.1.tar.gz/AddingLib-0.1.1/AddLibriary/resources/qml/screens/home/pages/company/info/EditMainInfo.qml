import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Pro
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: editMainInfo

    property string companyLogo: (appCompany.data.company_logo.images.filter(
        (image) => image.resolution == "original"
    )[0] || {"url": ""}).url

    property var confirmationPreset: {
        return {
            "resendCodeTime": 120000,
            "sendCodesTime": {},
            "sendCodesInfo": {},
            "timeDiff": function f(information) {
                var nextTime = confirmationPreset.sendCodesTime[information]
                if (!nextTime) return 0

                var currentTime = new Date()
                currentTime = currentTime.getTime()

                var result = nextTime - currentTime
                return result > 0 ? result : 0
            }
        }
    }
    property var itemToScroll: null

    function checkValid() {
        var valid = true

        for (var index in content.children) {
            var child = content.children[index]

            if (child instanceof DS.InputFieldConflict && child.visible) {
                valid = false
                if (!itemToScroll) itemToScroll = child
            }

            if (
                child instanceof DS.MultiInputField
                || child instanceof DS.MultiInputCountryPhone
                || child instanceof DS.InputField
                || child instanceof DS.InputArea
                || child.objectName == "logoBlock"
            ) if (!child.checkValid()) {
                valid = false
                if (!itemToScroll) itemToScroll = child
            }

            if (child instanceof Custom.CountriesComboboxAlt) {
                if (!child.code && child.required) {
                    child.textLabel.error = tr.field_cant_be_empty
                    child.textLabel.valid = false
                    valid = false
                    if (!itemToScroll) itemToScroll = child
                } else {
                    child.textLabel.error = ""
                    child.textLabel.valid = true
                }
            }

            if (child instanceof Custom.ComboBoxNewAlt) {
                if (!child.currentText) {
                    valid = false
                    if (!itemToScroll) itemToScroll = child
                } else {
                    child.backgroundRectangle.border.width = 0
                }
            }
        }

        if (!valid) scrollTimer.start()

        return valid
    }

    function createSettings(initial, versioning) {
        var settings = {}
        settings["short_name"] = fieldCompanyName.value.trim()
        settings["email_addresses"] = multiFieldCompanyEmailAddHubs.listData

        settings["full_name"] = fieldFullLegalCompanyName.value.trim()
        settings["head_of_company"] = fieldDirectorFio.value.trim()
        settings["registration_number"] = fieldStateDeclarationNumber.value.trim()
        settings["company_type"] = comboboxCompanyType.serverModel[comboboxCompanyType.currentIndex]
        settings["employees_number"] = comboboxNumberEmployees.serverModel[comboboxNumberEmployees.currentIndex]
        settings["technical_emails"] = multiFieldCompanyTechnicalEmail.listData
        settings["legal_address"] = {
            "country": comboboxLegalAddressCountry.code,
            "state": fieldLegalAddressState.value.trim(),
            "city": fieldLegalAddressCity.value.trim(),
            "zip_code": fieldLegalAddressZipCode.value.trim(),
            "address_line1": fieldLegalAddressSHO.value.trim(),
        }
        settings["postal_address"] = {
            "country": comboboxMailAddressCountry.code,
            "state": fieldMailAddressState.value.trim(),
            "city": fieldMailAddressCity.value.trim(),
            "zip_code": fieldMailAddressZipCode.value.trim(),
            "address_line1": fieldMailAddressSHO.value.trim(),
        }
        settings["customer_inquiries_emails"] = multiFieldCompanyPublicEmail.listData
        settings["web_site_url"] = fieldWebsiteUrl.value.trim()
        settings["company_logo"] = {
            "image_id": logoImage.imageId
        }
        settings["phone_numbers"] = multiFieldPhones.collectData()
        settings["country_code"] = comboboxCompanyCountryWork.code
        settings["locations"] = multiFieldCompanyRegionWork.listData

        if (versioning) settings["version"] = 0
        return settings
    }

    color: ui.backgrounds.base

    Timer {
        id: scrollTimer

        interval: 1

        onTriggered: {
            scrollBar.scrollTo(Math.min(Math.max((itemToScroll.y - 20) / content.height, 0), 1 - scrollBar.size))
            itemToScroll = undefined
        }
    }

    DS.ScrollView {
        id: view

        contentHeight: content.height
        bottomInset: 32

        ScrollBar.vertical: DS.ScrollBar {
            id: scrollBar
        }

        Column {
            id: content

            width: 620

            padding: 32

            DS.Text {
                text: tr.a911_general_info
                weight: Font.Bold
                size: 32
                line: 40
                color: ui.colors.base
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldCompanyName

                fieldWidth: 452
                title: tr.field_company_name
                value: appCompany.mc_short_name || companyName
                info: util.hyperlink(tr.tip_company_name_not_editable, "mailto:support@ajax.systems")
                enabled: false
                required: true
            }

            Spacing { height: 32 }

            DS.InputFieldConflict {
                id: multiFieldCompanyEmailAddHubsConflict

                visible: "email_addresses" in conflicts
                propertyName: tr.field_company_email_add_hubs
                valueKey: "email"
                conflictData: conflicts.email_addresses
                info: tr.main_email_editing_conflict_description
                conflictTitle: tr.select_one_several_emails_title
                conflictInfo: tr.select_one_several_emails_description

                onSelected: {
                    multiFieldCompanyEmailAddHubs.listData = values
                    visible = false
                    saveButton.enabled = true
                }
            }

            DS.MultiInputField {
                id: multiFieldCompanyEmailAddHubs

                visible: !multiFieldCompanyEmailAddHubsConflict.visible
                title: tr.field_company_email_add_hubs
                info: tr.main_email_editing_conflict_description
                listData: appCompany.data.email_addresses
                confirmedValues: confirmedEmails
                confirmationError: tr.confirm_email_first
                valueKey: "email"
                required: true
                validator: RegExpValidator { regExp: ui.regexes.email }
                maximumLength: 100
                validatorError: tr.incorrect_email_format_911
                maxCount: 5
                onConfirmationRequest: {
                    list.currentIndex = index
                    if (editMainInfo.confirmationPreset.timeDiff(value) > 0) {
                        var confirmationInfo = editMainInfo.confirmationPreset.sendCodesInfo[value]
                        Popups.confirm_email_popup_alt(confirmationInfo, editMainInfo.confirmationPreset, false)
                    } else {
                        app.company_module.request_new_email_confirmation({"email": value})
                    }
                }

                Connections {
                    target: app.company_module

                    onRequestNewEmailConfirmationFailed: {
                        if (notUnique) {
                            multiFieldCompanyEmailAddHubs.list.currentItem.forcedError = tr.verification_code_email_already_used
                        }
                    }

                    onConfirmNewEmailSuccess: {
                        multiFieldCompanyEmailAddHubs.confirmedValues.push(confirmationInfo.email)
                        multiFieldCompanyEmailAddHubs.confirmedValuesChanged()
                    }
                }
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldFullLegalCompanyName

                fieldWidth: 620
                title: tr.full_legal_company_name
                value: companyFullName
                required: inMarketplace
                minimumLength: 3
                maximumLength: 200
                lengthError: tr.from_3_to_200_characters_911
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldDirectorFio

                fieldWidth: 620
                title: tr.a911_director_fio
                value: directorName
                required: true
                minimumLength: 3
                maximumLength: 200
                lengthError: tr.from_3_to_200_characters_911
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldStateDeclarationNumber

                fieldWidth: 620
                title: tr.a911_state_declaration_number
                value: registrationNumber
                maximumLength: 100
                required: inMarketplace
            }

            Spacing { height: 32 }

            DS.Text {
                text: tr.сompany_type + ui.required
                size: 14
                line: 20
                color: ui.colors.secondary
            }

            Spacing { height: 4 }

            // TODO: REPLACE WITH DS
            Custom.ComboBoxNewAlt {
                id: comboboxCompanyType

                property var readyToSave: currentIndex != serverModel.indexOf(companyType)
                property var serverModel: [
                    "INSTALLATION_COMPANY_OR_INSTALLER",
                    "MONITORING_COMPANY",
                    "SECURITY_COMPANY",
                    "DISTRIBUTOR",
                    "RESELLER_OR_SUB_DISTRIBUTOR",
                    "FIRE_DETECTION_COMPANY",
                    "CORPORATE_CLIENT",
                    "SYSTEM_INTEGRATOR_OR_SECURITY_CONSULTANT",
                    "END_USER",
                    "OTHER"
                ]

                width: parent.width

                currentIndex: serverModel.indexOf(companyType)
                contentColor: ui.colors.base
                backgroundRectangle.border.color: ui.colors.warningContrast
                backgroundRectangle.border.width: companyTypeWarning.visible ? 1 : 0

                model: [
                    tr.company_type_option_installation,
                    tr.company_type_option_cms,
                    tr.company_type_option_mix,
                    tr.distributor,
                    tr.company_type_option_reseller,
                    tr.company_type_option_fire,
                    tr.company_type_option_corporate,
                    tr.company_type_option_intergator,
                    tr.company_type_option_enduser,
                    tr.a911_other_alarm_reason,
                ]

                Component.onCompleted: if (currentIndex == -1) companyTypeWarning.visible = true
                onActivated: companyTypeWarning.visible = false
            }

            Spacing {
                height: 4

                visible: companyTypeWarning.visible
            }

            DS.Text {
                id: companyTypeWarning

                text: tr.popup_company_info_why_need_description
                visible: false
                size: 16
                color: ui.colors.warningContrast
            }

            Spacing { height: 32 }

            DS.Text {
                text: tr.number_of_employees + ui.required
                size: 14
                line: 20
                color: ui.colors.secondary
            }

            Spacing { height: 4 }

            // TODO: REPLACE WITH DS
            Custom.ComboBoxNewAlt {
                id: comboboxNumberEmployees

                property var readyToSave: currentIndex != serverModel.indexOf(employeesNumber)
                property var serverModel: [
                    "EMPLOYEES_NUMBER_1",
                    "EMPLOYEES_NUMBER_2_10",
                    "EMPLOYEES_NUMBER_11_30",
                    "EMPLOYEES_NUMBER_31_50",
                    "EMPLOYEES_NUMBER_51_100",
                    "EMPLOYEES_NUMBER_101_200",
                    "EMPLOYEES_NUMBER_201_300",
                    "EMPLOYEES_NUMBER_301_500",
                    "EMPLOYEES_NUMBER_500_OR_MORE",
                    "EMPLOYEES_NUMBER_UNKNOWN",
                ]

                width: parent.width

                currentIndex: serverModel.indexOf(employeesNumber)
                contentColor: ui.colors.base
                backgroundRectangle.border.color: ui.colors.warningContrast
                backgroundRectangle.border.width: numberEmployeesWarning.visible ? 1 : 0

                model: [
                    "1",
                    "2–10",
                    "11–30",
                    "31–50",
                    "51–100",
                    "101–200",
                    "201–300",
                    "301–500",
                    ">500",
                    tr.na,
                ]

                Component.onCompleted: if (currentIndex == -1) numberEmployeesWarning.visible = true
                onActivated: if (numberEmployeesWarning.visible) numberEmployeesWarning.visible = false
            }

            Spacing {
                height: 4

                visible: numberEmployeesWarning.visible
            }

            DS.Text {
                id: numberEmployeesWarning

                text: tr.popup_company_info_why_need_description
                visible: false
                size: 16
                color: ui.colors.warningContrast
            }

            Spacing { height: 32 }

            DS.MultiInputField {
                id: multiFieldCompanyTechnicalEmail

                title: tr.field_company_technical_email
                listData: appCompany.data.technical_emails
                valueKey: "email"
                maximumLength: 100
                maxCount: 5
                info: tr.info_company_technical_email
                required: inMarketplace
                validator: RegExpValidator { regExp: ui.regexes.email }
                validatorError: tr.incorrect_email_format_911
            }

            Spacing { height: 64 }

            DS.Text {
                text: tr.a911_legal_address
                weight: Font.Bold
                size: 32
                line: 40
                color: ui.colors.base
            }

            Spacing { height: 4 }

            DS.Text {
                text: tr.legal_address_info
                size: 14
                line: 20
                color: ui.colors.secondary
            }

            Spacing { height: 32 }

            DS.Text {
                text: tr.country + (inMarketplace ? ui.required : "")
                size: 14
                line: 20
                color: ui.colors.secondary
            }

            Spacing { height: 4 }

            Custom.CountriesComboboxAlt {
                id: comboboxLegalAddressCountry

                width: 400
                height: 40

                contentColor: ui.colors.base
                code: legalAddress.country
                maxPopupHeight: 300
                badgeImageMargin: 4
                includeWorldwide: false
                textLabel.placeHolderText: ""

                property var readyToSave: code != legalAddress.country
                property var required: inMarketplace
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldLegalAddressState

                fieldWidth: 400
                title: tr.region_911
                value: legalAddress.state
                maximumLength: 100
                required: inMarketplace
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldLegalAddressCity

                fieldWidth: 400
                title: tr.city
                value: legalAddress.city
                maximumLength: 100
                required: inMarketplace
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldLegalAddressZipCode

                fieldWidth: 400
                title: tr.zip_code_911
                value: legalAddress.zip_code
                maximumLength: 20
                required: inMarketplace
            }

            Spacing { height: 32 }

            DS.InputArea {
                id: fieldLegalAddressSHO

                areaWidth: 400
                required: inMarketplace
                title: tr.street_house_office_tip
                value: (legalAddress.address_line1 + "\n" + legalAddress.address_line2).trim()
                minimumLength: 3
                maximumLength: 200
                lengthError: tr.from_3_to_200_characters_911
            }

            Column {
                width: parent.width

                visible: !inMarketplace

                property var readyToSave: (
                    comboboxMailAddressCountry.readyToSave
                    || fieldMailAddressState.readyToSave
                    || fieldMailAddressCity.readyToSave
                    || fieldMailAddressZipCode.readyToSave
                    || fieldMailAddressSHO.readyToSave
                )

                Spacing { height: 64 }

                DS.Text {
                    text: tr.a911_mail_address
                    weight: Font.Bold
                    size: 32
                    line: 40
                    color: ui.colors.base
                }

                Spacing { height: 4 }

                DS.Text {
                    text: tr.mail_address_info
                    size: 14
                    line: 20
                    color: ui.colors.secondary
                }

                Spacing { height: 32 }

                DS.Checkbox {
                    id: mailLegalAddressMatchesCheckbox

                    text: tr.mail_legal_adress_matches
                    checked: JSON.stringify(mailAddress) == JSON.stringify(legalAddress)
                }

                Spacing { height: 32 }

                DS.Text {
                    text: tr.country
                    size: 14
                    line: 20
                    color: ui.colors.secondary
                }

                Spacing { height: 4 }

                Custom.CountriesComboboxAlt {
                    id: comboboxMailAddressCountry

                    width: 400
                    height: 40

                    contentColor: ui.colors.base
                    code: mailLegalAddressMatchesCheckbox.checked ? comboboxLegalAddressCountry.code : mailAddress.country
                    maxPopupHeight: 300
                    badgeImageMargin: 4
                    includeWorldwide: false
                    textLabel.placeHolderText: ""
                    opacity: enabled ? 1 : 0.3
                    enabled: !mailLegalAddressMatchesCheckbox.checked

                    property var readyToSave: code != mailAddress.country
                }

                Spacing { height: 32 }

                DS.InputField {
                    id: fieldMailAddressState

                    fieldWidth: 400
                    title: tr.region_911
                    value: mailLegalAddressMatchesCheckbox.checked ? fieldLegalAddressState.value : mailAddress.state
                    enabled: !mailLegalAddressMatchesCheckbox.checked
                    maximumLength: 100
                }

                Spacing { height: 32 }

                DS.InputField {
                    id: fieldMailAddressCity

                    fieldWidth: 400
                    title: tr.city
                    value: mailLegalAddressMatchesCheckbox.checked ? fieldLegalAddressCity.value : mailAddress.city
                    enabled: !mailLegalAddressMatchesCheckbox.checked
                    maximumLength: 100
                }

                Spacing { height: 32 }

                DS.InputField {
                    id: fieldMailAddressZipCode

                    fieldWidth: 400
                    title: tr.zip_code_911
                    value: mailLegalAddressMatchesCheckbox.checked ? fieldLegalAddressZipCode.value : mailAddress.zip_code
                    enabled: !mailLegalAddressMatchesCheckbox.checked
                    maximumLength: 20
                }

                Spacing { height: 32 }

                DS.InputArea {
                    id: fieldMailAddressSHO

                    areaWidth: 400
                    title: tr.street_house_office_tip
                    value: mailLegalAddressMatchesCheckbox.checked ? fieldLegalAddressSHO.value : (mailAddress.address_line1 + "\n" + legalAddress.address_line2).trim()
                    enabled: !mailLegalAddressMatchesCheckbox.checked
                    minimumLength: 3
                    maximumLength: 200
                    lengthError: tr.from_3_to_200_characters_911
                }
            }

            Spacing { height: 64 }

            DS.Text {
                text: tr.public_pro_desktop_title
                weight: Font.Bold
                size: 32
                line: 40
                color: ui.colors.base
            }

            Spacing { height: 4 }

            DS.Text {
                text: tr.public_pro_desktop_info
                size: 14
                line: 20
                color: ui.colors.secondary
            }

            Spacing { height: 32 }

            DS.MultiInputField {
                id: multiFieldCompanyPublicEmail

                title: tr.field_company_public_email
                listData: appCompany.data.customer_inquiries_emails

                maxCount: 5
                valueKey: "email"
                maximumLength: 100
                required: inMarketplace
                validator: RegExpValidator { regExp: ui.regexes.email }
                validatorError: tr.incorrect_email_format_911
            }

            Spacing { height: 32 }

            DS.InputFieldConflict {
                id: multiFieldPhonesConflict

                propertyName: tr.company_phone_number
                visible: "phone_numbers" in conflicts
                valueKey: "number"
                conflictData: conflicts.phone_numbers
                conflictTitle: tr.select_one_several_phones_title
                conflictInfo: tr.select_one_several_phones_description

                onSelected: {
                    multiFieldPhones.listData = values
                    multiFieldPhones.guessCountryCodes()
                    visible = false
                    saveButton.enabled = true
                }
            }

            DS.MultiInputCountryPhone {
                id: multiFieldPhones

                required: inMarketplace
                visible: !multiFieldPhonesConflict.visible
                title: tr.company_phone_number
                defaultCountry: countryCode
                listData: appCompany.data.phone_numbers
                maxCount: 5
            }

            Spacing { height: 32 }

            DS.InputField {
                id: fieldWebsiteUrl

                title: tr.website
                info: tr.website_format_tip_desktop
                isJointBottomText: true
                value: websiteUrl
                regex: ui.regexes.websiteUrl
                validatorError: tr.wrong_website_desktop
                minimumLength: 3
                maximumLength: 100
                lengthError: tr.from_3_to_100_characters_911
            }

            Spacing { height: 32 }

            Item {
                id: logoBlock

                objectName: "logoBlock"

                property alias logoImage: logoImage
                property var readyToSave: logoImage.imageId != appCompany.data.company_logo.image_id
                property var required: inMarketplace

                function checkValid() {
                    if (logoBlock.required && logoImage.imageId == "") {
                        logoImage.error()
                        logoError.visible = true
                        return false
                    }
                    return true
                }

                width: parent.width
                height: childrenRect.height

                DS.Text {
                    id: logoTitle

                    text: logoBlock.required ? tr.a911_logo + ui.required : tr.a911_logo
                    size: 14
                    line: 20
                    color: ui.colors.secondary
                }

                DS3.CompanyImageUpload {
                    id: logoImage

                    property var imageId: appCompany.data.company_logo.image_id

                    anchors {
                        top: logoTitle.bottom
                        topMargin: 12
                    }

                    imageRect.source: companyLogo

                    uploadSwitchChecked: () => {
                        imageFileDialog.target = imageRect
                        imageFileDialog.isRounded = false
                        imageFileDialog.open()

                        sheetAction.close()
                    }
                    deleteSwitchChecked: () => {
                        logoImage.imageId = ""
                        imageRect.source = ""
                        imageRect.imageData = null
                        sheetAction.close()
                    }
                }

                DS.Text {
                    id: logoError

                    anchors {
                        top: logoImage.top
                        left: logoImage.right
                        leftMargin: 16
                    }

                    text: tr.logo_is_required
                    visible: false
                    size: 14
                    line: 20

                    color: ui.colors.attention
                }

                DS.Text {
                    width: 300

                    anchors {
                        top: logoImage.top
                        topMargin: logoError.visible ? 24 : 0
                        left: logoImage.right
                        leftMargin: 16
                    }

                    text: tr.a911_drag_and_drop
                    size: 14
                    line: 20
                    color: ui.colors.secondary
                }
            }

            Spacing { height: 32 }

            DS.Text {
                text: tr.field_company_country_work + ui.required
                size: 14
                line: 20
                color: ui.colors.secondary
            }

            Spacing { height: 4 }

            // TODO: REPLACE WITH DS
            Custom.CountriesComboboxAlt {
                id: comboboxCompanyCountryWork

                width: 400
                height: 40

                contentColor: ui.colors.base
                code: countryCode
                maxPopupHeight: 300
                badgeImageMargin: 4
                includeWorldwide: false
                textLabel.placeHolderText: ""
                enabled: !countryCode

                property var readyToSave: code != countryCode
            }

            Spacing { height: 32 }

            DS.MultiInputField {
                id: multiFieldCompanyRegionWork

                title: tr.field_company_region_work
                listData: appCompany.data.locations
                warningText: tr.popup_company_info_why_need_description
                warning: listData.length == 0
                required: true
                minimumLength: 2
                maximumLength: 100
                lengthError: tr.min_length.replace("{0}", minimumLength)
                maxCount: 50
            }

            Spacing { height: 70 }

            Row {
                id: saveCancelBlock

                width: parent.width
                height: saveButton.height

                spacing: 16

                DS3.ButtonContained {
                    id: saveButton

                    implicitWidth: 220
                    text: tr.a911_save_changes
                    enabled: {
                        var valid = false
                        for (var index in content.children) {
                            var child = content.children[index]
                            if (
                                typeof(child.readyToSave) != "undefined"
                                || child instanceof Item && child.logoImage
                            ) valid = valid || child.readyToSave
                        }
                        return valid
                    }

                    onClicked: {
                        forceActiveFocus()
                        if (checkValid()) {
                            application.debug("company -> company info -> edit general info -> save")
                            var newSettings = editMainInfo.createSettings(false, false)
                            app.company_module.update_company(appCompany, newSettings, [])
                        }
                    }
                }

                DS3.ButtonOutlined {
                    implicitWidth: 164
                    text: tr.cancel
                    isAttention: true

                    onClicked: {
                        application.debug("company -> company info -> edit general info -> cancel")
                        editInfoLoader.setSource("")
                        companyStack.companyEditMode = false
                    }
                }
            }
        }
    }

    Connections {
        target: app.company_module

        onUploadCompanyLogoSuccess: {
            logoImage.imageRect.source = logo_url
            logoImage.imageId = image_id
        }

        onSaveCompanyValidationErrors: {
            for (var phoneErrorKey of Object.keys(result).filter((name) => /20/.test(name))) {
                var index = phoneErrorKey.match(/\[(\d)\]/)[1]
                var phoneField = multiFieldPhones.get(index)
                if (!itemToScroll) itemToScroll = multiFieldPhones
                phoneField.forcedError = result[phoneErrorKey].message
            }

            if (result["31"]) {
                if (!itemToScroll) itemToScroll = fieldWebsiteUrl
                fieldWebsiteUrl.forcedError = result["31"].message
            }

            if (itemToScroll) scrollTimer.start()

            if (result["versioning_error_message"]) {
                function continue_saving() {
                    var newSettings = editMainInfo.createSettings(false, true)
                    app.company_module.update_company(appCompany, newSettings, [])
                }

                Popups.facility_versioning_popup(result["versioning_error_message"], continue_saving)
            }
        }

        onRequestNewEmailConfirmationSuccess: {
            var date = new Date()

            editMainInfo.confirmationPreset.sendCodesTime[confirmationInfo.email] = date.getTime() + editMainInfo.confirmationPreset.resendCodeTime
            editMainInfo.confirmationPreset.sendCodesInfo[confirmationInfo.email] = confirmationInfo

            Popups.confirm_email_popup_alt(confirmationInfo, editMainInfo.confirmationPreset, false)
        }
    }

    Connections {
        target: appCompany

        onSaveSuccess: {
            editInfoLoader.setSource("")
            companyStack.companyEditMode = false
        }
    }
}

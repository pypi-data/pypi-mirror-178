import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: companyCreateScreen

    property var companies: null
    property var companyName: ""
    property var countryCode: ""

    property var companyInfo: null

    function collectUserData() {
        var settings = {}

        settings["provided_services"] = createScreenServices.itemLoader.item.value
        settings["short_name"] = createScreenCompanyName.itemLoader.item.value
        settings["email_addresses"] = createScreenMainEmail.itemLoader.item.value
        settings["head_of_company"] = createScreenCeoName.itemLoader.item.value
        settings["company_type"] = createScreenCompanyType.itemLoader.item.value
        settings["employees_number"] = createScreenEmployees.itemLoader.item.value
        settings["phone_numbers"] = createScreenNumbers.itemLoader.item.value
        settings["country_code"] = createScreenCountry.itemLoader.item.value
        settings["locations"] = createScreenRegion.itemLoader.item.value

        return settings
    }

    Connections {
        target: companyStack

        onMakeCreateCompanyRequest: {
            createScreenCreate.itemLoader.item.createScreenCreateButton.clicked(true)
        }
    }

    ScrollView {
        id: scrollView

        clip: true
        width: parent.width

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
        }

        Column {
            width: companyCreateScreen.width

            Desktop.ColumnItem {
                id: createScreenHeader

                margin: 48

                contentItem: Component {
                    Item {
                        height: createScreenHeaderText.contentHeight

                        Desktop.NormalText {
                            id: createScreenHeaderText

                            text: tr.company_creation_title
                            color: ui.colors.light3
                            size: 32
                            bold: true

                            anchors.fill: parent
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenTip

                margin: 64

                contentItem: Component {
                    Item {
                        height: createScreenTipText.contentHeight

                        Desktop.NormalText {
                            id: createScreenTipText

                            text: tr.function_pro_desktop_title
                            color: ui.colors.light3
                            size: 24
                            bold: true

                            anchors.fill: parent
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenServices

                margin: 32

                contentItem: Component {
                    Item {
                        height: Math.max(monitoringService.originalHeight, installationService.originalHeight)

                        property var value: {
                            return {
                                "installation": installationService.selected,
                                "monitoring": monitoringService.selected,
                                "reaction": false,
                            }
                        }

                        property var valid: monitoringService.selected || installationService.selected

                        Desktop.CompanyService {
                            id: monitoringService

                            enabled: true

                            width: parent.width / 2 - 8
                            height: parent.height

                            anchors.left: parent.left

                            selected: false
                            comingSoon: false
                            title: tr.alarm_monitoring

                            reasons: [
                                tr.function_monitoring_desc1,
                                tr.function_monitoring_desc2,
                                tr.function_monitoring_desc3,
                                tr.function_monitoring_desc4,
                                tr.function_monitoring_desc5,
                            ]

                            onToggle: {
                                monitoringService.selected = !monitoringService.selected
                            }
                        }

                        Desktop.CompanyService {
                            id: installationService

                            enabled: true

                            width: parent.width / 2 - 8
                            height: parent.height

                            anchors.right: parent.right

                            selected: false
                            comingSoon: false
                            title: tr.installation_and_maintenance

                            reasons: [
                                tr.function_installation_desc1,
                                tr.function_installation_desc2,
                                tr.function_installation_desc3,
                                tr.function_installation_desc4,
                            ]

                            onToggle: {
                                installationService.selected = !installationService.selected
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenInfo

                margin: 64

                contentItem: Component {
                    Item {
                        height: createScreenInfoText.contentHeight

                        Desktop.NormalText {
                            id: createScreenInfoText

                            text: tr.about_company
                            color: ui.colors.light3
                            size: 24
                            bold: true

                            anchors.fill: parent
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenCompanyName

                margin: 32

                contentItem: Component {
                    Item {
                        height: 70

                        property var value: createScreenCompanyNameField.valueText.control.text.trim()

                        property var valid: value.length >= 2 && value.length <= 100

                        Custom.TextFieldEdit {
                            id: createScreenCompanyNameField

                            width: parent.width * 0.7
                            key: tr.field_company_name + ui.required
                            distance: 12

                            value: companyCreateScreen.companyName
                            enabled: false
                            opacity: enabled ? 1 : 0.5

                            valueText.control.maximumLength: 100

                            keyText {
                                opacity: 1
                                color: ui.colors.secondary
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenMainEmail

                margin: 32

                contentItem: Component {
                    Item {
                        height: 70 + createScreenMainEmailFieldHint.contentHeight + 4

                        property var value: {
                            return [{
                                "email": createScreenMainEmailField.valueText.control.text.trim(),
                                "confirmed": true,
                            }]
                        }

                        property var valid: {
                            return value[0].email.length > 0
                        }

                        Desktop.ToolTip {
                            text: tr.hover_company_email_add_hubs
                            visible: createScreenMainEmailField.valueText.control.activeFocus
                        }

                        Custom.TextFieldEdit {
                            id: createScreenMainEmailField

                            width: parent.width * 0.7
                            key: tr.field_company_email_add_hubs + ui.required
                            distance: 12

                            valueText.control.maximumLength: 100
                            valueText.control.validator: RegExpValidator { regExp: /^[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я+]+)*@[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я]+)*(\.[0-9a-zA-Zа-яА-Я]{2,10})+$/ }

                            value: {
                                if (!companyCreateScreen.companyInfo) return ""
                                if (!companyCreateScreen.companyInfo.companyData) return ""
                                if (!companyCreateScreen.companyInfo.companyData.email_addresses) return ""
                                if (!companyCreateScreen.companyInfo.companyData.email_addresses[0]) return ""
                                if (!companyCreateScreen.companyInfo.companyData.email_addresses[0].email) return ""

                                return companyCreateScreen.companyInfo.companyData.email_addresses[0].email
                            }

                            keyText {
                                opacity: 1
                                color: ui.colors.secondary
                            }
                        }

                        Desktop.NormalText {
                            id: createScreenMainEmailFieldHint

                            width: parent.width * 0.7
                            text: createScreenMainEmailField.valueText.valid ? tr.company_email_add_hubs_new_tip : createScreenMainEmailFieldHint.errorText
                            color: createScreenMainEmailField.valueText.valid ? ui.colors.middle3 : ui.colors.red1

                            property var errorText: ""

                            anchors {
                                top: createScreenMainEmailField.bottom
                                topMargin: 4
                                left: parent.left
                            }
                        }

                        Connections {
                            target: app.company_module

                            onRequestNewEmailConfirmationFailed: {
                                if (notUnique) {
                                    createScreenMainEmailFieldHint.errorText = tr.verification_code_email_already_used
                                    createScreenMainEmailField.valueText.valid = false

                                    var scrollTo = createScreenMainEmail.y / scrollView.contentHeight - 0.15
                                    scrollBarAnim.to = scrollTo > 0 ? scrollTo : 0
                                    scrollBarAnim.start()
                                }
                            }

                            onCompanyValidationErrors: {
                                if (result["1"]) {
                                    createScreenMainEmailFieldHint.errorText = result["1"].message
                                    createScreenMainEmailField.valueText.valid = false

                                    var scrollTo = createScreenMainEmail.y / scrollView.contentHeight - 0.15
                                    scrollBarAnim.to = scrollTo > 0 ? scrollTo : 0
                                    scrollBarAnim.start()
                                }
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenCeoName

                margin: 32

                contentItem: Component {
                    Item {
                        height: createScreenCeoNameField.height

                        property var value: createScreenCeoNameField.valueText.control.text.trim()

                        property var valid: value.length >= 3 && value.length <= 200

                        Desktop.ToolTip {
                            text: tr.hover_director_fio
                            visible: createScreenCeoNameField.valueText.control.activeFocus
                        }

                        Custom.TextFieldEdit {
                            id: createScreenCeoNameField

                            width: parent.width
                            key: tr.a911_director_fio + ui.required
                            distance: 12

                            value: {
                                if (!companyCreateScreen.companyInfo) return ""
                                if (!companyCreateScreen.companyInfo.companyData) return ""
                                if (!companyCreateScreen.companyInfo.companyData.head_of_company) return ""

                                return companyCreateScreen.companyInfo.companyData.head_of_company
                            }

                            keyText {
                                opacity: 1
                                color: ui.colors.secondary
                            }

                            valueText {
                                errorMargin: 12
                                errorPixelSize: 14
                                errorTextColor: ui.colors.red1
                                control.maximumLength: 200
                            }
                        }

                        Connections {
                            target: app.company_module

                            onCompanyValidationErrors: {
                                if (result["2.7"]) {
                                    createScreenCeoNameField.valueText.error = result["2.7"].message
                                    createScreenCeoNameField.valueText.valid = false

                                    var scrollTo = createScreenCeoName.y / scrollView.contentHeight - 0.15
                                    scrollBarAnim.to = scrollTo > 0 ? scrollTo : 0
                                    scrollBarAnim.start()
                                }
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenCompanyType

                margin: 32

                contentItem: Component {
                    Item {
                        height: 70

                        property var value: createScreenCompanyTypeCombo.serverModel[createScreenCompanyTypeCombo.currentIndex]

                        property var valid: createScreenCompanyTypeCombo.currentIndex >= 0

                        Desktop.ToolTip {
                            text: tr.choose_one_posible
                            visible: createScreenCompanyTypeCombo.comboPopup.opened
                        }

                        Desktop.NormalText {
                            id: createScreenCompanyTypeText

                            text: tr.сompany_type + ui.required
                            color: ui.colors.middle1

                            width: parent.width
                            textFormat: Text.RichText

                            anchors.top: parent.top
                        }

                        Custom.ComboBoxNew {
                            id: createScreenCompanyTypeCombo

                            width: parent.width
                            model: userModel

                            anchors {
                                top: createScreenCompanyTypeText.bottom
                                topMargin: 6
                            }

                            currentIndex: {
                                if (!companyCreateScreen.companyInfo) return 0
                                if (!companyCreateScreen.companyInfo.companyData) return 0
                                if (!companyCreateScreen.companyInfo.companyData.company_type) return 0

                                if (companyCreateScreen.companyInfo.companyData.company_type == "NO_COMPANY_TYPE_INFO") return 0

                                return serverModel.indexOf(companyCreateScreen.companyInfo.companyData.company_type)
                            }

                            property var userModel: [
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
                                "OTHER",
                            ]
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenEmployees

                margin: 32

                contentItem: Component {
                    Item {
                        height: 70

                        property var value: createScreenEmployeesCombo.serverModel[createScreenEmployeesCombo.currentIndex]

                        property var valid: createScreenEmployeesCombo.currentIndex >= 0

                        Desktop.NormalText {
                            id: createScreenEmployeesText

                            text: tr.number_of_employees + ui.required
                            color: ui.colors.middle1

                            width: parent.width
                            textFormat: Text.RichText

                            anchors.top: parent.top
                        }

                        Custom.ComboBoxNew {
                            id: createScreenEmployeesCombo

                            width: parent.width * 0.3
                            model: userModel

                            anchors {
                                top: createScreenEmployeesText.bottom
                                topMargin: 6
                            }

                            currentIndex: {
                                if (!companyCreateScreen.companyInfo) return 0
                                if (!companyCreateScreen.companyInfo.companyData) return 0
                                if (!companyCreateScreen.companyInfo.companyData.employees_number) return 0

                                if (companyCreateScreen.companyInfo.companyData.employees_number == "NO_EMPLOYEES_NUMBER_INFO") return 0

                                return serverModel.indexOf(companyCreateScreen.companyInfo.companyData.employees_number)
                            }

                            property var userModel: [
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
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenNumbers

                margin: 32

                contentItem: Component {
                    Item {
                        height: createScreenCountryPhones.height

                        property var value: createScreenCountryPhones.itemsCollection
                        property var phoneNumbers: createScreenCountryPhones.phoneNumbers

                        property var valid: {
                            for (var i = 0; i < phoneNumbers.length; i++) {
                                var item = phoneNumbers[i].phoneField.trim()
                                if (item.length < createScreenCountryPhones.fieldMinLength || item.length > 30) return false
                            }
                            return true
                        }

                        Desktop.ToolTip {
                            text: tr.hover_company_phone_number
                            visible: createScreenCountryPhones.active
                        }

                        Desktop.CountryPhones {
                            id: createScreenCountryPhones

                            key: tr.company_phone_number + ui.required
                            defaultCountry: createScreenCountry.itemLoader.item.value

                            maxCount: 5
                            distance: 12
                            fieldDistance: 12

                            fieldMinLength: 3
                            atLeastOneField: true
                            useDescription: true
                            useFooter: itemsCollection.length == 0
                            errorProperty: "2.20"

                            keyText {
                                width: parent.width
                                textFormat: Text.RichText
                            }

                            model: {
                                if (!companyCreateScreen.companyInfo) return []
                                if (!companyCreateScreen.companyInfo.phoneNumbers) return []

                                return companyCreateScreen.companyInfo.phoneNumbers
                            }

                            plusItemVisible: {
                                for (var i = 0; i < phoneNumbers.length; i++) {
                                    var item = phoneNumbers[i].phoneField.trim()
                                    if (item.length < createScreenCountryPhones.fieldMinLength) return false
                                }
                                return true
                            }
                        }

                        Connections {
                            target: app.company_module

                            onCompanyValidationErrors: {
                                createScreenCountryPhones.errorResult(result)
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenCountry

                margin: 32

                contentItem: Component {
                    Item {
                        height: 72

                        enabled: false

                        property var value: createScreenCountryCombo.code

                        property var valid: value != ""

                        Desktop.NormalText {
                            id: createScreenCountryText

                            enabled: parent.enabled
                            opacity: enabled ? 1 : 0.5

                            text: tr.field_company_country_work + ui.required
                            color: ui.colors.secondary

                            width: parent.width
                            textFormat: Text.RichText
                        }

                        Custom.CountriesCombobox {
                            id: createScreenCountryCombo

                            width: parent.width * 0.3

                            enabled: parent.enabled
                            opacity: enabled ? 1 : 0.5

                            code: companyCreateScreen.countryCode
                            maxPopupHeight: 300
                            badgeImageMargin: 4
                            includeWorldwide: false
                            textLabel.placeHolderText: ""

                            anchors {
                                top: createScreenCountryText.bottom
                                topMargin: 8
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenRegion

                margin: 32

                contentItem: Component {
                    Item {
                        height: createScreenLocationsEdit.height

                        property var value: createScreenLocationsEdit.itemsCollection

                        property var valid: {
                            for (var i = 0; i < value.length; i++) {
                                var item = value[i].trim()
                                if (item.length < 2 || item.length > 200) return false
                            }
                            return true
                        }

                        Desktop.ToolTip {
                            text: tr.hover_company_region_work
                            visible: createScreenLocationsEdit.multiFieldActive
                        }

                        Desktop.MultiField {
                            id: createScreenLocationsEdit

                            width: parent.width * 0.58
                            key: tr.field_company_region_work + ui.required

                            maxCount: 50
                            distance: 12
                            useFooter: false
                            fieldDistance: 12
                            maximumLength: 100
                            atLeastOneField: true

                            keyText {
                                width: parent.width
                                textFormat: Text.RichText
                            }

                            model: {
                                if (!companyCreateScreen.companyInfo) return []
                                if (!companyCreateScreen.companyInfo.companyData) return []
                                if (!companyCreateScreen.companyInfo.companyData.locations) return []

                                return companyCreateScreen.companyInfo.companyData.locations
                            }

                            plusItemVisible: {
                                for (var i = 0; i < itemsCollection.length; i++) {
                                    var item = itemsCollection[i].trim()
                                    if (item.length < 2 || item.length > 200) return false
                                }
                                return true
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenAgree

                margin: 48

                contentItem: Component {
                    Item {
                        height: Math.max(32, createScreenAgreeText.contentHeight)

                        property var value: createScreenAgreeCheckbox.selected

                        property var valid: value

                        Item {
                            id: createScreenAgreeCheckbox

                            width: 24
                            height: 24

                            anchors {
                                left: parent.left
                                verticalCenter: parent.verticalCenter
                            }

                            property var selected: {
                                if (!companyCreateScreen.companyInfo) return false
                                if (!companyCreateScreen.companyInfo.agreement) return false

                                return companyCreateScreen.companyInfo.agreement
                            }

                            Image {
                                source: "qrc:/resources/images/pro/company/selected.svg"
                                sourceSize.width: 24
                                sourceSize.height: 20

                                visible: createScreenAgreeCheckbox.selected

                                anchors {
                                    top: parent.top
                                    topMargin: 2
                                    left: parent.left
                                }
                            }

                            Rectangle {
                                width: 24
                                height: 24
                                radius: 4
                                color: "transparent"

                                visible: !createScreenAgreeCheckbox.selected

                                border {
                                    width: 2
                                    color: createScreenAgreeCheckbox.enabled ? ui.colors.middle1 : ui.colors.middle4
                                }

                                anchors {
                                    top: parent.top
                                    left: parent.left
                                }
                            }

                            Custom.HandMouseArea {
                                onClicked: {
                                    createScreenAgreeCheckbox.forceActiveFocus()
                                    createScreenAgreeCheckbox.selected = !createScreenAgreeCheckbox.selected
                                }
                            }
                        }

                        Custom.FontText {
                            id: createScreenAgreeText

                            width: parent.width - 36
                            text: tr.i_have_read_and_agree + ": " + "<a style='text-decoration:none' href='agreement'>" + util.colorize(tr.a911_terms_of_use, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='privacy'>" + util.colorize(tr.a911_privacy_policy, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='license'>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.colors.green1) + "</a>"
                            color: ui.colors.middle1
                            opacity: 0.9

                            font.pixelSize: 15
                            wrapMode: Text.Wrap
                            textFormat: Text.RichText
                            verticalAlignment: Text.AlignVCenter

                            anchors {
                                left: createScreenAgreeCheckbox.right
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }

                            onLinkActivated: {
                                var locale = tr.get_locale()
                                locale = locale == "uk" ? "ua" : locale
                                locale = locale == "pt_PT" ? "pt" : locale

                                if (link == "agreement") {
                                    link = "https://ajax.systems/" + locale + "/end-user-agreement/"
                                    Qt.openUrlExternally(link)
                                    return
                                }

                                if (link == "privacy") {
                                    link = "https://ajax.systems/" + locale + "/privacy-policy/"
                                    Qt.openUrlExternally(link)
                                    return
                                }

                                if (link == "license") {
                                    link = "https://ajax.systems/" + locale + "/ajax-pro-agreement/"
                                    Qt.openUrlExternally(link)
                                    return
                                }
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                id: createScreenCreate

                margin: 32

                contentItem: Component {
                    Item {
                        height: 48

                        property alias createScreenCreateButton: createScreenCreateButton

                        Item {
                            width: createScreenCreateItem.width
                            height: 48

                            Item {
                                id: createScreenCreateItem

                                width: createScreenCreateButton.textButton.contentWidth + 64
                                height: parent.height

                                Custom.Button {
                                    id: createScreenCreateButton

                                    width: parent.width
                                    text: tr.a911_create_company
                                    textButton.textFormat: Text.PlainText
                                    loading_background_color: "transparent"

                                    enabledCustom: {
                                        if (!createScreenServices.itemLoader.item.valid) return false
                                        if (!createScreenCompanyName.itemLoader.item.valid) return false
                                        if (!createScreenMainEmail.itemLoader.item.valid) return false
                                        if (!createScreenCeoName.itemLoader.item.valid) return false
                                        if (!createScreenCompanyType.itemLoader.item.valid) return false
                                        if (!createScreenEmployees.itemLoader.item.valid) return false
                                        if (!createScreenNumbers.itemLoader.item.valid) return false
                                        if (!createScreenCountry.itemLoader.item.valid) return false
                                        if (!createScreenRegion.itemLoader.item.valid) return false
                                        if (!createScreenAgree.itemLoader.item.valid) return false

                                        return true
                                    }

                                    anchors.centerIn: parent

                                    onClicked: {
                                        createScreenCreateButton.forceActiveFocus()

                                        var email = createScreenMainEmail.itemLoader.item.value[0]["email"]
                                        var companyData = collectUserData()
                                        var saveData = {
                                            "userID": appUser.user_id,
                                            "name": companyData["short_name"],
                                            "code": companyData["country_code"],
                                            "companyData": companyData,
                                            "agreement": createScreenAgree.itemLoader.item.value,
                                            "phoneNumbers": createScreenNumbers.itemLoader.item.phoneNumbers,
                                            "uniqueFields": ["userID", "name", "code"]
                                        }
                                        settings.storage_append("companies_creation", saveData)

                                        if (email.toLowerCase() in companyStack.confirmedEmails) {
                                            var settingsData = {
                                                "email_token": companyStack.confirmedEmails[email.toLowerCase()],
                                                "company": companyData,
                                            }
                                            createScreenCreateButton.loading = true
                                            app.company_module.create_company_new(settingsData)
                                            return
                                        }

                                        var td = companyStack.timeDiff(email)
                                        if (td > 0) {
                                            var confirmationInfo = companyStack.sendCodesInfo[email]
                                            Popups.confirm_email_popup(confirmationInfo, companyStack, false)
                                            return
                                        }

                                        var emailSettings = {"email": email}
                                        createScreenCreateButton.loading = true
                                        app.company_module.request_new_email_confirmation(emailSettings)
                                    }
                                }

                                Connections {
                                    target: app.company_module

                                    onRequestNewEmailConfirmationSuccess: {
                                        createScreenCreateButton.loading = false
                                    }

                                    onRequestNewEmailConfirmationFailed: {
                                        createScreenCreateButton.loading = false
                                    }

                                    onCreateCompanySuccess: {
                                        createScreenCreateButton.loading = false
                                    }

                                    onCreateCompanyFailed: {
                                        createScreenCreateButton.loading = false
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Desktop.ColumnItem {
                margin: 48

                contentItem: Component {
                    Item {}
                }
            }
        }
    }

    Desktop.BackArea {
        backArea.onClicked: {
            if (companyCreateScreen.companies) {
                companyLoader.setSource(companyStack.foundScreen, {"companies": companyCreateScreen.companies, "companyName": companyCreateScreen.companyName, "countryCode": companyCreateScreen.countryCode})
            } else {
                companyLoader.setSource(companyStack.searchScreen, {"companyNameDefault": companyCreateScreen.companyName, "countryCodeDefault": companyCreateScreen.countryCode})
            }
        }
    }
}

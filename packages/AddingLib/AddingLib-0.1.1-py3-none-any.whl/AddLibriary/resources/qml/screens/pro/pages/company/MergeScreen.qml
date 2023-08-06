import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtQml.Models 2.14
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: companyMergeScreen

    property var companies: null
    property var companyName: ""
    property var countryCode: ""

    property var companyInfo: null

    function collectUserData() {
        var settings = {}

        settings["provided_services"] = mergeScreenServices.itemLoader.item.value
        settings["short_name"] = mergeScreenCompanyName.itemLoader.item.value
        settings["email_addresses"] = mergeScreenMainEmail.itemLoader.item.value
        settings["full_name"] = mergeScreenCompanyLegalName.itemLoader.item.value
        settings["head_of_company"] = mergeScreenCeoName.itemLoader.item.value
        settings["registration_number"] = mergeScreenRegistrationNumber.itemLoader.item.value
        settings["company_type"] = mergeScreenCompanyType.itemLoader.item.value
        settings["employees_number"] = mergeScreenEmployees.itemLoader.item.value
        settings["technical_emails"] = mergeScreenTechEmail.itemLoader.item.value

        settings["legal_address"] = {}
        settings["legal_address"]["country"] = mergeScreenLegalCountry.itemLoader.item.value
        settings["legal_address"]["state"] = mergeScreenLegalRegion.itemLoader.item.value
        settings["legal_address"]["city"] = mergeScreenLegalCity.itemLoader.item.value
        settings["legal_address"]["zip_code"] = mergeScreenLegalCode.itemLoader.item.value
        settings["legal_address"]["address_line1"] = mergeScreenLegalAddressLines.itemLoader.item.value
        settings["legal_address"]["address_line2"] = ""

        settings["customer_inquiries_emails"] = mergeScreenCustomerEmail.itemLoader.item.value
        settings["phone_numbers"] = mergeScreenNumbers.itemLoader.item.value
        settings["web_site_url"] = mergeScreenWebsite.itemLoader.item.value
        settings["country_code"] = mergeScreenCountry.itemLoader.item.value
        settings["locations"] = mergeScreenRegion.itemLoader.item.value

        settings["company_logo"] = {}
        settings["company_logo"]["image_id"] = mergeScreenLogo.itemLoader.item.value

        return settings
    }

    ListView {
        id: listView

        spacing: 32
        currentIndex: 0
        interactive: false
        model: objectsModel

        anchors.fill: parent

        orientation: Qt.Horizontal
        snapMode: ListView.SnapOneItem
        highlightMoveDuration: 300
        highlightMoveVelocity: -1
        highlightRangeMode: ListView.StrictlyEnforceRange
    }

    ObjectModel {
        id: objectsModel

        Item {
            width: companyMergeScreen.width
            height: companyMergeScreen.height

            Desktop.StepItem {
                width: parent.width / 4 - 84

                step: "1"
                count: "3"
            }

            Desktop.ScrollView {
                id: scrollViewFirst

                Column {
                    width: companyMergeScreen.width

                    Desktop.ColumnItem {
                        id: mergeScreenHeaderFirst

                        margin: 48

                        contentItem: Component {
                            Item {
                                height: mergeScreenHeaderFirstText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenHeaderFirstText

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
                        id: mergeScreenTip

                        margin: 64

                        contentItem: Component {
                            Item {
                                height: mergeScreenTipText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenTipText

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
                        id: mergeScreenServices

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

                                    comingSoon: false
                                    title: tr.alarm_monitoring

                                    selected: {
                                        if (!companyMergeScreen.companyInfo) return false
                                        if (!companyMergeScreen.companyInfo.companyData) return false
                                        if (!companyMergeScreen.companyInfo.companyData.provided_services) return false
                                        if (!companyMergeScreen.companyInfo.companyData.provided_services.monitoring) return false

                                        return companyMergeScreen.companyInfo.companyData.provided_services.monitoring
                                    }

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

                                    comingSoon: false
                                    title: tr.installation_and_maintenance

                                    selected: {
                                        if (!companyMergeScreen.companyInfo) return false
                                        if (!companyMergeScreen.companyInfo.companyData) return false
                                        if (!companyMergeScreen.companyInfo.companyData.provided_services) return false
                                        if (!companyMergeScreen.companyInfo.companyData.provided_services.installation) return false

                                        return companyMergeScreen.companyInfo.companyData.provided_services.installation
                                    }

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
                        id: mergeScreenInfo

                        margin: 64

                        contentItem: Component {
                            Item {
                                height: mergeScreenInfoText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenInfoText

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
                        id: mergeScreenCompanyName

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenCompanyNameField.valueText.control.text.trim()

                                property var valid: value.length >= 2 && value.length <= 100

                                Desktop.ToolTip {
                                    text: tr.hover_company_name
                                    visible: mergeScreenCompanyNameArea.containsMouse
                                }

                                Custom.TextFieldEdit {
                                    id: mergeScreenCompanyNameField

                                    width: parent.width * 0.7
                                    key: tr.field_company_name + ui.required
                                    distance: 12

                                    enabled: false
                                    opacity: enabled ? 1 : 0.5
                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.short_name) return ""

                                        return companyMergeScreen.companyInfo.companyData.short_name
                                    }

                                    valueText.control.maximumLength: 100

                                    keyText {
                                        opacity: 1
                                        color: ui.colors.secondary
                                    }
                                }

                                MouseArea {
                                    id: mergeScreenCompanyNameArea

                                    hoverEnabled: true
                                    width: mergeScreenCompanyNameField.width
                                    height: mergeScreenCompanyNameField.height
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenMainEmail

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenMainEmailEdit.height

                                property var value: {
                                    if (!companyMergeScreen.companyInfo) return []
                                    if (!companyMergeScreen.companyInfo.companyData) return []
                                    if (!companyMergeScreen.companyInfo.companyData.email_addresses) return []

                                    return companyMergeScreen.companyInfo.companyData.email_addresses
                                }

                                property var valid: true

                                Desktop.ToolTip {
                                    text: tr.hover_company_email_add_hubs
                                    visible: mergeScreenCompanyNameArea.containsMouse
                                }

                                Desktop.MultiField {
                                    id: mergeScreenMainEmailEdit

                                    enabled: false
                                    width: parent.width * 0.7
                                    key: tr.field_company_email_add_hubs + ui.required

                                    maxCount: 5
                                    distance: 12
                                    fieldDistance: 12
                                    useFooter: false
                                    maximumLength: 100
                                    atLeastOneField: true

                                    keyText {
                                        width: parent.width
                                        textFormat: Text.RichText
                                    }

                                    model: {
                                        if (!companyMergeScreen.companyInfo) return []
                                        if (!companyMergeScreen.companyInfo.companyData) return []
                                        if (!companyMergeScreen.companyInfo.companyData.email_addresses) return []

                                        var items = []
                                        companyMergeScreen.companyInfo.companyData.email_addresses.forEach(function(item) {
                                            items.push(item.email)
                                        })
                                        return items
                                    }
                                }

                                MouseArea {
                                    id: mergeScreenCompanyNameArea

                                    hoverEnabled: true
                                    width: mergeScreenMainEmailEdit.width
                                    height: mergeScreenMainEmailEdit.height
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenCompanyLegalName

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenCompanyLegalNameField.valueText.control.text.trim()

                                property var valid: value.length >= 3 && value.length <= 200

                                Desktop.ToolTip {
                                    text: tr.hover_company_legal_name
                                    visible: mergeScreenCompanyLegalNameField.valueText.control.activeFocus
                                }

                                Custom.TextFieldEdit {
                                    id: mergeScreenCompanyLegalNameField

                                    width: parent.width
                                    key: tr.full_legal_company_name + ui.required
                                    distance: 12

                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.full_name) return ""

                                        return companyMergeScreen.companyInfo.companyData.full_name
                                    }

                                    valueText.control.maximumLength: 200

                                    keyText {
                                        opacity: 1
                                        color: ui.colors.secondary
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenCeoName

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenCeoNameField.valueText.control.text.trim()

                                property var valid: value.length >= 3 && value.length <= 200

                                Desktop.ToolTip {
                                    text: tr.hover_director_fio
                                    visible: mergeScreenCeoNameField.valueText.control.activeFocus
                                }

                                Custom.TextFieldEdit {
                                    id: mergeScreenCeoNameField

                                    width: parent.width
                                    key: tr.a911_director_fio + ui.required
                                    distance: 12

                                    valueText.control.maximumLength: 200

                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.head_of_company) return ""

                                        return companyMergeScreen.companyInfo.companyData.head_of_company
                                    }

                                    keyText {
                                        opacity: 1
                                        color: ui.colors.secondary
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenRegistrationNumber

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenRegistrationNumberField.valueText.control.text.trim()

                                property var valid: value.length >= 1 && value.length <= 100

                                Desktop.ToolTip {
                                    text: tr.hover_company_registration_number
                                    visible: mergeScreenRegistrationNumberField.valueText.control.activeFocus
                                }

                                Custom.TextFieldEdit {
                                    id: mergeScreenRegistrationNumberField

                                    width: parent.width * 0.7
                                    key: tr.a911_state_declaration_number + ui.required
                                    distance: 12

                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.registration_number) return ""

                                        return companyMergeScreen.companyInfo.companyData.registration_number
                                    }

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
                        id: mergeScreenCompanyType

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenCompanyTypeCombo.serverModel[mergeScreenCompanyTypeCombo.currentIndex]

                                property var valid: mergeScreenCompanyTypeCombo.currentIndex >= 0

                                Desktop.ToolTip {
                                    text: tr.choose_one_posible
                                    visible: mergeScreenCompanyTypeCombo.comboPopup.opened
                                }

                                Desktop.NormalText {
                                    id: mergeScreenCompanyTypeText

                                    text: tr.сompany_type + ui.required
                                    color: ui.colors.middle1

                                    width: parent.width
                                    textFormat: Text.RichText

                                    anchors.top: parent.top
                                }

                                Custom.ComboBoxNew {
                                    id: mergeScreenCompanyTypeCombo

                                    width: parent.width
                                    model: userModel

                                    anchors {
                                        top: mergeScreenCompanyTypeText.bottom
                                        topMargin: 6
                                    }

                                    currentIndex: {
                                        if (!companyMergeScreen.companyInfo) return 0
                                        if (!companyMergeScreen.companyInfo.companyData) return 0
                                        if (!companyMergeScreen.companyInfo.companyData.company_type) return 0

                                        if (companyMergeScreen.companyInfo.companyData.company_type == "NO_COMPANY_TYPE_INFO") return 0

                                        return serverModel.indexOf(companyMergeScreen.companyInfo.companyData.company_type)
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
                        id: mergeScreenEmployees

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenEmployeesCombo.serverModel[mergeScreenEmployeesCombo.currentIndex]

                                property var valid: mergeScreenEmployeesCombo.currentIndex >= 0

                                Desktop.NormalText {
                                    id: mergeScreenEmployeesText

                                    text: tr.number_of_employees + ui.required
                                    color: ui.colors.middle1

                                    width: parent.width
                                    textFormat: Text.RichText

                                    anchors.top: parent.top
                                }

                                Custom.ComboBoxNew {
                                    id: mergeScreenEmployeesCombo

                                    width: parent.width * 0.3
                                    model: userModel

                                    anchors {
                                        top: mergeScreenEmployeesText.bottom
                                        topMargin: 6
                                    }

                                    currentIndex: {
                                        if (!companyMergeScreen.companyInfo) return 0
                                        if (!companyMergeScreen.companyInfo.companyData) return 0
                                        if (!companyMergeScreen.companyInfo.companyData.employees_number) return 0

                                        if (companyMergeScreen.companyInfo.companyData.employees_number == "NO_EMPLOYEES_NUMBER_INFO") return 0

                                        return serverModel.indexOf(companyMergeScreen.companyInfo.companyData.employees_number)
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
                        id: mergeScreenTechEmail

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenTechEmailEdit.height + mergeScreenTechEmailFieldHint.contentHeight + 4

                                property var value: {
                                    var emails = []
                                    for (var i = 0; i < mergeScreenTechEmailEdit.itemsCollection.length; i++) {
                                        emails.push({"email": mergeScreenTechEmailEdit.itemsCollection[i].trim()})
                                    }
                                    return emails
                                }

                                property var valid: mergeScreenTechEmailEdit.allFieldsValid

                                Desktop.ToolTip {
                                    text: tr.hover_company_technical_email
                                    visible: mergeScreenTechEmailEdit.multiFieldActive
                                }

                                Desktop.MultiField {
                                    id: mergeScreenTechEmailEdit

                                    width: parent.width * 0.7
                                    key: tr.field_company_technical_email + ui.required

                                    maxCount: 5
                                    distance: 12
                                    fieldDistance: 12
                                    useFooter: false
                                    atLeastOneField: true
                                    validator: RegExpValidator { regExp: /^[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я+]+)*@[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я]+)*(\.[0-9a-zA-Zа-яА-Я]{2,10})+$/ }

                                    keyText {
                                        width: parent.width
                                        textFormat: Text.RichText
                                    }

                                    model: {
                                        if (!companyMergeScreen.companyInfo) return []
                                        if (!companyMergeScreen.companyInfo.companyData) return []
                                        if (!companyMergeScreen.companyInfo.companyData.technical_emails) return []

                                        var items = []
                                        companyMergeScreen.companyInfo.companyData.technical_emails.forEach(function(item) {
                                            items.push(item.email)
                                        })
                                        return items
                                    }

                                    plusItemVisible: mergeScreenTechEmailEdit.allFieldsValid
                                }

                                Desktop.NormalText {
                                    id: mergeScreenTechEmailFieldHint

                                    width: parent.width
                                    text: tr.info_company_technical_email
                                    color: ui.colors.middle3

                                    anchors {
                                        top: mergeScreenTechEmailEdit.bottom
                                        topMargin: 4
                                        left: parent.left
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenMergeFirst

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 48

                                property alias mergeScreenContinueFirst: mergeScreenContinueFirst

                                Item {
                                    width: mergeScreenContinueFirstItem.width
                                    height: 48

                                    Item {
                                        id: mergeScreenContinueFirstItem

                                        width: mergeScreenContinueFirst.textButton.contentWidth + 64
                                        height: parent.height

                                        Custom.Button {
                                            id: mergeScreenContinueFirst

                                            width: parent.width
                                            text: tr.continue_
                                            textButton.textFormat: Text.PlainText
                                            loading_background_color: "transparent"

                                            enabledCustom: {
                                                if (!mergeScreenServices.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyName.itemLoader.item.valid) return false
                                                if (!mergeScreenMainEmail.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyLegalName.itemLoader.item.valid) return false
                                                if (!mergeScreenCeoName.itemLoader.item.valid) return false
                                                if (!mergeScreenRegistrationNumber.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyType.itemLoader.item.valid) return false
                                                if (!mergeScreenEmployees.itemLoader.item.valid) return false
                                                if (!mergeScreenTechEmail.itemLoader.item.valid) return false

                                                return true
                                            }

                                            anchors.centerIn: parent

                                            onClicked: {
                                                listView.currentIndex = 1
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
        }

        Item {
            width: companyMergeScreen.width
            height: companyMergeScreen.height

            Desktop.StepItem {
                width: parent.width / 4 - 84

                step: "2"
                count: "3"
            }

            Desktop.ScrollView {
                id: scrollViewSecond

                Column {
                    width: companyMergeScreen.width

                    Desktop.ColumnItem {
                        id: mergeScreenHeaderSecond

                        margin: 48

                        contentItem: Component {
                            Item {
                                height: mergeScreenHeaderSecondText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenHeaderSecondText

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
                        id: mergeScreenLegalAddress

                        margin: 64

                        contentItem: Component {
                            Item {
                                height: mergeScreenLegalAddressText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenLegalAddressText

                                    text: tr.a911_legal_address
                                    color: ui.colors.light3
                                    size: 24
                                    bold: true

                                    anchors.fill: parent
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenAddressTip

                        margin: 4

                        contentItem: Component {
                            Item {
                                height: mergeScreenAddressTipText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenAddressTipText

                                    text: tr.legal_address_info
                                    color: ui.colors.middle1

                                    anchors.fill: parent
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenLegalCountry

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 72

                                property var value: mergeScreenLegalCountryCombo.code

                                property var valid: mergeScreenLegalCountryCombo.name == mergeScreenLegalCountryCombo.currentFieldValue

                                Desktop.NormalText {
                                    id: mergeScreenLegalCountryText

                                    enabled: parent.enabled
                                    opacity: enabled ? 1 : 0.5

                                    text: tr.country + ui.required
                                    color: ui.colors.secondary

                                    width: parent.width
                                    textFormat: Text.RichText
                                }

                                Custom.CountriesCombobox {
                                    id: mergeScreenLegalCountryCombo

                                    width: parent.width * 0.3

                                    enabled: parent.enabled
                                    opacity: enabled ? 1 : 0.5

                                    maxPopupHeight: 300
                                    badgeImageMargin: 4
                                    includeWorldwide: false
                                    textLabel.placeHolderText: ""

                                    anchors {
                                        top: mergeScreenLegalCountryText.bottom
                                        topMargin: 8
                                    }

                                    code: {
                                        if (!companyMergeScreen.companyInfo) return companyMergeScreen.countryCode
                                        if (!companyMergeScreen.companyInfo.companyData) return companyMergeScreen.countryCode
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address) return companyMergeScreen.countryCode
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address.country) return companyMergeScreen.countryCode

                                        return companyMergeScreen.companyInfo.companyData.legal_address.country
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenLegalRegion

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenLegalRegionField.valueText.control.text.trim()

                                property var valid: value.length >= 1 && value.length <= 100

                                Custom.TextFieldEdit {
                                    id: mergeScreenLegalRegionField

                                    width: parent.width * 0.7
                                    key: tr.region_911 + ui.required
                                    distance: 12

                                    enabled: true
                                    opacity: enabled ? 1 : 0.5
                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address.state) return ""

                                        return companyMergeScreen.companyInfo.companyData.legal_address.state
                                    }

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
                        id: mergeScreenLegalCity

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenLegalCityField.valueText.control.text.trim()

                                property var valid: value.length >= 1 && value.length <= 100

                                Custom.TextFieldEdit {
                                    id: mergeScreenLegalCityField

                                    width: parent.width * 0.7
                                    key: tr.city + ui.required
                                    distance: 12

                                    enabled: true
                                    opacity: enabled ? 1 : 0.5
                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address.city) return ""

                                        return companyMergeScreen.companyInfo.companyData.legal_address.city
                                    }

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
                        id: mergeScreenLegalCode

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 70

                                property var value: mergeScreenLegalCodeField.valueText.control.text.trim()

                                property var valid: value.length >= 1 && value.length <= 20

                                Custom.TextFieldEdit {
                                    id: mergeScreenLegalCodeField

                                    width: parent.width * 0.3
                                    key: tr.zip_code_911 + ui.required
                                    distance: 12

                                    enabled: true
                                    opacity: enabled ? 1 : 0.5
                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address.zip_code) return ""

                                        return companyMergeScreen.companyInfo.companyData.legal_address.zip_code
                                    }

                                    valueText.control.maximumLength: 20

                                    keyText {
                                        opacity: 1
                                        color: ui.colors.secondary
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenLegalAddressLines

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenLegalAddressLinesField.height + 6

                                property var value: mergeScreenLegalAddressLinesField.valueText.control.text.trim()

                                property var valid: value.length >= 3 && value.length <= 200

                                Custom.TextAreaEdit {
                                    id: mergeScreenLegalAddressLinesField

                                    width: parent.width
                                    key: tr.street_house_office_tip + ui.required
                                    distance: 12

                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.legal_address) return ""

                                        var fa = companyMergeScreen.companyInfo.companyData.legal_address.address_line1 ? companyMergeScreen.companyInfo.companyData.legal_address.address_line1 : ""
                                        var sa = companyMergeScreen.companyInfo.companyData.legal_address.address_line2 ? companyMergeScreen.companyInfo.companyData.legal_address.address_line2 : ""

                                        if (fa && sa) return fa + ", " + sa
                                        if (fa) return fa
                                        if (sa) return sa
                                        return ""
                                    }

                                    keyText {
                                        opacity: 1
                                        color: ui.colors.secondary
                                    }

                                    valueText {
                                        maximumLength: 200
                                        height: valueText.control.contentHeight + 24 < 136 ? 136 : valueText.control.contentHeight + 24

                                        control {
                                            wrapMode: Text.WordWrap
                                            verticalAlignment: TextInput.AlignTop
                                            height: valueText.control.contentHeight + 24 < 128 ? 128 : valueText.control.contentHeight + 24
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        margin: 0

                        contentItem: Component {
                            Item {
                                height: scrollViewSecond.height - scrollViewHeight > 0 ? scrollViewSecond.height - scrollViewHeight : 0

                                property var scrollViewHeight: {
                                    return (
                                        mergeScreenHeaderSecond.height +
                                        mergeScreenLegalAddress.height +
                                        mergeScreenAddressTip.height +
                                        mergeScreenLegalCountry.height +
                                        mergeScreenLegalRegion.height +
                                        mergeScreenLegalCity.height +
                                        mergeScreenLegalCode.height +
                                        mergeScreenLegalAddressLines.height +
                                        mergeScreenMergeSecond.height + 48
                                    )
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenMergeSecond

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 48

                                property alias mergeScreenContinueSecond: mergeScreenContinueSecond

                                Item {
                                    width: mergeScreenContinueSecondItem.width
                                    height: 48

                                    Item {
                                        id: mergeScreenContinueSecondItem

                                        width: mergeScreenContinueSecond.textButton.contentWidth + 64
                                        height: parent.height

                                        Custom.Button {
                                            id: mergeScreenContinueSecond

                                            width: parent.width
                                            text: tr.continue_
                                            textButton.textFormat: Text.PlainText
                                            loading_background_color: "transparent"

                                            enabledCustom: {
                                                if (!mergeScreenServices.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyName.itemLoader.item.valid) return false
                                                if (!mergeScreenMainEmail.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyLegalName.itemLoader.item.valid) return false
                                                if (!mergeScreenCeoName.itemLoader.item.valid) return false
                                                if (!mergeScreenRegistrationNumber.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyType.itemLoader.item.valid) return false
                                                if (!mergeScreenEmployees.itemLoader.item.valid) return false
                                                if (!mergeScreenTechEmail.itemLoader.item.valid) return false

                                                if (!mergeScreenLegalCountry.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalRegion.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalCity.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalCode.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalAddressLines.itemLoader.item.valid) return false

                                                return true
                                            }

                                            anchors.centerIn: parent

                                            onClicked: {
                                                listView.currentIndex = 2
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
        }

        Item {
            width: companyMergeScreen.width
            height: companyMergeScreen.height

            Desktop.StepItem {
                width: parent.width / 4 - 84

                step: "3"
                count: "3"
            }

            Desktop.ScrollView {
                id: scrollViewThird

                PropertyAnimation {
                    id: scrollBarAnimThird

                    target: scrollViewThird.ScrollBar.vertical
                    to: 0
                    duration: 300
                    property: "position"
                }

                Connections {
                    target: app.company_module

                    onCompanyValidationErrors: {
                        scrollBarAnimThird.to = 0.1
                        scrollBarAnimThird.start()
                    }
                }

                Column {
                    width: companyMergeScreen.width

                    Desktop.ColumnItem {
                        id: mergeScreenHeaderThird

                        margin: 48

                        contentItem: Component {
                            Item {
                                height: mergeScreenHeaderThirdText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenHeaderThirdText

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
                        id: mergeScreenPublic

                        margin: 64

                        contentItem: Component {
                            Item {
                                height: mergeScreenPublicText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenPublicText

                                    text: tr.public_pro_desktop_title
                                    color: ui.colors.light3
                                    size: 24
                                    bold: true

                                    anchors.fill: parent
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenPublicTip

                        margin: 4

                        contentItem: Component {
                            Item {
                                height: mergeScreenPublicTipText.contentHeight

                                Desktop.NormalText {
                                    id: mergeScreenPublicTipText

                                    text: tr.public_pro_desktop_info
                                    color: ui.colors.middle1

                                    anchors.fill: parent
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenCustomerEmail

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenCustomerEmailEdit.height

                                property var value: {
                                    var emails = []
                                    for (var i = 0; i < mergeScreenCustomerEmailEdit.itemsCollection.length; i++) {
                                        emails.push({"email": mergeScreenCustomerEmailEdit.itemsCollection[i].trim()})
                                    }
                                    return emails
                                }

                                property var valid: mergeScreenCustomerEmailEdit.allFieldsValid

                                Desktop.ToolTip {
                                    text: tr.hover_company_public_email
                                    visible: mergeScreenCustomerEmailEdit.multiFieldActive
                                }

                                Desktop.MultiField {
                                    id: mergeScreenCustomerEmailEdit

                                    width: parent.width * 0.7
                                    key: tr.field_company_public_email + ui.required

                                    maxCount: 5
                                    distance: 12
                                    fieldDistance: 12
                                    useFooter: false
                                    maximumLength: 100
                                    atLeastOneField: true
                                    validator: RegExpValidator { regExp: /^[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я+]+)*@[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я]+)*(\.[0-9a-zA-Zа-яА-Я]{2,10})+$/ }

                                    keyText {
                                        width: parent.width
                                        textFormat: Text.RichText
                                    }

                                    model: {
                                        if (!companyMergeScreen.companyInfo) return []
                                        if (!companyMergeScreen.companyInfo.companyData) return []
                                        if (!companyMergeScreen.companyInfo.companyData.customer_inquiries_emails) return []

                                        var items = []
                                        companyMergeScreen.companyInfo.companyData.customer_inquiries_emails.forEach(function(item) {
                                            items.push(item.email)
                                        })
                                        return items
                                    }

                                    plusItemVisible: mergeScreenCustomerEmailEdit.allFieldsValid
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenNumbers

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenCountryPhones.height

                                property var value: mergeScreenCountryPhones.itemsCollection
                                property var phoneNumbers: mergeScreenCountryPhones.phoneNumbers

                                property var valid: {
                                    for (var i = 0; i < phoneNumbers.length; i++) {
                                        var item = phoneNumbers[i].phoneField.trim()
                                        if (item.length < mergeScreenCountryPhones.fieldMinLength || item.length > 30) return false
                                    }
                                    return true
                                }

                                Desktop.ToolTip {
                                    text: tr.hover_company_phone_number
                                    visible: mergeScreenCountryPhones.active
                                }

                                Desktop.CountryPhones {
                                    id: mergeScreenCountryPhones

                                    key: tr.company_phone_number + ui.required
                                    defaultCountry: mergeScreenCountry.itemLoader.item.value

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
                                        if (!companyMergeScreen.companyInfo) return []
                                        if (!companyMergeScreen.companyInfo.phoneNumbers) return []

                                        return companyMergeScreen.companyInfo.phoneNumbers
                                    }

                                    plusItemVisible: {
                                        for (var i = 0; i < phoneNumbers.length; i++) {
                                            var item = phoneNumbers[i].phoneField.trim()
                                            if (item.length < mergeScreenCountryPhones.fieldMinLength) return false
                                        }
                                        return true
                                    }
                                }

                                Connections {
                                    target: app.company_module

                                    onCompanyValidationErrors: {
                                        mergeScreenCountryPhones.errorResult(result)
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenWebsite

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenWebsiteField.height

                                property var value: mergeScreenWebsiteField.value.trim()

                                property var valid: mergeScreenWebsiteField.valid

                                Desktop.ToolTip {
                                    text: tr.hover_company_website
                                    visible: mergeScreenWebsiteField.hasFocus
                                }

                                DS.InputField {
                                    id: mergeScreenWebsiteField

                                    width: parent.width * 0.7

                                    title: tr.website
                                    info: tr.website_format_tip_desktop
                                    isJointBottomText: true
                                    value: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.web_site_url) return ""
                                        return companyMergeScreen.companyInfo.companyData.web_site_url
                                    }
                                    regex: ui.regexes.websiteUrl
                                    validatorError: tr.wrong_website_desktop
                                    minimumLength: 3
                                    maximumLength: 100
                                    lengthError: tr.from_3_to_100_characters_911
                                }

                                Connections {
                                    target: app.company_module

                                    onCompanyValidationErrors: {
                                        if (result["2.31"]) {
                                            mergeScreenWebsiteField.forcedError = result["2.31"].message
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenLogo

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenLogoText.contentHeight + 12 + imageItem.height

                                property var value: imageItem.trueImageId

                                property var valid: imageItem.trueImageId != ""

                                Desktop.NormalText {
                                    id: mergeScreenLogoText

                                    text: tr.a911_logo + ui.required
                                    color: ui.colors.middle1

                                    width: parent.width
                                    textFormat: Text.RichText

                                    anchors.top: parent.top
                                }

                                Desktop.OriginalImage {
                                    id: imageItem

                                    size: 300
                                    radius: 16
                                    deleteSize: 24
                                    editable: true

                                    text: mergeScreenCompanyName.itemLoader.item.value

                                    trueImage: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.company_logo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.company_logo.images) return ""

                                        var item = ""

                                        item = util.get_image_with_resolution(companyMergeScreen.companyInfo.companyData.company_logo.images, "300x300")
                                        if (item) return item

                                        item = util.get_image_with_resolution(companyMergeScreen.companyInfo.companyData.company_logo.images, "128x128")
                                        if (item) return item

                                        item = util.get_image_with_resolution(companyMergeScreen.companyInfo.companyData.company_logo.images, "64x64")
                                        if (item) return item

                                        return ""
                                    }

                                    trueImageId: {
                                        if (!companyMergeScreen.companyInfo) return ""
                                        if (!companyMergeScreen.companyInfo.companyData) return ""
                                        if (!companyMergeScreen.companyInfo.companyData.company_logo.image_id) return ""

                                        return companyMergeScreen.companyInfo.companyData.company_logo.image_id
                                    }

                                    anchors {
                                        top: mergeScreenLogoText.bottom
                                        topMargin: 12
                                        left: parent.left
                                    }

                                    deleteArea.onClicked: {
                                        imageItem.trueImage = ""
                                        imageItem.trueImageId = ""
                                    }
                                }

                                Desktop.NormalText {
                                    id: mergeScreenLogoTip

                                    width: parent.width - imageItem.width - 16
                                    text: tr.a911_drag_and_drop
                                    color: ui.colors.middle1

                                    anchors {
                                        top: imageItem.top
                                        left: imageItem.right
                                        leftMargin: 16
                                    }
                                }

                                Item {
                                    id: logoButtonBlock

                                    width: logoButton.textButton.contentWidth + 64
                                    height: 48

                                    anchors {
                                        left: imageItem.right
                                        leftMargin: 16
                                        bottom: parent.bottom
                                    }

                                    Custom.Button {
                                        id: logoButton

                                        width: parent.width
                                        text: tr.a911_upload_logo

                                        animColor: color
                                        transparent: true
                                        color: ui.colors.white
                                        loading_background_color: "transparent"
                                        textButton.textFormat: Text.PlainText

                                        anchors.centerIn: parent

                                        onClicked: {
                                            fileDialog.open()
                                        }
                                    }
                                }

                                Connections {
                                    target: app.company_module

                                    onUploadCompanyLogoSuccess: {
                                        imageItem.trueImage = logo_url
                                        imageItem.trueImageId = image_id
                                    }
                                }

                                Desktop.FileDialogImages {
                                    id: fileDialog

                                    onAccepted: {
                                        if (fileDialog.fileUrls.length == 1) {
                                            app.company_module.upload_company_logo(fileDialog.fileUrl, "300x300", false)
                                        }
                                        fileDialog.close()
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenCountry

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 72

                                property var value: mergeScreenCountryCombo.code

                                property var valid: mergeScreenCountryCombo.name == mergeScreenCountryCombo.currentFieldValue

                                Desktop.ToolTip {
                                    text: tr.hover_company_country_work
                                    visible: mergeScreenCountryCombo.countriesPopup.opened
                                }

                                Desktop.NormalText {
                                    id: mergeScreenCountryText

                                    enabled: parent.enabled
                                    opacity: enabled ? 1 : 0.5

                                    text: tr.field_company_country_work + ui.required
                                    color: ui.colors.secondary

                                    width: parent.width
                                    textFormat: Text.RichText
                                }

                                Custom.CountriesCombobox {
                                    id: mergeScreenCountryCombo

                                    width: parent.width * 0.3

                                    enabled: parent.enabled
                                    opacity: enabled ? 1 : 0.5

                                    maxPopupHeight: 300
                                    badgeImageMargin: 4
                                    includeWorldwide: false
                                    textLabel.placeHolderText: ""

                                    anchors {
                                        top: mergeScreenCountryText.bottom
                                        topMargin: 8
                                    }

                                    code: {
                                        if (!companyMergeScreen.companyInfo) return companyMergeScreen.countryCode
                                        if (!companyMergeScreen.companyInfo.companyData) return companyMergeScreen.countryCode
                                        if (!companyMergeScreen.companyInfo.companyData.country_code) return companyMergeScreen.countryCode

                                        return companyMergeScreen.companyInfo.companyData.country_code
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenRegion

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: mergeScreenLocationsEdit.height

                                property var value: mergeScreenLocationsEdit.itemsCollection

                                property var valid: {
                                    for (var i = 0; i < value.length; i++) {
                                        var item = value[i].trim()
                                        if (item.length < 2 || item.length > 200) return false
                                    }
                                    return true
                                }

                                Desktop.ToolTip {
                                    text: tr.hover_company_region_work
                                    visible: mergeScreenLocationsEdit.multiFieldActive
                                }

                                Desktop.MultiField {
                                    id: mergeScreenLocationsEdit

                                    width: parent.width * 0.58
                                    key: tr.field_company_region_work + ui.required

                                    maxCount: 50
                                    distance: 12
                                    fieldDistance: 12
                                    useFooter: false
                                    atLeastOneField: true

                                    keyText {
                                        width: parent.width
                                        textFormat: Text.RichText
                                    }

                                    model: {
                                        if (!companyMergeScreen.companyInfo) return []
                                        if (!companyMergeScreen.companyInfo.companyData) return []
                                        if (!companyMergeScreen.companyInfo.companyData.locations) return []

                                        return companyMergeScreen.companyInfo.companyData.locations
                                    }

                                    plusItemVisible: {
                                        for (var i = 0; i < itemsCollection.length; i++) {
                                            var item = itemsCollection[i].trim()
                                            if (item.length == 0) return false
                                        }
                                        return true
                                    }
                                }
                            }
                        }
                    }

                    Desktop.ColumnItem {
                        id: mergeScreenAgree

                        margin: 48

                        contentItem: Component {
                            Item {
                                height: Math.max(32, mergeScreenAgreeText.contentHeight)

                                property var value: mergeScreenAgreeCheckbox.selected

                                property var valid: value

                                Item {
                                    id: mergeScreenAgreeCheckbox

                                    width: 24
                                    height: 24

                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }

                                    property var selected: {
                                        if (!companyMergeScreen.companyInfo) return false
                                        if (!companyMergeScreen.companyInfo.agreement) return false

                                        return companyMergeScreen.companyInfo.agreement
                                    }

                                    Image {
                                        source: "qrc:/resources/images/pro/company/selected.svg"
                                        sourceSize.width: 24
                                        sourceSize.height: 20

                                        visible: mergeScreenAgreeCheckbox.selected

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

                                        visible: !mergeScreenAgreeCheckbox.selected

                                        border {
                                            width: 2
                                            color: mergeScreenAgreeCheckbox.enabled ? ui.colors.middle1 : ui.colors.middle4
                                        }

                                        anchors {
                                            top: parent.top
                                            left: parent.left
                                        }
                                    }

                                    Custom.HandMouseArea {
                                        onClicked: {
                                            mergeScreenAgreeCheckbox.forceActiveFocus()
                                            mergeScreenAgreeCheckbox.selected = !mergeScreenAgreeCheckbox.selected
                                        }
                                    }
                                }

                                Custom.FontText {
                                    id: mergeScreenAgreeText

                                    width: parent.width - 36
                                    text: tr.i_have_read_and_agree + ": " + "<a style='text-decoration:none' href='agreement'>" + util.colorize(tr.a911_terms_of_use, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='privacy'>" + util.colorize(tr.a911_privacy_policy, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='license'>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.colors.green1) + "</a>"
                                    color: ui.colors.middle1
                                    opacity: 0.9

                                    font.pixelSize: 15
                                    wrapMode: Text.Wrap
                                    textFormat: Text.RichText
                                    verticalAlignment: Text.AlignVCenter

                                    anchors {
                                        left: mergeScreenAgreeCheckbox.right
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
                        id: mergeScreenMergeThird

                        margin: 32

                        contentItem: Component {
                            Item {
                                height: 48

                                property alias mergeScreenContinueThird: mergeScreenContinueThird

                                Item {
                                    width: mergeScreenContinueThirdItem.width
                                    height: 48

                                    Item {
                                        id: mergeScreenContinueThirdItem

                                        width: mergeScreenContinueThird.textButton.contentWidth + 64
                                        height: parent.height

                                        Custom.Button {
                                            id: mergeScreenContinueThird

                                            width: parent.width
                                            text: tr.a911_create_company
                                            textButton.textFormat: Text.PlainText
                                            loading_background_color: "transparent"

                                            enabledCustom: {
                                                if (!mergeScreenServices.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyName.itemLoader.item.valid) return false
                                                if (!mergeScreenMainEmail.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyLegalName.itemLoader.item.valid) return false
                                                if (!mergeScreenCeoName.itemLoader.item.valid) return false
                                                if (!mergeScreenRegistrationNumber.itemLoader.item.valid) return false
                                                if (!mergeScreenCompanyType.itemLoader.item.valid) return false
                                                if (!mergeScreenEmployees.itemLoader.item.valid) return false
                                                if (!mergeScreenTechEmail.itemLoader.item.valid) return false

                                                if (!mergeScreenLegalCountry.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalRegion.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalCity.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalCode.itemLoader.item.valid) return false
                                                if (!mergeScreenLegalAddressLines.itemLoader.item.valid) return false

                                                if (!mergeScreenCustomerEmail.itemLoader.item.valid) return false
                                                if (!mergeScreenNumbers.itemLoader.item.valid) return false
                                                if (!mergeScreenWebsite.itemLoader.item.valid) return false
                                                if (!mergeScreenLogo.itemLoader.item.valid) return false
                                                if (!mergeScreenCountry.itemLoader.item.valid) return false
                                                if (!mergeScreenRegion.itemLoader.item.valid) return false
                                                if (!mergeScreenAgree.itemLoader.item.valid) return false

                                                return true
                                            }

                                            anchors.centerIn: parent

                                            onClicked: {
                                                mergeScreenContinueThird.forceActiveFocus()

                                                if (!enabledCustom) return
                                                var companyData = collectUserData()

                                                var settingsData = {
                                                    "email_token": companyStack.confirmedEmails[companyMergeScreen.companyInfo.confirmationInfo.cluster_company_id.toLowerCase()],
                                                    "company": companyData,
                                                    "cluster_company_id": companyMergeScreen.companyInfo.confirmationInfo.cluster_company_id,
                                                }
                                                mergeScreenContinueThird.loading = true
                                                app.company_module.merge_companies(settingsData)
                                            }
                                        }

                                        Connections {
                                            target: app.company_module

                                            onMergeCompaniesSuccess: {
                                                mergeScreenContinueThird.loading = false
                                            }

                                            onMergeCompaniesFailed: {
                                                mergeScreenContinueThird.loading = false
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
        }
    }

    Desktop.BackArea {
        backArea.onClicked: {
            if (listView.currentIndex == 2) {
                listView.currentIndex = 1
                return
            }
            if (listView.currentIndex == 1) {
                listView.currentIndex = 0
                return
            }

            companyLoader.setSource(companyStack.foundScreen, {"companies": companyMergeScreen.companies, "companyName": companyMergeScreen.companyName, "countryCode": companyMergeScreen.countryCode})
        }
    }
}

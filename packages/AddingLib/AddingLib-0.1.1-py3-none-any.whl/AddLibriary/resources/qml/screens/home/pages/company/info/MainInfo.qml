import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import 'qrc:/resources/qml/components/911/DS' as DS
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: mainInfo

    property string companyId: appCompany.id
    property string companyName: appCompany.data.short_name
    property string companyEmail: util.join(appCompany.data.email_addresses, "email", "\n")
    property string companyFullName: appCompany.data.full_name
    property string directorName: appCompany.data.head_of_company
    property string companyType: appCompany.data.company_type
    property string employeesNumber: appCompany.data.employees_number
    property string registrationNumber: appCompany.data.registration_number
    property string technicalEmail: util.join(appCompany.data.technical_emails, "email", "\n")
    property string customerInquiriesEmail: util.join(appCompany.data.customer_inquiries_emails, "email", "\n")
    property string phoneNumber: util.join(appCompany.data.phone_numbers, "number", "\n")
    property string websiteUrl: appCompany.data.web_site_url
    property string countryCode: appCompany.data.country_code
    property bool synced: appCompany.data.synchronized
    property bool inMarketplace: appCompany.data.marketplace_visibility_status == "VISIBLE_IN_MARKET_PLACE"
    property var conflicts: synced ? {} : appCompany.conflicts
    property var confirmedEmails: appCompany.confirmed_emails
    property var legalAddress: appCompany.data.legal_address
    property var mailAddress: appCompany.data.postal_address
    property string companyLogo: (appCompany.data.company_logo.images.filter(
        (image) => image.resolution == "original"
    )[0] || {"url": ""}).url
    property string companyCountry: application.countries ? util.get_country_name_alt(application.countries.countries, countryCode) : countryCode
    property string legalAddressLabel: util.join([
        legalAddress.zip_code,
        application.countries ? util.get_country_name_alt(application.countries.countries, legalAddress.country) : legalAddress.country,
        legalAddress.state,
        legalAddress.city,
        legalAddress.address_line1,
        legalAddress.address_line2
    ], "")
    property string companyLocations: (!!companyCountry ? companyCountry + "\n" : "") + util.join(appCompany.data.locations, "")

    color: ui.backgrounds.base

    Component.onCompleted: {
        syncedChanged()
    }

    onSyncedChanged: if (!synced && companyAccess.COMPANY_GENERAL_INFO_EDIT) app.company_module.get_user_mc_company()

    Item {
        anchors.fill: parent

        Loader {
            id: editInfoLoader

            anchors.fill: parent

            z: 2
        }

        DS.ScrollView {
            id: view

            contentHeight: content.height

            ScrollBar.vertical: DS.ScrollBar {}

            Item {
                width: parent.width
                height: 40

                anchors {
                    right: parent.right
                    top: parent.top
                    margins: 32
                }

                z: 1

                DS3.ButtonOutlined {
                    id: editButton

                    implicitWidth: 166

                    text: tr.edit
                    visible: companyAccess.COMPANY_GENERAL_INFO_EDIT

                    anchors.right: parent.right

                    onClicked: {
                        if (editInfoLoader.source == "") {
                            application.debug("company -> company info -> general info -> edit")
                            editInfoLoader.setSource("qrc:/resources/qml/screens/home/pages/company/info/EditMainInfo.qml")
                            companyStack.companyEditMode = true
                        }
                    }
                }
            }

            Column {
                id: content

                width: view.width

                z: 0
                padding: 32

                DS.Text {
                    text: tr.a911_general_info
                    weight: Font.Bold
                    size: 32
                    line: 40
                    color: ui.colors.base
                }

                Spacing { height: 32 }

                Spacing { height: 32 }

                RowLayout {
                    id: dataGroup

                    width: parent.width - 2 * content.padding

                    spacing: 32

                    Column {
                        id: dataAboutCompanyLeft

                        spacing: 32
                        Layout.preferredWidth: (dataGroup.width - spacing) / 2
                        Layout.alignment: Qt.AlignTop

                        DataRow {
                            title: tr.company_id
                            value: companyId
                            copy: true
                        }

                        DataRow {
                            title: tr.a911_short_word
                            value: companyName
                        }

                        DataRow {
                            title: tr.field_company_email_add_hubs
                            value: companyEmail
                        }

                        DataRow {
                            title: tr.a911_full_name
                            value: companyFullName
                        }

                        DataRow {
                            title: tr.a911_director_fio
                            value: directorName
                        }
                    }

                    Column {
                        id: dataAboutCompanyRight

                        spacing: 32
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop | Qt.AlignLeft

                        DataRow {
                            title: tr.сompany_type
                            value: {
                                return {
                                    "INSTALLATION_COMPANY_OR_INSTALLER": tr.company_type_option_installation,
                                    "MONITORING_COMPANY": tr.company_type_option_cms,
                                    "SECURITY_COMPANY": tr.company_type_option_mix,
                                    "DISTRIBUTOR": tr.distributor,
                                    "RESELLER_OR_SUB_DISTRIBUTOR": tr.company_type_option_reseller,
                                    "FIRE_DETECTION_COMPANY": tr.company_type_option_fire,
                                    "CORPORATE_CLIENT": tr.company_type_option_corporate,
                                    "SYSTEM_INTEGRATOR_OR_SECURITY_CONSULTANT": tr.company_type_option_intergator,
                                    "END_USER": tr.company_type_option_enduser,
                                    "OTHER": tr.a911_other_alarm_reason,
                                    "NO_COMPANY_TYPE_INFO": ""
                                }[companyType]
                            }
                        }

                        DataRow {
                            title: tr.number_of_employees
                            value: {
                                return {
                                    "EMPLOYEES_NUMBER_1": "1",
                                    "EMPLOYEES_NUMBER_2_10": "2–10",
                                    "EMPLOYEES_NUMBER_11_30": "11–30",
                                    "EMPLOYEES_NUMBER_31_50": "31–50",
                                    "EMPLOYEES_NUMBER_51_100": "51–100",
                                    "EMPLOYEES_NUMBER_101_200": "101–200",
                                    "EMPLOYEES_NUMBER_201_300": "201–300",
                                    "EMPLOYEES_NUMBER_301_500": "301–500",
                                    "EMPLOYEES_NUMBER_500_OR_MORE": ">500",
                                    "EMPLOYEES_NUMBER_UNKNOWN": tr.na,
                                    "NO_EMPLOYEES_NUMBER_INFO": ""
                                }[employeesNumber]
                            }
                        }

                        DataRow {
                            title: tr.a911_state_declaration_number
                            value: registrationNumber
                        }

                        DataRow {
                            title: tr.field_company_technical_email
                            value: technicalEmail
                        }
                    }
                }


                Spacing { height: 64 }
                Divider { width: parent.width - 2 * content.padding }
                Spacing { height: 16 }

                DS.Text {
                    text: tr.a911_legal_address
                    weight: Font.Bold
                    size: 32
                    line: 40
                    color: ui.colors.base
                }

                Spacing { height: 40 }

                DS.Text {
                    width: content.width - 2 * content.padding

                    text: legalAddressLabel
                    size: 16
                    line: 24
                    color: ui.colors.base
                }

                Spacing { height: 64 }
                Divider { width: parent.width - 2 * content.padding }
                Spacing { height: 16 }

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

                RowLayout {
                    id: publicInfo

                    width: parent.width

                    spacing: 32

                    Column {
                        id: publicInfoLeft

                        spacing: 32
                        Layout.preferredWidth: (dataGroup.width - spacing) / 2
                        Layout.alignment: Qt.AlignTop

                        DataRow {
                            title: tr.field_company_public_email
                            value: customerInquiriesEmail
                        }

                        DataRow {
                            title: tr.company_phone_number
                            value: phoneNumber
                        }

                        DataRow {
                            title: tr.website
                            value: util.hyperlink(websiteUrl, websiteUrl)
                        }

                        DataRow {
                            title: tr.company_editing_country_region
                            value: companyLocations
                        }
                    }

                    Column {
                        id: publicInfoRight

                        spacing: 32
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop | Qt.AlignLeft

                        DataRow {
                            title: tr.a911_logo

                            LogoImage {
                                anchors {
                                    top: parent.top
                                    topMargin: 28
                                }

                                source: companyLogo
                            }
                        }
                    }
                }

                Spacing { height: 32 }
            }
        }
    }

    Connections {
        target: company

        onEditModeOpen: editButton.clicked()
    }
}

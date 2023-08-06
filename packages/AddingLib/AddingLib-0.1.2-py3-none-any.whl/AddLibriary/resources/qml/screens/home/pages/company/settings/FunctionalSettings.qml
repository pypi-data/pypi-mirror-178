import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/company/info"
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: functionalSettingsRect

    color: companyStack.color

    function updateProvidedServices(services) {
        Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
            title: tr.logout_popup_desktop_title,
            text: tr.logout_popup_desktop_descr,
            firstButtonText: tr.restart_now_button,
            firstButtonCallback: () => {
                app.company_module.update_company_provided_services(services)
            },
            isFirstButtonRed: true,
            firstButtonIsOutline: true,
            secondButtonText: tr.later_button,
            secondButtonIsOutline: false,
            isVertical: true
        })
    }

    Connections {
        target: app.company_module

        onUpdateCompanyProvidedServicesFailed: (result) => {
            Popups.popupByPath(
                "qrc:/resources/qml/screens/home/pages/company/settings/UpdateCompanyProvidedSettingsFailedPopup.qml",
                {errors: result}
            )
        }
    }

    Rectangle {
        id: functionalSettings
        color: ui.colors.dark3
        anchors.fill: parent

        property var installersAccess: appCompany.data.provided_services.installation
        property var mediaPolicy: companyAccess.COMPANY_GENERAL_INFO_EDIT
        property var lockedHubs: appCompany.company_type == "MIX"

        Custom.BlockLoading {
            id: settingsLoader

            minTime: 300
            startSignals: [
                app.company_module.getCompanySettings,
                app.company_module.updateCompanyPermissionSettings,
                app.company_module.updateCompanyQrUsageSettings,
                app.company_module.getMediaPolicySettings,
                app.company_module.updateMediaPolicySettings,
                app.company_module.updateCompanyService,
                app.company_module.updateCompanyMaintenanceReportSettings,
            ]
            stopSignals: [
                app.company_module.getCompanySettingsSuccess,
                app.company_module.getCompanySettingsFailed,
                app.company_module.updateCompanyServiceFailed,
                app.company_module.updateCompanyPermissionSettingsSuccess,
                app.company_module.updateCompanyPermissionSettingsFailed,
                app.company_module.updateCompanyQrUsageSettingsSuccess,
                app.company_module.updateCompanyQrUsageSettingsFailed,
                app.company_module.getMediaPolicySettingsSuccess,
                app.company_module.getMediaPolicySettingsFailed,
                app.company_module.updateMediaPolicySettingsSuccess,
                app.company_module.updateMediaPolicySettingsFailed,
                app.company_module.updateCompanyMaintenanceReportSettingsSuccess,
                app.company_module.updateCompanyMaintenanceReportSettingsFailed,
            ]
        }

        DS3.ScrollView {
            id: scrollView

            anchors.fill: parent

            padding: 0
            clip: true
            contentHeight: content.height

            Column {
                id: content

                width: functionalSettings.width

                DS.Spacing { height: 40 }

                DS3.Text {
                    text: tr.services_settings
                    style: ui.ds3.text.title.XLBold

                    anchors {
                        left: content.left
                        leftMargin: 32
                    }
                }

                DS.Spacing { height: 32 }

                DS3.Text {
                    text: tr.function_pro_desktop_title

                    style: ui.ds3.text.body.MRegular
                    color: ui.ds3.figure.secondary

                    anchors {
                        left: content.left
                        leftMargin: 32
                    }
                }

                DS.Spacing { height: 10 }

                Desktop.ColumnItem {
                    id: companyServices

                    width: 700

                    columnItemBody.anchors {
                        left: companyServices.left
                        leftMargin: 32
                    }

                    contentItem: Component {
                        Item {
                            width: 1000
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

                                width: parent.width / 2 - 8
                                height: parent.height

                                anchors.left: parent.left

                                enabled: companyAccess.COMPANY_SERVICES_SETTINGS_EDIT && (
                                    !monitoringService.selected || installationService.selected
                                )
                                selected: appCompany.data.provided_services.monitoring
                                comingSoon: false
                                title: tr.alarm_monitoring

                                reasons: [
                                    tr.function_monitoring_desc1,
                                    tr.function_monitoring_desc2,
                                    tr.function_monitoring_desc3,
                                    tr.function_monitoring_desc4,
                                    tr.function_monitoring_desc5,
                                ]

                                onToggle: updateProvidedServices({
                                    "provided_services": {
                                        'monitoring': !monitoringService.selected,
                                        'installation': installationService.selected,
                                        'reaction': false
                                    }
                                })
                            }

                            Desktop.CompanyService {
                                id: installationService

                                width: parent.width / 2 - 8
                                height: parent.height

                                anchors.right: parent.right

                                enabled: companyAccess.COMPANY_SERVICES_SETTINGS_EDIT && (
                                    !installationService.selected || monitoringService.selected
                                )
                                selected: appCompany.data.provided_services.installation
                                comingSoon: false
                                title: tr.installation_and_maintenance

                                reasons: [
                                    tr.function_installation_desc1,
                                    tr.function_installation_desc2,
                                    tr.function_installation_desc3,
                                    tr.function_installation_desc4,
                                ]

                                onToggle: updateProvidedServices({
                                    "provided_services": {
                                        'monitoring': monitoringService.selected,
                                        'installation': !installationService.selected,
                                        'reaction': false
                                    }
                                })
                            }
                        }
                    }
                }

                GridLayout {
                    id: infoLayout

                    columns: 4
                    rowSpacing: 8
                    columnSpacing: 28
                    width: functionalSettings.width

                    InfoCell {
                        Layout.columnSpan: 4

                        visible: functionalSettings.installersAccess

                        Custom.FontText {
                            font.pixelSize: 20
                            text: tr.access_control
                            color: ui.colors.white
                            opacity: 0.5

                            anchors {
                                bottom: parent.bottom
                                bottomMargin: 12
                                left: parent.left
                                leftMargin: 32
                            }
                        }

                        Item {
                            id: reloadButtonItem
                            width: refreshIcon.width + refreshText.width + 4
                            height: 32

                            visible: false

                            anchors {
                                right: parent.right
                                rightMargin: 32
                                verticalCenter: parent.verticalCenter
                            }

                            Image {
                                id: refreshIcon
                                sourceSize.width: 16
                                sourceSize.height: 16
                                source: "qrc:/resources/images/desktop/button_icons/refresh.svg"
                                anchors {
                                    left: parent.left
                                    verticalCenter: parent.verticalCenter
                                }

                                RotationAnimator {
                                    id: refreshAnim
                                    target: refreshIcon
                                    from: 0
                                    to: 360
                                    duration: 500
                                }
                            }

                            Custom.FontText {
                                id: refreshText

                                width: contentWidth
                                height: contentHeight

                                anchors {
                                    right: parent.right
                                    verticalCenter: parent.verticalCenter
                                }

                                text: tr.Refresh_button_desktop
                                color: ui.colors.green1
                                font.bold: true
                                font.pixelSize: 14
                                verticalAlignment: Text.AlignVCenter
                            }

                            Custom.HandMouseArea {
                                onClicked: {
                                    refreshAnim.start()
                                    app.company_module.get_company_settings()
                                }
                            }
                        }
                    }

                    InfoCell {
                        Layout.minimumHeight: 128
                        Layout.maximumHeight: 128
                        Layout.columnSpan: 2

                        visible: functionalSettings.installersAccess
                        enabled: companyAccess.COMPANY_GLOBAL_INSTALLER_ACCESS_SETTINGS

                        Column {
                            spacing: 16
                            width: parent.width - 32
                            height: parent.height
                            anchors {
                                top: parent.top
                                topMargin: 16
                                left: parent.left
                                leftMargin: 32
                            }

                            Rectangle {
                                width: 440
                                height: 40
                                radius: 10
                                color: installationToggle.checked ? ui.colors.dark1 : ui.colors.dark2

                                Custom.FontText {
                                    width: parent.width - 64

                                    anchors {
                                        left: parent.left
                                        leftMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }

                                    text: tr.a911_installer
                                    color: ui.colors.white
                                    font.pixelSize: 16
                                    font.weight: Font.Light
                                    wrapMode: Text.WordWrap
                                }

                                Custom.Toggle {
                                    id: installationToggle

                                    anchors {
                                        right: parent.right
                                        rightMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }

                                    mouseArea.onClicked: {
                                        app.company_module.update_company_permission_settings(!installationToggle.checked)
                                    }

                                    checked: {
                                        if (!appCompany) return false
                                        if (!appCompany.workplaces_model) return false
                                        if (!appCompany.workplaces_model.incidents_settings) return false
                                        if (!appCompany.workplaces_model.incidents_settings.facility_permission_settings) return false
                                        if (!appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access) return false

                                        if (appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access == "ON") return true
                                        return false
                                    }
                                }
                            }

                            Item {
                                width: 440
                                height: 40

                                Custom.FontText {
                                    id: toggleAccessTip

                                    width: parent.width
                                    height: parent.height

                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }

                                    text: installationToggle.checked ? tr.access_control_for_installers_on : tr.access_control_for_installers_off
                                    color: ui.colors.white
                                    opacity: 0.5
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    verticalAlignment: Text.AlignTop
                                }
                            }
                        }
                    }

                    InfoCell {
                        Layout.columnSpan: 2

                        visible: functionalSettings.installersAccess

                    }

                    InfoCell {
                        Layout.columnSpan: 4

                        visible: functionalSettings.mediaPolicy

                        Custom.FontText {
                            anchors {
                                bottom: parent.bottom
                                bottomMargin: 12
                                left: parent.left
                                leftMargin: 32
                            }

                            font.pixelSize: 20
                            text: tr.company_surveillance_media_title
                            color: ui.colors.white
                            opacity: 0.5

                        }
                    }

                    InfoCell {
                        Layout.minimumHeight: mediaColumn.height + 24
                        Layout.maximumHeight: mediaColumn.height + 24
                        Layout.columnSpan: 2

                        visible: functionalSettings.mediaPolicy

                        Column {
                            id: mediaColumn

                            width: parent.width - 32

                            anchors {
                                top: parent.top
                                topMargin: 16
                                left: parent.left
                                leftMargin: 32
                            }

                            spacing: 16

                            Item {
                                width: 440
                                height: mediaFirstTip.contentHeight

                                Custom.FontText {
                                    id: mediaFirstTip

                                    width: parent.width - 48

                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }

                                    text: tr.company_surveillance_media_tip
                                    color: ui.colors.white
                                    opacity: 0.5
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    verticalAlignment: Text.AlignTop
                                }

                                Item {
                                    id: infoIcon

                                    width: 48
                                    height: 32

                                    anchors {
                                        right: parent.right
                                        bottom: parent.bottom
                                        bottomMargin: -4
                                    }

                                    Image {
                                        sourceSize.width: 32
                                        sourceSize.height: 32
                                        opacity: 0.7
                                        source: "qrc:/resources/images/icons/info-red.svg"
                                        anchors.centerIn: parent

                                        Custom.HandMouseArea {
                                            id: mediaTipArea
                                        }
                                    }
                                }

                                ToolTip {
                                    id: toolTip

                                    width: 296
                                    height: contentText.contentHeight + 24

                                    x: settings.language == "Farsi" ? -300 : 460
                                    y: parent.height - height / 2 - 16

                                    visible: mediaTipArea.containsMouse

                                    contentItem: Custom.FontText {
                                        id: contentText
                                        color: ui.colors.light3
                                        text: tr.media_policy_info
                                        font.pixelSize: 12
                                        wrapMode: Text.Wrap
                                        textFormat: Text.PlainText
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        anchors.centerIn: parent
                                    }

                                    background: Rectangle {
                                        radius: 8
                                        color: ui.colors.dark4
                                        anchors.fill: parent
                                    }
                                }
                            }

                            Item {
                                width: 440
                                height: 40

                                Custom.MediaPolicyCombobox {
                                    id: mediaCombobox

                                    width: parent.width
                                    height: 40

                                    rightPadding: 16

                                    days: {
                                        if (!appCompany) return 0
                                        if (!appCompany.workplaces_model) return 0
                                        if (!appCompany.workplaces_model.media_settings) return 0
                                        if (!appCompany.workplaces_model.media_settings.b2b_surveillance_ttl_in_days) return 0

                                        return appCompany.workplaces_model.media_settings.b2b_surveillance_ttl_in_days
                                    }

                                    onActivated: {
                                        var value = 730

                                        if (index == 0) value = 7
                                        if (index == 1) value = 30
                                        if (index == 2) value = 90
                                        if (index == 3) value = 180
                                        if (index == 4) value = 365
                                        if (index == 5) value = 730

                                        app.company_module.set_media_policy_settings(value)
                                    }
                                }
                            }

                            Item {
                                width: 440
                                height: -44
                            }

                            Item {
                                width: 440
                                height: mediaFirstTip.contentHeight

                                Custom.FontText {
                                    id: mediaSecondTip
                                    text: tr.warning_media_policy
                                    width: parent.width
                                    color: ui.colors.white
                                    opacity: 0.3
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    verticalAlignment: Text.AlignTop
                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }
                                }
                            }
                        }
                    }

                    InfoCell {
                        Layout.columnSpan: 2

                        visible: functionalSettings.mediaPolicy

                    }

                    InfoCell {
                        Layout.columnSpan: 4

                        visible: functionalSettings.lockedHubs

                        Custom.FontText {
                            font.pixelSize: 20
                            text: tr.add_locking_hub_with_qr
                            color: ui.colors.white
                            opacity: 0.5

                            anchors {
                                bottom: parent.bottom
                                bottomMargin: 12
                                left: parent.left
                                leftMargin: 32
                            }
                        }
                    }

                    InfoCell {
                        Layout.minimumHeight: 128
                        Layout.maximumHeight: 128
                        Layout.columnSpan: 2

                        visible: functionalSettings.lockedHubs
                        enabled: companyAccess.HUB_ACCESS_RESTRICT

                        Column {
                            width: parent.width - 32
                            height: parent.height

                            anchors {
                                top: parent.top
                                topMargin: 16
                                left: parent.left
                                leftMargin: 32

                            }

                            spacing: 16

                            Rectangle {
                                width: 440
                                height: 40

                                radius: 10
                                color: denyQrUsage.checked ? ui.colors.dark1 : ui.colors.dark2

                                Custom.FontText {
                                    text: tr.add_locking_hub_with_qr_enable
                                    width: parent.width - 64
                                    color: ui.colors.white
                                    font.pixelSize: 16
                                    font.weight: Font.Light
                                    wrapMode: Text.WordWrap
                                    anchors {
                                        left: parent.left
                                        leftMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Custom.Toggle {
                                    id: denyQrUsage

                                    anchors {
                                        right: parent.right
                                        rightMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }

                                    mouseArea.onClicked: {
                                        app.company_module.update_qr_usage_settings(!denyQrUsage.checked)
                                    }

                                    checked: {
                                        if (!appCompany) return false
                                        if (!appCompany.workplaces_model) return false
                                        if (!appCompany.workplaces_model.incidents_settings) return false
                                        if (!appCompany.workplaces_model.incidents_settings.qr_usage_settings) return false
                                        if (!appCompany.workplaces_model.incidents_settings.qr_usage_settings.deny_qr_usage) return false

                                        if (appCompany.workplaces_model.incidents_settings.qr_usage_settings.deny_qr_usage) return true
                                        return false
                                    }
                                }
                            }

                            Item {
                                width: 440
                                height: 40

                                Custom.FontText {
                                    id: toggleQrTip

                                    width: parent.width
                                    height: parent.height

                                    text: tr.add_locking_hub_with_qr_tip
                                    color: ui.colors.white
                                    opacity: 0.5
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    verticalAlignment: Text.AlignTop
                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }
                                }
                            }
                        }
                    }

                    InfoCell {
                        Layout.columnSpan: 2

                        visible: functionalSettings.lockedHubs
                    }


                    // MAINTENANCE REPORT

                    InfoCell {
                        id: maintenanceReport

                        Layout.columnSpan: 4

                        visible: companyAccess.MAINTENANCE_REPORT_TOGGLE && __maintenance_report_features__

                        Custom.FontText {
                            text: tr.objects_maintenance_title

                            font.pixelSize: 20
                            color: ui.colors.white
                            opacity: 0.5

                            anchors {
                                bottom: parent.bottom
                                bottomMargin: 12
                                left: parent.left
                                leftMargin: 32
                            }
                        }
                    }

                    InfoCell {
                        Layout.minimumHeight: 128
                        Layout.maximumHeight: 128
                        Layout.columnSpan: 2

                        visible: maintenanceReport.visible


                        Column {
                            width: parent.width - 32
                            height: parent.height

                            anchors {
                                top: parent.top
                                topMargin: 16
                                left: parent.left
                                leftMargin: 32

                            }

                            spacing: 16

                            Rectangle {
                                width: 440
                                height: 40

                                radius: 10
                                color: ui.colors.dark2

                                Custom.FontText {
                                    width: parent.width - 64

                                    text: tr.maintenance_reports_creating_title
                                    color: ui.colors.white
                                    font.pixelSize: 16
                                    font.weight: Font.Light
                                    wrapMode: Text.WordWrap
                                    anchors {
                                        left: parent.left
                                        leftMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Custom.Toggle {
                                    id: reportToggle

                                    anchors {
                                        right: parent.right
                                        rightMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }

                                    checked: {
                                        if (!appCompany
                                            || !appCompany.workplaces_model
                                            || !appCompany.workplaces_model.incidents_settings
                                            || !appCompany.workplaces_model.incidents_settings.maintenance_report_settings
                                            || !appCompany.workplaces_model.incidents_settings.maintenance_report_settings.report_enabled
                                        ) return false

                                        return (appCompany.workplaces_model.incidents_settings.maintenance_report_settings.report_enabled == "ON")
                                    }

                                    mouseArea.onClicked: {
                                        app.company_module.update_maintenance_report_settings(!reportToggle.checked)
                                    }
                                }
                            }

                            Item {
                                width: 440
                                height: 60

                                Custom.FontText {
                                    id: reportDescription

                                    width: parent.width
                                    height: parent.height

                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }

                                    text: tr.maintenance_reports_creating_descr
                                    color: ui.ds3.figure.contrast
                                    opacity: 0.5
                                    font.pixelSize: 14
                                    wrapMode: Text.WordWrap
                                    textFormat: Text.PlainText
                                    verticalAlignment: Text.AlignTop
                                }
                            }
                        }
                    }

                    InfoCell {
                        Layout.columnSpan: 4
                    }
                }
            }
        }
    }
}
